import re
import requests
import json

cur_ids = {"USD":145, "EUR":19}

def load_exchange():
    URL = 'https://www.nbrb.by/api/exrates/rates/145'
    response = requests.get(URL)
    print(response.json())
    return response.json()

def cur(currency:str):
    curs_usd = load_exchange(currency)
    return curs_usd['Cur_OfficialRate']



