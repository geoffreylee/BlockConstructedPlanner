import json

with open("rules/legacy_banlist.json", "r") as legacy_banlist_file:
	legacy_banlist = json.load(legacy_banlist_file)
	legacy_banlist_file.close()

with open("rules/banlist.json", "r") as our_banlist_file:
	our_banlist = json.load(our_banlist_file)
	our_banlist_file.close()

with open("rules/modern_banlist.json", "r") as modern_banlist_file:
	modern_banlist = json.load(modern_banlist_file)
	modern_banlist_file.close()

with open("rules/setlist.json", "r") as our_setlist_file:
	our_setlist = json.load(our_setlist_file)
	our_setlist_file.close()

#our_banlist = open()
def getModernBanlist():
	return modern_banlist

def getLegacyBanlist():
	return legacy_banlist

def getBanlist():
	return our_banlist

def getSetlist():
	return our_setlist

def checkLegality(name):
	if name in our_banlist:
		return False
	else:
		return True
def checkSnowSensitiveBasic(name):
	if name == "Mountain": 
		return True
	elif name == "Forest":
		return True
	elif name == "Swamp":
		return True
	elif name == "Island":
		return True
	elif name == "Plains":
		return True
	else:
		return False

def checkBasic(n):
	name = n.replace("Snow-Covered", "").strip()
	if name == "Mountain": 
		return True
	elif name == "Forest":
		return True
	elif name == "Swamp":
		return True
	elif name == "Island":
		return True
	elif name == "Plains":
		return True
	else:
		return False
