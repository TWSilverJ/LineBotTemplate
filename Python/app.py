import os
from flask import Flask
from dotenv_vault import load_dotenv
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


@app.route("/webhook")
def line_webhook():
    return "ok"


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
