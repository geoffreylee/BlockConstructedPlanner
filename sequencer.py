import re
import ssl
import json
import utils
import scryfall_api
import collections
import time
import db
from urllib.error import HTTPError
ssl._create_default_https_context = ssl._create_unverified_context

# Prints the sequenec of picks

# Parse the list first
decklist = list() 
setlist = utils.getSetlist()
setcontribution = dict()

# initialize
for mtgset in setlist:
	setcontribution[mtgset] = {'total_cards': 0, 'weighted_total_cards': 0, 'relevant_cards': list()}


deckdictionary = dict()
with open("decklist.txt") as deckf:
	for line in deckf:
		parse = re.search('([^ ]+)', line)
		copies = int(parse.group(0))
		cardname = (line.replace(str(copies)+" ", "")).strip()
		decklist.append({'name': cardname, 'copies': copies})
		deckdictionary[cardname] = copies
	deckf.close()
with open("sequence_visualizer/js/decklist.js", "w") as dlf:
	dlf.write("var decklist="+json.dumps(deckdictionary))
	dlf.close() 
#print (decklist)
clumpscores = db.getClumpScores()
for card in decklist:
	if utils.checkBasic(card['name']):
		continue
	query = "!\"" + card['name'] + "\""
	try:
		api_return = scryfall_api.lookup(query)
	except HTTPError:
		print(card['name'])
		print('failed')
		continue
	sets = api_return[next(iter(api_return))]
	redundancy = len(sets)


	for mtgset in sets:
		setcontribution[mtgset]['relevant_cards'].append([card['name'],redundancy])
		setcontribution[mtgset]['total_cards'] += card['copies']
		setcontribution[mtgset]['weighted_total_cards'] += float(card['copies']/redundancy)


for x in setcontribution:
	setcontribution[x]['adjusted_score']=setcontribution[x]['weighted_total_cards']*clumpscores[x]['max_clump_score']
	setcontribution[x]['max_clump_score'] = clumpscores[x]['max_clump_score']

sequence = collections.OrderedDict(sorted(setcontribution.items(), key=lambda mtgset: mtgset[1]['adjusted_score'], reverse=True))

viewer = list()
for x in sequence:
	if setcontribution[x]['total_cards'] == 0:
		continue
	viewer.append([x, setcontribution[x]])
fmt = json.dumps(viewer)

with open("sequence_visualizer/js/deck_sequence.js","w") as seqf:
	seqf.write("var deck_sequence="+fmt)
	seqf.close()




