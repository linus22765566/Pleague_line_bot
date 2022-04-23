import requests
from bs4 import BeautifulSoup
from lxml import etree
response = requests.get("https://pleagueofficial.com/schedule-regular-season")
allinfo = BeautifulSoup(response.text, "html.parser")
future_four_game = allinfo.find_all("div",class_="is-future",limit = 4)
for a_game in future_four_game:
    print((a_game.find_all("a",class_="fs12 mt-md-2 my-0 py-0 d-md-block d-inline mr-2")[1]['href']))