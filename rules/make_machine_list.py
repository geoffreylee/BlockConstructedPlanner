# All the methods about banned cards
import json

filename = input()
banlist = open(filename)
blist = list()

for line in banlist:
	blist.append(line.strip())

json_fmt = json.dumps(blist)

output = filename.replace(".txt", ".json")
jsonlist = open(output, 'w')
jsonlist.write(json_fmt)
jsonlist.close()
banlist.close()

