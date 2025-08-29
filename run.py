from app.server import create_app
from app.config import Config
from waitress import serve

app = create_app()

if __name__ == '__main__':
    if Config.ENV == 'production':
        serve(app, host="0.0.0.0", port=Config.PORT, threads=64)
    else:
        app.run(port=Config.PORT, debug=Config.DEBUG)
    