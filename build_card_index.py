# Run this last! This combines all the existing database into a large index
import scryfall_api
import db
import utils
import json
import time

card_db = dict()
toplegacycards = db.getTopLegacyCards()
topmoderncards = db.getTopModernCards()
legacydecks = db.getTopLegacyDecks()
moderndecks = db.getTopModernDecks()
legacy_bans = utils.getLegacyBanlist()
modern_bans = utils.getModernBanlist()
bans = utils.getBanlist()
legacy_unbans = [x for x in legacy_bans if x not in bans]
modern_unbans = [x for x in modern_bans if x not in bans]

def createEntry(x):
	query = "!\"" + x + "\""
	api_return = scryfall_api.scryfall(query)
	art = scryfall_api.extract_art(api_return)
	time.sleep(0.11)
	scryfall_sets = scryfall_api.extract_sets(api_return)
	sets = list(scryfall_sets[next(iter(scryfall_sets))])
	return {'sets': sets, 'legacy_decks': list(), 'modern_decks': list(), 'art': art}

OGdualnames = [
	"Scrubland", 
	"Volcanic Island", 
	"Tundra", 
	"Bayou", 
	"Plateau", 
	"Tropical Island", 
	"Underground Sea", 
	"Badlands",
	"Taiga",
	"Savannah"]

for card_data in toplegacycards:
	name = card_data['name'];
	art = card_data['art']
	sets = card_data['sets']
	card_db[name] = {'sets': sets, 'legacy_decks': list(), 'modern_decks': list(), 'art': art}

for card_data in topmoderncards:
	name = card_data['name'];
	art = card_data['art']
	sets = card_data['sets']
	card_db[name] = {'sets': sets, 'legacy_decks': list(), 'modern_decks': list(), 'art': art}

for x in legacy_unbans:
	if x not in card_db:
		card_db[x] = createEntry(x)
for x in modern_unbans:
	if x not in card_db:
		card_db[x] = createEntry(x)

for x in OGdualnames:
	if x not in card_db:
		card_db[x] = createEntry(x)

for deck in legacydecks:
	for card in deck['list']:
		if card['name'] in card_db:
			#ordinary logic
			card_db[card['name']]['legacy_decks'].append(deck['name'])
		else:
			card_db[card['name']] = createEntry(card['name'])
			card_db[card['name']]['legacy_decks'].append(deck['name'])
		
for deck in moderndecks:
	for card in deck['list']:
		if card['name'] in card_db:
			#ordinary logic
			card_db[card['name']]['modern_decks'].append(deck['name'])
		else:
			card_db[card['name']] = createEntry(card['name'])
			card_db[card['name']]['modern_decks'].append(deck['name'])

with open("data/card_index.json", "w") as composite_dbf:
	composite_dbf.write(json.dumps(card_db))
	composite_dbf.close()
with open("sets_visualizer/js/card_index.js", "w") as composite_dbf:
	composite_dbf.write("card_index="+json.dumps(card_db))
	composite_dbf.close()
with open("predictions_visualizer/js/card_index.js", "w") as composite_dbf:
	composite_dbf.write("card_index="+json.dumps(card_db))
	composite_dbf.close()