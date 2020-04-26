#Tags the deck archetype; manual entry

import json
import utils
import db

def formatlist(dlist):
	for card in dlist:
		print(str(card['copies']) + " " + card['name'] + " " + card['board'])

def tagdecks(decklist):
	tags = dict()
	for deck in decklist:
		print(deck['name'] + ": See List? y/n")
		ans = input()
		if ans == 'y':
			formatlist(deck['list'])
		print("Input tags (comma separated)")
		tags_s = input()
		tags_a = [x.strip() for x in tags_s.split(",")]
		tags[deck['name']] = tags_a
	return tags

print("Tags for [m]odern or [l]egacy decks?")
meta = input() 

if meta == "m":
	mdecks = db.getTopModernDecks()
	tags = tagdecks(mdecks)
	with open("data/decktagsm.json" ,"w") as dtf:
		dtf.write(json.dumps(tags))
		dtf.close()
else if meta == "l":
	ldecks = db.getTopLegacyDecks()
	tags = tagdecks(ldecks)
	with open("data/decktagsm.json" ,"w") as dtf:
		dtf.write(json.dumps(tags))
		dtf.close()
else:
	print("Not a format")