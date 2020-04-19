import json
import collections
legacy_overweight = 1.0

def calculate_score(legacy,modern):
	return (1.7*legacy + modern)

def assign_score(lambda_mtgset):
	lambda_mtgset[1]['score']=calculate_score(lambda_mtgset[1]['legacy_score'], lambda_mtgset[1]['modern_score'])
	return lambda_mtgset[1]['score']

with open('setscores.json','r') as results:
	setscores = json.load(results)
	results.close()

# Sort setscores by formula
#print(setscores.items())
#exit()
leaderboards = collections.OrderedDict(
	sorted(setscores.items(), key=lambda mtgset: assign_score(mtgset), reverse=True))

viewer = list()
i = 0
for x in leaderboards:
	setscores[x]['rank'] = i
	if setscores[x]['score'] == 0 and len(setscores[x]['legacy_unbans']) == 0 and len(setscores[x]['modern_unbans'])==0:
		continue
	viewer.append((x, setscores[x])) 
	i += 1

with open("sorted.json", "w") as output:
	fmt = json.dumps(viewer)
	output.write(fmt)
	output.close()

with open("setscoresdb.json", "w") as db:
	dbfmt = json.dumps(setscores)
	db.write(dbfmt)
	db.close()