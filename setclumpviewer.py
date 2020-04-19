import json
import db
import collections
import math
import statistics
import time
import matplotlib 
import matplotlib.pyplot as plt

matplotlib.interactive(True)

cardindex = db.getCardIndex()
setscores = db.getSetsData()
maximum_contribution_array = list()

def maximumContribution(lambda_mtgset):
	clumps = lambda_mtgset[1]['clumps']
	maximum_contribution = 0.0
	for clump in clumps:
		deckname = clump[1]
		RELfmt = clump[2]
		deck = db.findDeck(deckname, RELfmt)
		family = clump[0]

		weighted_contribution = 0.0
		highest_frequency = 0.0

		for card in family:
			for c in deck['list']:
				if c['name'] == card:
					actual_name = c['name']
					eqs = db.equivalentTo(actual_name)
					insets = []
					for e in eqs:
						insets = insets + cardindex[e]['sets']
					dilution = len(set(insets))
					weighted_contribution += float(c['copies']/dilution)
		
			top_card_data = db.findTopCard(card)
			#dont count table top casual clumps
			if top_card_data != 0:
				if top_card_data['frequency'] > highest_frequency:
					highest_frequency = top_card_data['frequency']


		weighted_contribution *= len(family)
		weighted_contribution *= highest_frequency
		
		if RELfmt == "legacy":
			weighted_contribution *= 2
		if weighted_contribution >= maximum_contribution:
			maximum_contribution = weighted_contribution
		clump.append(weighted_contribution)
	lambda_mtgset[1]['max_clump_score'] = maximum_contribution

	# Jerry rigged statistical function before the return statement

	maximum_contribution_array.append(maximum_contribution)
	return maximum_contribution



with open("analyses/setclumpscores.json", "r") as clumpscoresf:
	clumpscores = json.load(clumpscoresf)
	clumpscoresf.close()

sortedscores = collections.OrderedDict(sorted(clumpscores.items(), key=lambda mtgset: maximumContribution(mtgset), reverse=True))
mean = statistics.mean(maximum_contribution_array)
sigma = statistics.stdev(maximum_contribution_array)

fig, ax = plt.subplots()
ax.plot([x for x in sortedscores], [clumpscores[y]['max_clump_score'] for y in sortedscores])
fig.savefig("set_strengths.png")

normal, ax = plt.subplots()
ax.hist([clumpscores[y]['max_clump_score'] for y in sortedscores], bins = 50, density = True)
normal.savefig("normal_curve.png")

print("rendered")
#time.sleep(100)

with open("sets_visualizer/js/stats.js", "w") as sf:
	sf.write("var mean=" + str(mean) + "; var std=" + str(sigma)+";")
	sf.close()
print("mean: " + str(mean))
print("stdev: " + str(sigma))

viewer = list()
i = 0
for x in sortedscores:
	clumpscores[x]['clump_rank'] = i
	'''if setscores[x]['score'] == 0 and len(setscores[x]['legacy_unbans']) == 0 and len(setscores[x]['modern_unbans'])==0:
					continue'''	
	viewer.append((x, clumpscores[x])) 
	i += 1

with open("analyses/clumpscores_sorted.json" , "w") as f:
	f.write(json.dumps(viewer))
	f.close()
with open("sets_visualizer/js/clumpscores_sorted.js" , "w") as ff:
	ff.write("sorted_sets="+ json.dumps(viewer));
	ff.close()

with open("analyses/clumpscores_db.json", "w") as g:
	g.write(json.dumps(clumpscores))
	g.close()

with open("sets_visualizer/js/clumpscores_db.js", "w") as dbjs:
	dbjs.write("clumpscores_db=" + json.dumps(clumpscores))
	dbjs.close()

