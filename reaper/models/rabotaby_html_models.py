"""Storage module for class MainPage"""
import logging

from requests import codes

from reaper.tools.parsers.parsing import RabotabyHTMLParser
from reaper.tools.clients.http_client import HTTPClient

DEFAULT_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/93.0.4577.82 Safari/537.36', 'accept': '*/*'}

BASE_URL = 'https://hh.ru/search/vacancy?clusters=true&area=1002&ored_clusters=true&enable_snippets=true&salary=&text='


class MainPage:
    """Class works with main rabota.by page"""

    def __init__(self, keyword: str, http_client: HTTPClient = HTTPClient(), base_url: str = BASE_URL):
        """
        Initialization method
        :param keyword: url main page with keyword python
        :param http_client: http_client
        :param base_url: base url for search
        """
        self.keyword = keyword
        self.url = f'{base_url}{keyword}'
        self.http_client = http_client

    @property
    def vacancy_names(self) -> list:
        """
        Method for receive vacancy names
        :return: list with vacancy names
        """
        try:
            response = self.http_client.get(self.url, DEFAULT_HEADERS)
            if response.status_code == codes.ok:
                total_names = []
                page_count = RabotabyHTMLParser.parse_pages_count(RabotabyHTMLParser(response.text))
                for page in range(page_count):
                    response = self.http_client.get(self.url, DEFAULT_HEADERS, params={'page': page})
                    total_names += RabotabyHTMLParser.parse_vacancy_names(RabotabyHTMLParser(response.text))
                return total_names
        except Exception as ex:
            logging.error(ex)

    @property
    def vacancy_links(self) -> list:
        """
        Method for receive vacancy links
        :return: list with vacancy links
        """
        try:
            response = self.http_client.get(self.url, DEFAULT_HEADERS)
            if response.status_code == codes.ok:
                total_links = []
                page_count = RabotabyHTMLParser.parse_pages_count(RabotabyHTMLParser(response.text))
                for page in range(page_count):
                    response = self.http_client.get(self.url, DEFAULT_HEADERS, params={'page': page})
                    total_links += RabotabyHTMLParser.parse_vacancy_links(RabotabyHTMLParser(response.text))
                return total_links
        except Exception as ex:
            logging.error(ex)

    @property
    def dict_with_data(self) -> dict:
        """
        Method for create dict with data from vacancy_links and vacancy_names methods
        :return: dict with vacancy names and vacancy links
        """
        parse_data = dict(zip(self.vacancy_names, self.vacancy_links))
        return parse_data
