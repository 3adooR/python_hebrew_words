from services.AsyncWordsService import AsyncWordsService
from sanic import Blueprint, json


class WordController:
    def __init__(self, session):
        """ Set URL prefix and service """
        self.blueprint = Blueprint('api', url_prefix='/api')
        self.service = AsyncWordsService(session)

    def setup_routes(self):
        """ Add routes """
        self.blueprint.add_route(self.get_word, '/word', methods=['GET'], name='get_word')
        self.blueprint.add_route(self.check_word, '/check', methods=['POST'], name='check_word')

    async def get_word(self, request):
        """ Return random word and variants of translation """
        words = await self.service.get_word_with_variants()
        return json({'data': words})

    async def check_word(self, request):
        """ Check translation of the word by UUID """
        if request.json is None:
            return json({'error': 'No JSON data received'}, status=400)

        json_data = request.json
        word_uuid = json_data.get('uuid')
        translation = json_data.get('translation')

        if word_uuid is None and translation is None:
            return json({'error': 'You need to send UUID of the word and chosen translation'}, status=400)

        result = await self.service.check_translation(word_uuid, translation)

        return json({'result': result})
