from flask import Flask
from dotenv_vault import load_dotenv

# 讀取環境變數
load_dotenv()

# 實作 Flask
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# 路由
@app.route('/')
def hello():
    """Renders a sample page."""
    return "Hello World!"

# 啟動程式
if __name__ == '__main__':
    import os
    HOST = os.environ.get('HOST', 'localhost')
    try:
        PORT = int(os.environ.get('PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
