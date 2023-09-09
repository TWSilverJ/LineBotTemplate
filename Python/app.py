import base64
from dotenv_vault import load_dotenv
from flask import Flask, jsonify, request
import hashlib
import hmac
import os
import requests

# 讀取環境變數
load_dotenv()

# 準備 Line message API 相關參數
channel_access_token = os.environ.get("CHANNEL_ACCESS_TOKEN")
channel_secret = os.environ.get("CHANNEL_SECRET")
line_message_api_url = "https://api.line.me/v2/"
line_message_api_headers = {
    "Authorization": f"Bearer {channel_access_token}",
    "Content-Type": "application/json",
}

# 實作 Flask
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


# 路由
@app.route("/")
def hello():
    return "Hello World!"


@app.route("/webhook", methods=["POST"])
def line_webhook():
    # 取得數位簽章
    signature = request.headers.get("x-line-signature")
    if signature is None:
        return jsonify({"message": "數位簽章無效"}), 403

    # 取得 HTTP request body ，檢查數位簽章
    if request.is_json:
        raw_data = request.data

        # 使用 HMAC-SHA-256 創建 HMAC 物件
        hmac_obj = hmac.new(channel_secret.encode("utf-8"), raw_data, hashlib.sha256)

        # 雜湊值比對
        if hmac.compare_digest(hmac_obj.digest(), base64.b64decode(signature)):
            # 驗證成功，數位簽章有效

            # 處理事件
            messages = []
            for event in request.get_json()["events"]:
                print(event)

                # 從這裡開始定義規則
                # 範例：針對文字訊息原封不動的回覆
                try:
                    if (
                        event["type"] == "message"
                        and event["message"]["type"] == "text"
                    ):
                        messages.append(
                            {"type": "text", "text": event["message"]["text"]}
                        )
                    pass
                except:
                    pass

            # 將產出訊息回覆
            if len(messages) > 0:
                r = requests.post(
                    f"{line_message_api_url}/bot/message/reply",
                    headers=line_message_api_headers,
                    json={"replyToken": event["replyToken"], "messages": messages},
                )
                print(r.status_code, r.json())

            # 回覆請求
            return jsonify({"message": "OK"}), 200
        else:
            # 驗證失敗，數位簽章無效
            return jsonify({"message": "數位簽章無效"}), 403
    else:
        return jsonify({"error": "Invalid JSON"}), 400


# 啟動程式
if __name__ == "__main__":
    # 取得 Line webhook endpoint
    url = os.environ.get("APP_URL")
    r = requests.get(
        f"{line_message_api_url}/bot/channel/webhook/endpoint",
        headers=line_message_api_headers,
    )
    data = r.json()

    # 比對 endpoint
    if url != data["endpoint"]:
        # 更新 endpoint
        r = requests.put(
            f"{line_message_api_url}/bot/channel/webhook/endpoint",
            headers=line_message_api_headers,
            json={"endpoint": f"{url}/webhook"},
        )
        print(r.status_code, r.json())

    # 啟動 Web server
    HOST = os.environ.get("HOST", "localhost")
    try:
        PORT = int(os.environ.get("PORT", "5555"))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

    # 測試 Line webhook
    r = requests.post(
        f"{line_message_api_url}/bot/channel/webhook/test",
        headers=line_message_api_headers,
    )
    print(r.status_code, r.json())
