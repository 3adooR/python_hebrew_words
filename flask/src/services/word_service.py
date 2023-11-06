from sqlalchemy.exc import NoResultFound

from src.database.models import Word


class WordService:
    @staticmethod
    def fetch_all_fields(session):
        return session.query(Word)

    @classmethod
    def fetch_word_bu_uuid(cls, session, uuid):
        return cls.fetch_all_fields(session).filter_by(
            uuid=uuid
        ).first()

    @staticmethod
    def bulk_create_words(session, words):
        count_added_words = 0
        words_to_create = [Word(**word) for word in words]
        for word in words_to_create:
            try:
                existing_obj = session.query(Word).filter_by(heb=word.heb).one()
                existing_obj.rus = word.rus
                session.merge(existing_obj)
            except NoResultFound:
                session.add(word)
                count_added_words += 1
        session.commit()
        return count_added_words
