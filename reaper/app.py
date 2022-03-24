import requests
from flask import Flask, request

from reaper.models.rabotaby_html_models import MainPage

app = Flask(__name__)


@app.route("/scrap/", methods=["POST", "GET"])
def reaper_service_run():
    """
    Route send scraping data to database rout
    """
    if request.method == "POST":
        incoming_report = request.get_json().popitem()[1]
        parse_object = MainPage(incoming_report)
        keyword = {"keyword": incoming_report}
        send_data = parse_object.dict_with_data | keyword
        response_data = requests.post(
            url="http://172.16.238.5:5001/save-data/",
            json=send_data)
        return "the data were sent to the database"


if __name__ == "__main__":
    app.run(host='172.16.238.10', port=5002)
