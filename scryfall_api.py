import json
import urllib.request
import urllib.parse
import ssl
from urllib.error import HTTPError
import utils

ssl._create_default_https_context = ssl._create_unverified_context
def check_set_legality(set_name):
	setlist = set(utils.getSetlist())
	if set_name in utils.getSetlist():
		return True
	else:
		return False

def setImage(set_query):
	raise Exception("Dude why are you doing this now")

def scryfall(q):
	arguments = {"order":"name", "as":"grid", "unique":"prints", "q":q}
	return scryfall_search(arguments)

def extract_sets(data):
	# for each unique card name, list all the sets it appears in
	results = dict()
	for card in data['data']:
		if card['name'] not in results:
			results[card['name']] = set()
			if check_set_legality(card['set_name']) == True:
				results[card['name']].add(card['set_name'])

		elif card['name'] in results:
			if check_set_legality(card['set_name']) == True:
				results[card['name']].add(card['set_name'])
	return results

def extract_art(data):
	card = data['data'][0]
	if card['layout'] == 'transform':
		return card['card_faces'][0]['image_uris']['small']
	else:
		return card['image_uris']['small']

	
def scryfall_search(arguments):
	rooturl = "https://api.scryfall.com/cards/search?"
	url = rooturl + urllib.parse.urlencode(arguments)
	req = urllib.request.Request(url)
	response = urllib.request.urlopen(req).read()
	data = json.loads(response.decode('utf-8'))
	if data['object'] == 'error':
		raise Exception(data['code'], data['details'])
		return data
	elif data['object'] != 'list':
		raise Exception("Unexpected api return type: ", data['object']) 
	elif data['object'] == 'list':
		return data

# JUST USE THE LOWLEVEL ONE PLEASE JESUS

def lookup(card_query):
	args_raw = card_query.split("&&")
	args = [a.strip() for a in args_raw]

	results = dict()
	for card_name in args:
		
		arguments = {"order":"name", "as":"grid", "unique":"prints", "q":card_name}
		data = scryfall_search(arguments)

		# for each unique card name, list all the sets it appears in
		for card in data['data']:
			if card['object'] == 'card': 
				if len(args) > 1 and card['name'].lower().strip() != card_name.lower().strip():
					continue
				
				elif card['name'] not in results:
					results[card['name']] = set()
					if check_set_legality(card['set_name']) == True:
						results[card['name']].add(card['set_name'])

				elif card['name'] in results:
					if check_set_legality(card['set_name']) == True:
						results[card['name']].add(card['set_name'])
	return results

	'''if len(args) == 1:
					for card_name in results:
						print(card_name + " is in: " + ', '.join(results[card_name]))
				
				elif len(args) > 1:
					if len(results) != len(args):
						print("results only found for: ")
						fmt = list()
						for card in results:
							if len(results[card]) != 0:
								fmt.append(card)
						print(", ".join(fmt))
			
					intersection = set(results[next(iter(results))])
					for card in results:
						#print(card)
						#print(intersection)
						intersection = intersection.intersection(results[card])
			
					if len(intersection) == 0:
						print("no results")
					else:
						print(intersection)
			'''
		
'''
while True:
	#print (utils.getSetlist())
	#lookup("ponder")
	print("What card to lookup? ")
	card_name = input()
	print("\n")

	try:
		lookup(card_name)
	except Exception:
		print("Lookup failed.")
	print("\n")


'''