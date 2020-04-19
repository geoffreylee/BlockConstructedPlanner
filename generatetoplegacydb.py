import json
import scryfall_api
import time

with open("data/best_legacy_creatures.json", "r") as best_legacy_creatures_file:
	best_legacy_creatures = json.load(best_legacy_creatures_file)
	best_legacy_creatures_file.close()

with open("data/best_legacy_spells.json", "r") as best_legacy_spells_file:
	best_legacy_spells = json.load(best_legacy_spells_file)
	best_legacy_spells_file.close()

with open("data/best_legacy_lands.json", "r") as best_legacy_lands_file:
	best_legacy_lands = json.load(best_legacy_lands_file)
	best_legacy_lands_file.close()

with open("data/best_modern_creatures.json", "r") as best_modern_creatures_file:
	best_modern_creatures = json.load(best_modern_creatures_file)
	best_legacy_creatures_file.close()

with open("data/best_modern_spells.json", "r") as best_modern_spells_file:
	best_modern_spells = json.load(best_modern_spells_file)
	best_modern_spells_file.close()

with open("data/best_modern_lands.json", "r") as best_modern_lands_file:
	best_modern_lands = json.load(best_modern_lands_file)
	best_modern_lands_file.close()

modern_database = list()
legacy_database = list()

for card in best_legacy_creatures:
	query = "!"+"\""+card['name']+"\""
	api_data = scryfall_api.scryfall(query)
	sets_data = scryfall_api.extract_sets(api_data)
	art = scryfall_api.extract_art(api_data)
	'''
				if len(api_data) > 1:
					print("error: ")
					print(api_data)
					print(card)
					break'''

	sets = list(sets_data[next(iter(sets_data))])
	entry = {'name': card['name'], 'frequency': card['frequency'], 'copies': card['copies'], 'sets': list(sets), 'art': art}
	legacy_database.append(entry)
	time.sleep(0.12)

for card in best_legacy_spells:
	query = "!"+"\""+card['name']+"\""
	api_data = scryfall_api.scryfall(query)
	sets_data = scryfall_api.extract_sets(api_data)
	art = scryfall_api.extract_art(api_data)
	'''
				if len(api_data) > 1:
					print("error: ")
					print(api_data)
					print(card)
					break'''

	sets = list(sets_data[next(iter(sets_data))])
	entry = {'name': card['name'], 'frequency': card['frequency'], 'copies': card['copies'], 'sets': list(sets), 'art': art}
	legacy_database.append(entry)
	time.sleep(0.12)

for card in best_legacy_lands:
	query = "!"+"\""+card['name']+"\""
	api_data = scryfall_api.scryfall(query)
	sets_data = scryfall_api.extract_sets(api_data)
	art = scryfall_api.extract_art(api_data)
	
	'''if len(api_data) > 1:
					print("error: ")
					print(api_data)
					print(card)
					break
			'''
	sets = list(sets_data[next(iter(sets_data))])
	entry = {'name': card['name'], 'frequency': card['frequency'], 'copies': card['copies'], 'sets': list(sets), 'art': art}
	legacy_database.append(entry)
	time.sleep(0.11)



legacy_fmt = json.dumps(legacy_database)

with open("data/legacy_database.json", "w") as legacy_db:
	legacy_db.write(legacy_fmt)
	legacy_db.close()
