from src import app
from dotenv import dotenv_values

if __name__ == '__main__':
    env = dotenv_values(".env")
    app.run(
        host='0.0.0.0',
        debug=bool(env['APP_DEBUG']),
        port=int(env['FLASK_PORT'])
    )
