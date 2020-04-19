import db 
import json
import utils
import sys
sys.setrecursionlimit(10**5)

cards = db.getCardIndex()
setscores = db.getSetsData()


def intersector(sheaf, deck, families, family, fmt):
	for c in deck['list']:
		if utils.checkBasic(c['name']) == True:
			continue
		if c['name'] in family:
			continue
		#how many of these other cards come from the same set? whats the maximum size
		#find largest intersection		
		else:
			d_sheaf = set(cards[c['name']]['sets']).intersection(sheaf)
			if len(d_sheaf) > 0:
				sheaf = d_sheaf
				return intersector(sheaf, deck, families, family+[c['name']],fmt)
	#If we finish iterating we found the longest chain
	#DO NOT LIST SINGLETONS
	if len(family) > 1:
		families.append([list(sheaf),family,deck['name'],fmt])
	return

for mtgset in setscores:
	setscores[mtgset]['clumps'] = list()

#GIVEN CARD IS IN THE DECK, HOW MANY TIMES DO OTHER CARDS FROM THE SAME SET APPEAR
init = list()
for card in cards:
	#print("card index :" + card)
	if utils.checkBasic(card) == True:
		continue

	for mdeck in cards[card]['modern_decks']:
		sheaf = set(cards[card]['sets'])
		#print(sheaf)
		#print(sheaf)
		family = list()
		family.append(card)
		#For any given modern deck with this card, how many cards from other sets show up and how often
		data = db.findDeck(mdeck, "modern") 
		intersector(sheaf, dict(data), init, family, "modern")


	for ldeck in cards[card]['legacy_decks']:
		sheaf = set(cards[card]['sets'])
		family = list()
		family.append(card)
		#For any given modern deck with this card, how many cards from other sets show up and how often
		data = db.findDeck(ldeck, "legacy") 

		intersector(sheaf, dict(data), init, family, "legacy")

	for entry in init:
		#entry = [sheaf, family, deckname]
		#entry[2]=entry[2].replace(".txt","")
		for mtgset in entry[0]:
			skip = False
			#only append new pairs tho
			for clump in setscores[mtgset]['clumps']:
				if set(clump[0])==set(entry[1]) and entry[2] == clump[1] and entry[3]==clump[2]:
					skip = True
			
			if skip == False:
				setscores[mtgset]['clumps'].append([entry[1],entry[2], entry[3]])

with open("analyses/setclumpscores.json", "w") as sf:
	sf.write(json.dumps(setscores))
	sf.close()




