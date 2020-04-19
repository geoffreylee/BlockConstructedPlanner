# Caluclate relevancy for each set

# Find which cards are unbanned for us but banned in legacy

import utils
import db
import scryfall_api
import json

def formula(data):
	return (float(data['frequency']) * float(data['copies']))

legacy_bans = utils.getLegacyBanlist()
modern_bans = utils.getModernBanlist()
bans = utils.getBanlist()
legacy_unbans = [x for x in legacy_bans if x not in bans]
modern_unbans = [x for x in modern_bans if x not in bans]

'''print(noteable_unbans)
print("\n\n")

print(modern_unbans)'''

setlist = utils.getSetlist()
setscores = dict()

# initialize scores
for mtgset in setlist:
	setscores[mtgset] = dict({'legacy_unbans' : list(), 'modern_unbans': list(), 'top_cards' : list(), 'modern_score': float(), 'legacy_score': float(), 'score': float()})

for card in legacy_unbans:
	query = "!\"" + card + "\"" 
	api_data = scryfall_api.lookup(query)
	sets = api_data[next(iter(api_data))]

	for mtgset in sets:
		setscores[mtgset]['legacy_unbans'].append(card)

for card in modern_unbans:
	query = "!\"" + card + "\"" 
	api_data = scryfall_api.lookup(query)
	sets = api_data[next(iter(api_data))]

	for mtgset in sets:
		setscores[mtgset]['modern_unbans'].append(card)

top_legacy = db.getTopLegacyCards()
for card in top_legacy:
	if utils.checkLegality(card['name']) == False:
		continue
	for mtgset in card['sets']:
		top_cards = set(setscores[mtgset]['top_cards'])
		top_cards.add(card['name'])
		setscores[mtgset]['top_cards'] = list(top_cards)
		setscores[mtgset]['legacy_score'] += float(formula(card)/len(card['sets']))

top_modern = db.getTopModernCards()
for card in top_modern:
	if utils.checkLegality(card['name']) == False:
		continue
	for mtgset in card['sets']:
		top_cards = set(setscores[mtgset]['top_cards'])
		top_cards.add(card['name'])
		setscores[mtgset]['top_cards'] = list(top_cards)
		setscores[mtgset]['modern_score'] += float(formula(card)/len(card['sets']))



with open("analyses/setscores.json", "w") as outf:
	fmt = json.dumps(setscores)
	outf.write(fmt)
	outf.close()

	




