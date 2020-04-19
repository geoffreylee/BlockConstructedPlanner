import os
import re
import json

decklist_db = list()
card_index = list()

# THE GOAL HERE IS TO CALCULATE "CLUMP PLAYABILITY" OF CARDS IE CARDS THAT GO TOGETHER IN THE SAME SET 
# JSONify all the decklists first
print("decklist directory: ")
directory = input()
for filename in os.listdir(directory):
	if filename.endswith(".txt"):
		print(filename)

		deckname = filename.replace("Deck - ", "")
		with open(directory + "/" + filename, "r") as rawdecklist:
			board = "mb"
			decklist = list()
			for line in rawdecklist:
				#sideboard
				if line == "\n":
					board = "sb"
					continue
			
				parse = re.search('([^ ]+)', line)
				copies = int(parse.group(0))
				cardname = (line.replace(str(copies), "")).strip()
				entry = {'name': cardname, 'copies': copies, 'board': board}
				decklist.append(entry)

			decklist_db.append({'name': deckname, 'list': decklist})

with open(directory+"/decklist_db.json", "w") as dbf:
	dbf.write(json.dumps(decklist_db))
	dbf.close()





				





