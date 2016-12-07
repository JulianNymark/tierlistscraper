from bs4 import BeautifulSoup
from pathlib import Path
import urllib.request
import os
import json

url = 'http://www.heartharena.com/tierlist'

soup = ""
cards = {}

tierfile = './tierlist.json'
tierlist_html = Path(tierfile)

if os.path.isfile(tierfile) and os.stat(tierfile).st_size > 0:
    f = open(tierfile, 'r')
    json_cards_info = f.read()
    cards_info = json.loads(json_cards_info)
else:
    f = open(tierfile, 'w')
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all(class_="card")

    cards_info = {}

    for card in cards:
        if card.dt != None and card.dd != None:
            card_extra = card.dt['class']
            card_name = card.dt.contents[0].strip().lower()
            card_cost = int(card.dd.contents[0].strip())
            cards_info[card_name] = ( card_cost, card_extra )

    f.write(json.dumps(cards_info))

print("\n#### pick these:\n")
for name, value in sorted(cards_info.items(), key=lambda tup: tup[1][0]):
    if value[0] <= 10:
        print(name.ljust(30), value)

print("\n#### absolute garbage (do not touch):\n")
for name, value in sorted(cards_info.items(), key=lambda tup: tup[1][0], reverse=True):
    if value[0] >= 100:
        print(name.ljust(30), value)
