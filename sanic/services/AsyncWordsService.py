import random
from models.word import Word
from sqlalchemy import func


class AsyncWordsService:
    def __init__(self, session, count_variants: int = 4):
        self.session = session
        self.count_variants = count_variants

    async def get_word_with_variants(self):
        """ Get random words in db, return one of them as word and others in variants """
        data = self.session.query(Word).order_by(func.random()).limit(self.count_variants).all()

        word = data[random.randint(0, len(data) - 1)]
        variants = [item.rus for item in data]

        return {
            'uuid': word.uuid,
            'word': word.heb,
            'variants': variants,
        }

    async def check_translation(self, uuid: str, translation: str) -> bool:
        """ Check translation of the word in db """
        word = self.session.query(Word).filter_by(uuid=uuid).first()
        if word is None:
            return False

        if word.rus != translation:
            return False

        return True
