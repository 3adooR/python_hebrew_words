from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.database.models import Word


class WordSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Word
        exclude = ['id']
        load_instance = True
