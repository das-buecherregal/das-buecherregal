import csv
import ebooklib
import json
import os
import re
import requests
from bs4 import BeautifulSoup, SoupStrainer
from ebooklib import epub
from ebooklib.utils import parse_html_string
from pprint import pprint

g = {}

with open('../identification/ids.txt', "r", encoding='utf8') as id_file:
	# A few wild regular expressions!
	find_birthdate = re.compile('(?<=birthdate: )[0-9]{4}')
	find_deathdate = re.compile('(?<=deathdate: )[0-9]{4}')

	# For each ID found, attempt to find information like title and author's birthdate
	for id_line in list(id_file):
		g_id = id_line.strip()
		print("Processing Item #{}".format(g_id))

		try:
			book = epub.read_epub('./downloads/{}.epub'.format(g_id))

			title = None
			author = None

			try:
				title = book.get_metadata('DC', 'title')[0][0]
			except:
				print("⮑ WARNING: Title not found for id {}".format(g_id))

			try:
				author = book.get_metadata('DC', 'creator')[0][1]['{http://www.idpf.org/2007/opf}file-as']
			except:
				print("⮑ WARNING: Author not found for id {}".format(g_id))

			things = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)

			path = "./outputs/{}/".format(g_id)
			if not os.path.exists(path):
				os.makedirs(path)

			filelist = [ f for f in os.listdir(path) ]
			for f in filelist:
				os.remove(os.path.join(path, f))

			c = 0

			for i, thing in enumerate(things):
				h = parse_html_string(thing.get_body_content().decode())
				s = "".join(h.itertext())
				p = s.strip().replace("\n\n", "\n").split("\n")
				t = "\n".join(p)
				# Writes a file to the outputs subdirectory
				with open("./outputs/{}/{}.txt".format(g_id, i), "w+", encoding='utf8') as outfile:
					outfile.write(t)
				c += 1

			print("⮑ STATUS: Wrote {} file(s) for this text.".format(c))

			strainer = SoupStrainer('a', href=True)
			soup = BeautifulSoup(requests.get("https://www.gitenberg.org/book/{}".format(g_id)).text, parse_only=strainer, features="lxml")
			link_soup = soup.find(text=' Repository').parent.get('href')
			raw_link = "{}/master/metadata.yaml".format(link_soup.replace("https://github.com", "https://raw.githubusercontent.com"))
			text = requests.get(raw_link).text
			birthdate = re.search(find_birthdate, text)
			deathdate = re.search(find_deathdate, text)

			j = {
				"metadata": {},
				"source": path
			}

			if title != None:
				j['metadata']['title'] = title

			if author != None:
				j['metadata']['author'] = author

			if birthdate != None:
				j['metadata']['birthdate'] = birthdate.group()

			if deathdate != None:
				j['metadata']['deathdate'] = deathdate.group()

			j['metadata']['section_count'] = c

			g[g_id] = j
			print("⮑ DONE!")
		except:
			print("⮑ ERROR: INVALID EPUB!!!")


json_out = {
	"texts": g
}

# Outputs the json file output.json
with open("output.json", "w+", encoding='utf8') as jsonfile:
	jsonfile.write(json.dumps(json_out))
