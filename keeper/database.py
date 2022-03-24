"""Storage module for class RabotaDatabase"""
import logging
import sqlite3
from sqlite3 import Cursor


class RabotaDatabase:
    """Class works with database"""

    __database_connection = None

    def __new__(cls, *args, **kwargs):
        if cls.__database_connection is None:
            cls.__database_connection: RabotaDatabase = super().__new__(cls)
        return cls.__database_connection

    def __del__(self):
        RabotaDatabase.__database_connection = None

    def __init__(self, table_name: str, database_name='my_database.db'):
        """
        Initialization method
        :param table_name: name for new table
        """
        self.database_name = database_name
        self.table_name = table_name
        self.connect = sqlite3.connect(self.database_name)
        self.cursor = self.connect.cursor()

    def new_table(self) -> None:
        """Method create new tables in the database """
        try:
            new_table = f"CREATE TABLE IF NOT EXISTS {self.table_name}(id INTEGER PRIMARY KEY," \
                        f"name VARCHAR(255),link VARCHAR(255))"
            self.cursor.execute(new_table)
            self.connect.commit()
        except Exception as ex:
            logging.error(ex)

    def add_data(self, data: dict) -> None:
        """
        Method for adding data to the tables
        :param data: dict with data for adding
        """
        try:
            self.new_table()
            with self.connect:
                self.cursor.execute(f'SELECT link FROM {self.table_name}')
                already_in_db = self.cursor.fetchall()
                for name, link in data.items():
                    if (link,) not in already_in_db:
                        self.cursor.execute(f"INSERT INTO {self.table_name}(name, link) VALUES(?, ?);", (name, link))
                        self.connect.commit()
                    else:
                        logging.debug('This record already exist')
        except Exception as ex:
            logging.error(ex)

    def get_data(self) -> Cursor:
        """
        Method for receive information from the table
        :return: cursor object
        """
        try:
            with self.connect:
                return self.cursor.execute(f"SELECT * FROM {self.table_name}")
        except Exception as ex:
            logging.error(ex)
