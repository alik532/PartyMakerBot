import requests

endpoint  = "https://alarmerbot.ru/?key=b26f6d-22e518-467f0c&message=youtube.com"

def do_req():
    get_responce = requests.get(endpoint)
    print(get_responce.status_code)