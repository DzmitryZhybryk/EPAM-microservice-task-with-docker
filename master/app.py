"""Storage module for app"""
import logging

import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

keyword = ""


@app.route("/", methods=["GET"])
def main_page():
    return render_template("welcome_page.html")


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        input_data = request.form["name"]
        try:
            global keyword
            keyword = {'vac': input_data}
            response = requests.post(
                url="http://172.16.238.10:5002/scrap/",
                json=keyword)
            return redirect("/search/data/")
        except KeyError as ex:
            logging.error(ex)
    return render_template("search_page.html")


@app.route("/search/data/", methods=["GET", "POST"])
def database_data():
    """
    Route get information from database
    """
    response = requests.post(url="http://172.16.238.5:5001/send-data/",
                             json=keyword)
    data = response.json()
    return data


if __name__ == '__main__':
    app.run(host='172.16.238.15', port=5000)
