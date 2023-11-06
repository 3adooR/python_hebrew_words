from dotenv import dotenv_values

env = dotenv_values(".env")
db_host = env['DB_HOST']
db_port = env['DB_PORT']
db_name = env['DB_DATABASE']
db_username = env['DB_USERNAME']
db_password = env['DB_PASSWORD']


class Config:
    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_name}:{db_password}@{db_host}:{db_port}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = env['FLASK_SECRET_KEY']
