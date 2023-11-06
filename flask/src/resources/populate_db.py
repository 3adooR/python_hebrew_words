import datetime
import bs4
import requests
from flask_restful import Resource
from urllib.parse import urlparse, parse_qs
from src import db
from src.resources.auth import token_required
from src.services.word_service import WordService
from concurrent.futures.thread import ThreadPoolExecutor as PoolExecutor


class Populate(Resource):
    url = 'https://www.pealim.com/ru/dict/'

    @token_required
    def post(self):
        t0 = datetime.datetime.now()
        words = self.parse_verbs()
        if words is None:
            return {'message': f'No words..'}, 201
        created_words = self.populated_db_with_words(words)
        dt = datetime.datetime.now() - t0
        print(f'Done in {dt.total_seconds()}')

        return {'message': f'Database was populated with {created_words} words'}, 201

    def parse_verbs(self):
        verbs_url = self.url + '?pos=verb&num-radicals=all'
        resp = requests.get(verbs_url)
        resp.raise_for_status()
        html = resp.text
        soup = bs4.BeautifulSoup(html, features='html.parser')

        count_pages = self.__count_pages(soup)
        if count_pages is None:
            return []

        work = []
        with PoolExecutor() as executor:
            for page in range(1, count_pages + 1):
                url = verbs_url + '&page=' + str(page)
                f = executor.submit(self.__parse_words, url)
                work.append(f)
        words = [f.result() for f in work]
        words = [word for sublist in words for word in sublist]

        return words

    def __parse_words(self, url: str):
        words = []
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            html = resp.text
            soup = bs4.BeautifulSoup(html, features='html.parser')
            html_table = soup.find('table', class_='dict-table-t')
            html_tr = html_table.find_all('tr')
            for word in html_tr:
                html_td = word.find_all('td')
                if html_td:
                    words.append({
                        'heb': html_td[0].find('a').text.strip(),
                        'rus': html_td[3].text.strip()
                    })
            print('Parsed page: ', url)
        except:
            print('Failed to parse page: ', url)

        return words

    def __count_pages(self, soup):
        html_ul = soup.find('ul', class_='pagination')
        last_a_tag = html_ul.find_all('li')[-1].find('a')
        last_href = last_a_tag.get('href')
        parsed_url = urlparse(last_href)
        query_parameters = parse_qs(parsed_url.query)
        last_page = query_parameters.get('page')

        return int(last_page[0])

    @staticmethod
    def populated_db_with_words(words: dict):
        return WordService.bulk_create_words(db.session, words)
