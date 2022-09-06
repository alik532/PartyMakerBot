import requests

endpoint  = "https://alarmerbot.ru/?key=ecefc4-59d973-347ce8&message=Hello"

def do_req():
    get_responce = requests.get(endpoint)
    print(get_responce.status_code)