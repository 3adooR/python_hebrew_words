import config
from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_swagger_ui import get_swaggerui_blueprint

# App
app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app, prefix='/api')
Bootstrap5(app)

# Swagger
SWAGGER_URL = '/swagger'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    '/static/api.yaml',
    config={'app_name': 'Hebrew words API'}
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefixes=SWAGGER_URL)

# API routes
from src import routes
from src.database.models import Word


# Web
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('layouts/index.html', path=request.path)


@app.route('/dictionary', methods=['GET'], endpoint='dictionary')
def items():
    page = request.args.get('page', type=int, default=1)
    words = Word.query.paginate(page=page, per_page=80)
    return render_template('layouts/words.html', words=words, path=request.path)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("layouts/error.html"), 404
