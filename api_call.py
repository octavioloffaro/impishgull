import requests
import json

def get_values(company,api_key,search):
    function = "SYMBOL_SEARCH" if search == True else "GLOBAL_QUOTE"
    keyword= "keywords" if search == True else "symbol"
    API_URL = "https://www.alphavantage.co/query"
    data = {
        "function": function,
        "{}".format(keyword) : company,
        "apikey": api_key}
    response = requests.get(API_URL, params=data)
    return (json.loads(response.text))