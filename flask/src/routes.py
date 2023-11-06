from src import api
from src.resources.auth import AuthRegister, AuthLogin
from src.resources.words import Words
from src.resources.populate_db import Populate

api.add_resource(AuthRegister, '/register', strict_slashes=False)
api.add_resource(AuthLogin, '/login', strict_slashes=False)
api.add_resource(Words, '/words', "/words/<uuid>", strict_slashes=False)
api.add_resource(Populate, '/pop', strict_slashes=False)
