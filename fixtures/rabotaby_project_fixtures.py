import sqlite3

import docker
from sqlite3 import Cursor

import pytest

import yaml
from requests import Response

from keeper.database import RabotaDatabase
from reaper.tools.clients.http_client import HTTPClient
from reaper.models.rabotaby_html_models import MainPage, DEFAULT_HEADERS
from reaper.tools.parsers.parsing import RabotabyHTMLParser


@pytest.fixture(scope='module')
def global_test_data(request) -> dict:
    """
    Fixture reads the yaml file and returns parameters depending on the test that called it
    :return: dict with parameters
    """
    with open(f'{request.fspath.dirname}/data.yaml') as file:
        return yaml.safe_load(file)


@pytest.fixture(scope='session')
def http_client() -> HTTPClient:
    """
    Fixture make http response
    :return: HTTPClient
    """
    return HTTPClient()


@pytest.fixture
def test_data(global_test_data, request) -> dict:
    """
    Fixture reads the yaml file and returns parameters depending on the test that called it
    :return: dict with parameters
    """
    return global_test_data.get(request.function.__name__)


@pytest.fixture
def response_code(http_client: HTTPClient, test_data: dict) -> Response:
    """
    Fixture for create response object
    :param http_client: http client
    :param test_data: dict with parameters
    :return: response object
    """
    return http_client.get(test_data.get('url'), DEFAULT_HEADERS)


@pytest.fixture
def rabotaby_html_parser_object(response_code: Response) -> RabotabyHTMLParser:
    """
    Fixture create RabotabyHTMLParser object
    :param response_code: response object
    :return: RabotabyHTMLParser object
    """
    return RabotabyHTMLParser(response_code.text)


@pytest.fixture
def page_count(rabotaby_html_parser_object: RabotabyHTMLParser, response_code: Response, http_client: HTTPClient,
               test_data: dict) -> int:
    """
    Fixture returns page count
    :param rabotaby_html_parser_object: object to call parse_pages_count method
    :param http_client: http client
    :param test_data: dict with parameters
    :param response_code: response object
    :return: page count
    """
    return rabotaby_html_parser_object.parse_pages_count()


@pytest.fixture
def vacancy_links_parser(rabotaby_html_parser_object: RabotabyHTMLParser, response_code: Response,
                         http_client: HTTPClient, test_data: dict, page_count: int) -> list:
    """
    Fixture returns vacancy links
    :param rabotaby_html_parser_object: object to call parse_vacancy_links method
    :param http_client: http client
    :param test_data: dict with parameters
    :param response_code: response object
    :param page_count: number of pages
    :return: list with vacancy links
    """
    return rabotaby_html_parser_object.parse_vacancy_links()


@pytest.fixture
def vacancy_names_parser(rabotaby_html_parser_object: RabotabyHTMLParser, response_code: Response,
                         http_client: HTTPClient, test_data: dict, page_count: int) -> list:
    """
    Fixture returns vacancy names
    :param rabotaby_html_parser_object: object to call parse_vacancy_names method
    :param http_client: http client
    :param test_data: dict with parameters
    :param response_code: response object
    :param page_count: number of pages
    :return: list with vacancy names
    """
    return rabotaby_html_parser_object.parse_vacancy_names()


@pytest.fixture
def main_page_object(test_data: dict, http_client: HTTPClient) -> MainPage:
    return MainPage(test_data.get('keyword'))


@pytest.fixture
def vacancy_links(test_data: dict, http_client: HTTPClient, main_page_object: MainPage) -> list:
    """
    Fixture returns vacancy links
    :param test_data: dict with parameters
    :param http_client: http client
    :param main_page_object: RabotabyMainPage object
    :return: list with vacancy links
    """
    return main_page_object.vacancy_links


@pytest.fixture
def vacancy_names(test_data: dict, http_client: HTTPClient, main_page_object: MainPage) -> list:
    """
    Fixture returns vacancy names
    :param test_data: dict with parameters
    :param http_client: http client
    :param main_page_object: RabotabyMainPage object
    :return: list with vacancy names
    """
    return main_page_object.vacancy_names


@pytest.fixture
def rabota_database_object(test_data: dict) -> RabotaDatabase:
    """
    Fixture create database
    :param test_data: dict with parameters
    :return: RabotaDatabase object
    """
    return RabotaDatabase(test_data.get('table_name'), test_data.get('database_name'))


@pytest.fixture
def database_table(rabota_database_object, test_data: dict) -> None:
    """
    Fixture create table in database
    :param rabota_database_object: RabotaDatabase object
    :param test_data: dict with parameters
    """
    return rabota_database_object.new_table()


@pytest.fixture
def database_new_data(database_table: None, rabota_database_object: RabotaDatabase, test_data: dict) -> None:
    """
    Fixture add data to database
    :param rabota_database_object: RabotaDatabase object
    :param test_data: dict with parameters
    """
    rabota_database_object.add_data(test_data.get('data'))


@pytest.fixture
def database_data(database_new_data: None, rabota_database_object: RabotaDatabase, test_data: dict) -> Cursor:
    """
    Fixture receive data from database
    :param rabota_database_object: RabotaDatabase object
    :param test_data: dict with parameters
    :return:
    """
    return rabota_database_object.get_data()


@pytest.fixture
def database_connect(test_data: dict) -> Cursor:
    """
    Fixture create connect to database
    :param test_data: dict with parameters
    :return: Cursor object
    """
    connect = sqlite3.connect(test_data.get('database_name'))
    return connect.cursor()


@pytest.fixture
def link_from_database(database_connect: Cursor, rabota_database_object: RabotaDatabase, test_data: dict) -> list:
    """
    Fixture for receive link from database
    :param database_connect: Cursor object
    :param rabota_database_object:
    :param test_data: dict with parameters
    :return: list with link
    """
    for i in database_connect.execute(f'SELECT link FROM {test_data.get("table_name")}'):
        return i[-1]


@pytest.fixture
def database_delete(database_connect: Cursor, test_data: dict) -> None:
    """
    Fixture for delete table from database
    :param database_connect: Cursor object
    :param test_data: dict with parameters
    """
    database_connect.execute(f"DROP TABLE IF EXISTS {test_data.get('table_name')}")


