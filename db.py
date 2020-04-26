import json

with open("data/legacy_database.json", "r") as legacy_db_f:
	legacy_db = json.load(legacy_db_f)
	legacy_db_f.close()

with open("data/modern_database.json", "r") as modern_db_f:
	modern_db = json.load(modern_db_f)
	modern_db_f.close()

with open("analyses/setscoresdb.json", "r") as setscores_db_f:
	setscores_db = json.load(setscores_db_f)
	setscores_db_f.close()

with open("data/legacydecks/decklist_db.json", "r") as ldecksf:
	legacydecksdb = json.load(ldecksf)
	ldecksf.close()

with open("data/moderndecks/decklist_db.json", "r") as mdecksf:
	moderndecksdb = json.load(mdecksf)
	mdecksf.close()

with open("data/card_index.json", "r") as indexf:
	cardindex = json.load(indexf)
	indexf.close()

with open("analyses/clumpscores_db.json", "r") as clumpf:
	clumpscoresdb = json.load(clumpf)
	clumpf.close()

with open("data/decktagsl.json") as dtlf:
	decktagsl = json.load(dtlf)
	dtlf.close()

with open("data/decktagsm.json") as dtmf:
	decktagsm = json.load(dtmf)
	dtmf.close()

# Programmatically read this maybe
equivalencies_data = [
	{"Scrubland", "Godless Shrine" },
	{"Volcanic Island", "Steam Vents"}, 
	{"Tundra", "Hallowed Fountain"}, 
	{"Bayou", "Overgrown Tomb"}, 
	{"Plateau", "Sacred Foundry"}, 
	{"Tropical Island", "Breeding Pool"},
	{"Tundra", "Hallowed Fountain"}, 
	{"Underground Sea", "Watery Grave"},
	{"Badlands", "Blood Crypt"},
	{"Taiga", "Stomping Ground"},
	{"Savannah", "Temple Garden"},
	{"Swords to Plowshares", "Path to Exile"},
	{"Preordain", "Serum Visions"},
	{"Grafdigger's Cage", "Relic of Progenitus", "Surgical Extraction", "Leyline of the Void", "Rest in Peace"}
]


# Due to to the nature of the format we must consider certain things to be equivalent
# because its impossible to get the best version of everything
def checkEquivalence(namea, nameb):
	for equivalences in equivalencies_data:
		if (namea in equivalences) and (nameb in equivalences):
			return True
	return False

def equivalentTo(name):
	data = getTotalEquivalences()
	for equivalence in data:
		if name in equivalence:
			#print(equivalence)
			#equivalence.remove(name)
			return equivalence
	return {name}

def getTotalEquivalences():
	return equivalencies_data

def getDeckTags(fmt):
	if fmt == "legacy":
		return decktagsl
	if fmt == "modern":
		return decktagsm
	if fmt == "all":
		decktagsl.update(decktagsm)
		return decktagsl

def getCardIndex():
	return cardindex
	
def findTopCard(name):
	for card in legacy_db:
		if card['name'] == name:
			return card
	for card in modern_db:
		if card['name'] == name:
			return card
	return 0

def findDeck(name, fmt):
	if fmt == 'modern':
		for deck in moderndecksdb:
			if deck['name'] == name:
				return deck
		return 0
	if fmt == 'legacy':
		for deck in legacydecksdb:
			if deck['name'] == name:
				return deck
		return 0
	if fmt == 'any':
		for deck in moderndecksdb:
			if deck['name'] == name:
				return deck
		for deck in legacydecksdb:
			if deck['name'] == name:
				return deck
		return 0
	return 0

def getClumpScores():
	return clumpscoresdb

def getTopModernDecks():
	return moderndecksdb

def getTopLegacyDecks():
	return legacydecksdb

def getTopLegacyCards():
	return legacy_db

def getTopModernCards():
	return modern_db

def getSetsData():
	return setscores_db