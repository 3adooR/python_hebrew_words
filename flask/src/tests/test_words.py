import http
import json
from flask.src import app
from dataclasses import dataclass
from unittest.mock import patch


@dataclass
class FakeWord:
    rus = 'Fake rus'
    heb = 'Fake heb'


class TestWords:
    uuid = []

    def test_get_words_with_db(self):
        client = app.test_client()
        resp = client.get('/words')
        assert resp.status_code == http.HTTPStatus.OK

    @patch('src.services.word_service.WordService.fetch_all_fields', autospec=True)
    def test_get_words_width_mock_db(self, mock_db_call):
        client = app.test_client()
        resp = client.get('/words')
        mock_db_call.assert_called_once()
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json) == 0

    def test_create_word_with_db(self):
        client = app.test_client()
        data = {
            'rus': 'test rus',
            'heb': 'test heb'
        }
        resp = client.post('/words', data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json['rus'] == data['rus']
        self.uuid.append(resp.json['uuid'])

    def test_create_word_with_mock_db(self):
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {
                'rus': 'test rus',
                'heb': 'test heb'
            }
            resp = client.post('/words', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_update_word_with_db(self):
        url = f'/words/{self.uuid[0]}'
        client = app.test_client()
        data = {
            'rus': 'updated rus',
            'heb': 'updated heb'
        }
        resp = client.put(url, data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json['rus'] == data['rus']

    def test_update_word_with_mock_db(self):
        with patch('src.services.word_service.WordService.fetch_word_bu_uuid', autospec=True) as mocked_query, \
                patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = FakeWord()
            url = f'/words/{self.uuid[0]}'
            client = app.test_client()
            data = {
                'rus': 'updated rus',
                'heb': 'updated heb'
            }
            resp = client.put(url, data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()
            assert resp.json['rus'] == data['rus']

    def test_delete_word_with_db(self):
        url = f'/words/{self.uuid[0]}'
        client = app.test_client()
        resp = client.delete(url)
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
