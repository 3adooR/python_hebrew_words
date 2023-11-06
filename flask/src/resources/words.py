from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from src import db
from src.resources.auth import token_required
from src.schemas.words import WordSchema
from src.services.word_service import WordService


class Words(Resource):
    word_schema = WordSchema()

    def get(self, uuid=None):
        if not uuid:
            word_list = WordService.fetch_all_fields(db.session).all()
            return self.word_schema.dump(word_list, many=True), 200
        word = WordService.fetch_word_bu_uuid(db.session, uuid)
        if not word:
            return {'message': 'Not found'}, 404
        return self.word_schema.dump(word), 200

    @token_required
    def post(self):
        try:
            word = self.word_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(word)
        db.session.commit()
        return self.word_schema.dump(word), 201

    @token_required
    def put(self, uuid):
        word = WordService.fetch_word_bu_uuid(db.session, uuid)
        if not word:
            return {'message': 'Not found'}, 404
        try:
            word = self.word_schema.load(request.json, instance=word, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(word)
        db.session.commit()
        return self.word_schema.dump(word), 200

    @token_required
    def patch(self, uuid):
        word = WordService.fetch_word_bu_uuid(db.session, uuid)
        if not word:
            return {'message': 'Not found'}, 404
        word_json = request.json
        rus = word_json.get('rus')
        heb = word_json.get('heb')
        if rus:
            word.rus = rus
        if heb:
            word.heb = heb
        try:
            word = self.word_schema.load(request.json, instance=word, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(word)
        db.session.commit()
        return {'message': 'Updated successfully'}, 201

    @token_required
    def delete(self, uuid):
        word = WordService.fetch_word_bu_uuid(db.session, uuid)
        if not word:
            return {'message': 'Not found'}, 404
        db.session.delete(word)
        db.session.commit()
        return '', 204
