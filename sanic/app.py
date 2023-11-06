import config
from dotenv import dotenv_values
from sanic import Sanic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from controllers.WordController import WordController

app = Sanic(__name__)
engine = create_engine(config.Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
env = dotenv_values(".env")

db_session = Session()
try:
    word_controller = WordController(db_session)
    word_controller.setup_routes()
    app.blueprint(word_controller.blueprint)
finally:
    db_session.close()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(env['SANIC_PORT']),
        debug=bool(env['APP_DEBUG']),
        workers=4
    )
