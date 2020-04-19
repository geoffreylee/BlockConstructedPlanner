import re
import json

filename = input()
file = open(filename)
data = list()
for line in file:
	
	array = line.split('\t')
	name = re.sub(r'\([^)]*\)', '', array[1])
	name = name.strip()
	if name == "Mountain" or name == "Island" or name == "Forest" or name == "Plains" or name == "Swamp":
		continue
	if name == "Snow-Covered Mountain" or name == "Snow-Covered Island" or name == "Snow-Covered Forest" or name == "Snow-Covered Plains" or name == "Snow-Covered Swamp":
		continue
	freq = float(array[2].replace("%",''))/100.0
	copies = float(array[3])

	entry = {'name': name, 'frequency': freq, 'copies': copies}
	data.append(entry)

json_fmt = json.dumps(data)

outputname = filename.replace(".txt", ".json")
with open(outputname, "w") as best_modern_lands:
	best_modern_lands.write(json_fmt)
	best_modern_lands.close()

