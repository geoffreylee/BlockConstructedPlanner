import json
import csv
import db
import utils
import collections

#SHOULDNT I BUILD A CLUMP VISUALIZER? - I DID ACTUALLY DO THIS DELET COMMENT LATER
players = ['Kyle', 'Kevin', 'Brad', 'Jimmy', 'Geoff', 'Justin', 'Andy', 'Andre']
#initializer 
picks_table = dict()
for player in players:
	picks_table[player] = list()

with open("current_picks.txt" ,"r") as pf:
	picks_list = csv.reader(pf, delimiter="\t")
	# populate the data from a hand copied google docs cause i dont have credentials for jimmys api
	i = 0
	for line in picks_list:
		overall_pick = line[1]
		pick_round = line[0]
		player = line[2]
		
		if line[3] == '':
			# The present moment!
			break
		#print(line)
		chosen_set = line[3]
		picks_table[player].append([chosen_set, pick_round, overall_pick])
		i+=1
	pf.close()
with open("sequence_visualizer/js/picks.js", "w") as jsf:
	jsf.write("var picks_table="+json.dumps(picks_table))
	jsf.close()

bviewer = dict()
#print("Who to predict?")

#target_player = input()
players_picks = dict()
#print(picks_table[target_player])
clumpscores = db.getClumpScores()
for target_player in players:

	total_picks = [x[0] for x in picks_table[target_player]]
	players_picks[target_player] = total_picks
	unavailable_picks = list()

	for other_player in players:
		if other_player == target_player:
			continue
		else:
			unavailable_picks = unavailable_picks + [x[0] for x in picks_table[other_player]]
			
	

	legacy_decks = db.getTopLegacyDecks()
	modern_decks = db.getTopModernDecks()

	for deck in legacy_decks:
		deck["format"] = "Legacy"
	for deck in modern_decks:
		deck["format"] = "Modern"

	total_decks = legacy_decks + modern_decks
	cardindex = db.getCardIndex()

	progress_data = dict()
	#print(target_player + "'s Total Picks")
	#print(total_picks)

	for deck in total_decks:
		progress = 0
		total = 0
		sets_needed = dict()
		blocked = 0
		cards_unavailable = list()

		#print("checking " + deck['name'])
		for card in deck['list']:
			total += card['copies']
			# All basics are free but NOT snow basics
			if utils.checkSnowSensitiveBasic(card['name']) == True:
				progress += card['copies']
				continue

			actual_name = card['name']
			eqs = db.equivalentTo(actual_name)
			insets = []
			# If there are equivalences, check them
			for e in eqs:
				insets = insets + cardindex[e]['sets']

			# If its in one of the sets we havfe
			if len(set(total_picks).intersection(insets))!= 0:
				progress += card['copies']
				continue
			# we need the card
			else:
				available = False
				for mtgset in insets:
					if mtgset in unavailable_picks:
						continue
					available = True
					if mtgset not in sets_needed:
						sets_needed[mtgset] = card['copies']
					else:
						sets_needed[mtgset] += card['copies']
				if available == False:
					# only punish blocked mb
					if card['board'] == 'mb':
						blocked += card['copies']
						#print("BLOCKED " + card['name'])
						#print(insets)
					cards_unavailable.append(card)

		#print(deck['format'] + " " + deck['name'] + " progress " + str(progress) + "/" + str(total))
		# Elves.txt trolls us
		#if total < 75:
		#	print(deck['name'] + " is an illegal decklist with " + str(total) + " cards")
		#if total > 75:
		#	print(deck['name'] + " is trolling you with a decklist of " + str(total) + " cards")


		sorted_sets_needed = collections.OrderedDict(sorted(sets_needed.items(), key= lambda mtgset: mtgset[1]*clumpscores[mtgset[0]]['max_clump_score'], reverse=True))
		viewer = dict()
		for x in sorted_sets_needed:
			viewer[x]= sets_needed[x]
		entry = {"progress": progress, "total": total, "percent": float(progress/total), "blocked": blocked, "needed": viewer, "unavailable": cards_unavailable, "format": deck['format'], "list": deck['list']}
		progress_data[deck['name']] = entry


	sorted_progress = collections.OrderedDict(sorted(progress_data.items(), key= lambda deckdata: deckdata[1]['progress'] - deckdata[1]['blocked'], reverse=True))

	jviewer = dict()
	for x in sorted_progress:
		entry = progress_data[x]
		#print(entry["format"] + " " + x.replace(".txt","") +":" + str(entry['progress']) + "/" + str(entry['total']))
		
		jviewer[x] = entry
	bviewer[target_player] = jviewer

with open("sets_visualizer/js/players_picks.js", "w") as ppf:
	ppf.write("var players_picks=" + json.dumps(players_picks))
	ppf.close()

with open("predictions_visualizer/js/players_picks.js", "w") as pdpf:
	pdpf.write("var players_picks=" + json.dumps(players_picks))
	pdpf.close()

with open("predictions_visualizer/js/total_predictions.js", "w") as f:
	f.write("var predictions=" + json.dumps(bviewer))
	f.close()

with open("total_predictions.json", "w") as ff:
	ff.write(json.dumps(bviewer))
	ff.close()























'''


clumpscores = db.getClumpScores()
cardindex = db.getCardIndex()
total_assoc_sets = dict()
# Calculating clumps they have access to













for pick in picks_table[target_player]:
	chosen_set = pick[0]
	pick_round = pick[1]
	overall_pick = pick[2]

	#print(clumpscores[chosen_set]['clumps'])














	for clump in clumpscores[chosen_set]['clumps']:
		assoc_sets = dict()
		progress = dict()
		deckname = clump[1]

		deck = db.findDeck(deckname, "any")
		if deckname not in total_assoc_sets:
			total_assoc_sets[deckname] = dict()

		for card in deck['list']:
			card_sets = cardindex[card['name']]['sets']
			for mtgset in card_sets:
				if mtgset in assoc_sets:
					assoc_sets[mtgset] += 1

				else:
					assoc_sets[mtgset] = 1
			total_assoc_sets[deckname] = {"completion": 0, "progress": progress, "assoc_sets": assoc_sets}




for potentialdeck in total_assoc_sets:

	total_assoc_sets[potentialdeck]['completion'] = 0.0




	


'''