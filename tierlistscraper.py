from bs4 import BeautifulSoup
from pathlib import Path
import urllib.request
import os
import json

url = 'http://www.heartharena.com/tierlist'

soup = ""

tierfile = './tierlist.json'
tierlist_html = Path(tierfile)

if os.path.isfile(tierfile) and os.stat(tierfile).st_size > 0:
    f = open(tierfile, 'r')
    json_card_values = f.read()
    card_values = json.loads(json_card_values)
else:
    f = open(tierfile, 'w')
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all(class_="card")

    card_values = {}

    for card in cards:
        if card.dt != None and card.dd != None:
            card_name = card.dt.contents[0].strip().lower()
            card_cost = int(card.dd.contents[0].strip())
            card_values[card_name] = card_cost

    f.write(json.dumps(card_values))

print("\n#### pick these:\n")
for name, value in sorted(card_values.items(), key=lambda tup: tup[1]):
    if value <= 10:
        print(name, value)

print("\n#### absolute garbage (do not touch):\n")
for name, value in sorted(card_values.items(), key=lambda tup: tup[1], reverse=True):
    if value >= 100:
        print(name, '\t', value)
