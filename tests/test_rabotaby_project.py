import pytest
from requests import codes

from reaper.tools.clients.http_client import HTTPClient

from reaper.models.rabotaby_html_models import DEFAULT_HEADERS


class TestParser:
    http_client = HTTPClient()

    def test_response_code_200(self, test_data: dict):
        response = self.http_client.get(test_data.get('url'), DEFAULT_HEADERS)
        assert response.status_code == codes.ok, f"server does not respond"

    def test_page_count(self, page_count):
        assert isinstance(page_count, int), f"page count should be have integer type"
        assert page_count, f"page count should not be empty"

    def test_parse_vacancy_links(self, vacancy_links_parser, test_data):
        assert isinstance(vacancy_links_parser, list), f"collection with links should be have list type"
        assert vacancy_links_parser, f"list with vacancy links can't be empty"

    def test_parse_vacancy_names(self, vacancy_names_parser, test_data):
        assert isinstance(vacancy_names_parser, list), f"collection with names should be have list type"
        assert vacancy_names_parser, f"list with vacancy names can't be empty"


class TestMainPage:

    def test_get_vacancy_links(self, vacancy_links, test_data):
        assert vacancy_links, f"list with vacancy links can't be empty"
        assert isinstance(vacancy_links, list), f"collection with links should be have list type"

    def test_get_vacancy_names(self, vacancy_names, test_data):
        assert vacancy_names, f"list with vacancy names can't be empty"
        assert isinstance(vacancy_names, list), f"collection with names should be have list type"


class TestDatabase:

    def test_get_data_from_database(self, database_data, link_from_database, test_data):
        assert database_data, f"database can't be empty"
        assert link_from_database == test_data.get('data').get('test_name'), f"{test_data.get('data').get('test_name')}"

    def test_database_delete(self, database_delete):
        assert not database_delete, f"The database is not deleted"
