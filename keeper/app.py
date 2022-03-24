from database import RabotaDatabase
from flask import Flask, request

app = Flask(__name__)


def create_database(keyword):
    """
    Function create database with table
    """
    database_object = RabotaDatabase(table_name=keyword)
    return database_object


@app.route("/save-data/", methods=["GET", "POST"])
def add_data_to_database():
    """
    Rout for add data to database
    """
    incoming_report = request.get_json()
    create_database(incoming_report.pop("keyword")).add_data(incoming_report)
    return "data was added to database"


@app.route("/send-data/", methods=["GET", "POST"])
def get_data_from_database():
    """
    Rout for get data to database
    """
    incoming_report = request.get_json().popitem()[1]
    database_object = RabotaDatabase(table_name=incoming_report)
    database_object.get_data()
    data_dict = {id_number: {name: link} for id_number, name, link in database_object.get_data()}
    return data_dict


if __name__ == '__main__':
    app.run(host='172.16.238.5', port=5001)
