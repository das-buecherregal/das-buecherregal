import json
import re
import requests
from bs4 import BeautifulSoup

def getAuthorUrl(id):
	# Finds internal link to author information within the Project Gutenberg website
	text_url = "http://www.gutenberg.org/ebooks/{}".format(id)
	r = requests.get(text_url)
	soup = BeautifulSoup(r.text, features="lxml")
	res = soup.findAll("a", {"title" : "Find more ebooks by the same author."})
	if len(res) == 0:
		return None
	return "http://www.gutenberg.org{}".format(res[0]['href'])

def getAuthorWikipedias(id):
	# Finds the link to an author's Wikipedia page, if available, prioritizing the
	# author's German wikipedia page
	author_url = getAuthorUrl(id)
	if author_url == None:
		return None
	r = requests.get(author_url)
	soup = BeautifulSoup(r.text, features="lxml")
	de = soup.findAll("a", {"href" : re.compile(r'.*de\.wikipedia.*')})
	en = soup.findAll("a", {"href" : re.compile(r'.*en\.wikipedia.*')})
	if (len(de) + len(en) == 0):
		return None
	out = {}
	if len(de) > 0:
		out['de'] = de[0]['href']
	if len(en) > 0:
			out['en'] = en[0]['href']
	return out

# List of all available Wikipedia pages
master = {}

with open("./../identification/ids.txt", 'r') as ids_file:
	# Attempts to find each author's Wikipedia page
	for id_r in list(ids_file):
		id = id_r[:-1]
		master[id] = getAuthorWikipedias(id)
		print("{} {}".format(id, master[id]))

with open("wikipedia.json", "w+", encoding='utf-8') as out_file:
	# Outputs wikipedia.json file
	json.dump(master, out_file)
