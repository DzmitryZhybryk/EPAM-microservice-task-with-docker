"""Storage module for class RabotabyHTMLParser"""
import re

from bs4 import BeautifulSoup


class RabotabyHTMLParser(BeautifulSoup):
    """Parsing class for working with Rabotaby pages"""

    def __init__(self, html):
        """
        Initialization method
        :param html: page html code
        """
        self.html = html

    def parse_pages_count(self) -> int:
        """
        Method for calculating the number of parsing pages
        :return: pages count
        """
        soup = BeautifulSoup(self.html, 'lxml')
        pagination = soup.find_all('span', class_="pager-item-not-in-short-range")
        if pagination:
            return int(pagination[-1].get_text())
        return 1

    def parse_vacancy_links(self) -> list:
        """
        Method creates the soup object and parses it for receive all vacancy links
        :return: list with all vacancy links
        """
        all_vacancy_links = []
        soup = BeautifulSoup(self.html, 'lxml')
        data = soup.find_all('span', class_='g-user-content')
        for items in data:
            item = items.find('a', class_="bloko-link").get("href")
            all_vacancy_links.append(item)
        return all_vacancy_links

    @staticmethod
    def __helper_parse_vacancy_names(text):
        """
        Helper parse_vacancy_names method. Checks for unnecessary characters in the vacancy names
        :param text: verification data
        :return: vacancy names
        """
        return re.sub(r'\xa0', ' ', text)

    def parse_vacancy_names(self) -> list:
        """
        Method creates the soup object and parses it for receive all vacancy names
        :return: list with all vacancy names
        """
        all_vacancy_names = []
        soup = BeautifulSoup(self.html, 'lxml')
        data = soup.find_all('span', class_='g-user-content')
        for items in data:
            item = items.find('a', class_="bloko-link").get_text(strip=True)
            all_vacancy_names.append(RabotabyHTMLParser.__helper_parse_vacancy_names(item))
        return all_vacancy_names
