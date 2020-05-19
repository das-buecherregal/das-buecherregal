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

directory = 'downloads/'
path = "./chunks/"

if not os.path.exists(path):
	os.makedirs(path)

# For each downloaded file, tries splitting epub file into chunks 
for filename in os.listdir(directory):
	try:
		book = epub.read_epub("{}{}".format(directory, filename))
		chunks = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)

		title = ""
		author = ""
		id = filename.split(".")[0]
		print("Processing Text #{}".format(id))

		try:
			title = book.get_metadata('DC', 'title')[0][0]
		except:
			title = "Text {}".format(id)
			print("⮑ WARNING: Title not found for id {}".format(g_id))

		try:
			author = book.get_metadata('DC', 'creator')[0][1]['{http://www.idpf.org/2007/opf}file-as']
		except:
			print("⮑ WARNING: Author not found for id {}".format(g_id))

		for i, chunk in enumerate(chunks):
			chunkbook = epub.EpubBook()
			chunkbook.set_identifier("{}.{}".format(id, i + 1))
			chunkbook.set_title("{} - Chunk {}".format(title, i + 1))
			chunkbook.set_language('en')
			chunkbook.add_author(author)
			ch = epub.EpubHtml(title="{} - Chunk {}".format(title, i + 1), file_name='chunk_{}.xhtml'.format(i+1), lang='de')
			ch.content = chunk.content
			chunkbook.add_item(ch)
			chunkbook.add_item(epub.EpubNcx())
			chunkbook.add_item(epub.EpubNav())

			style = 'BODY {color: white;}'
			nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

			# add CSS file
			chunkbook.add_item(nav_css)

			chunkbook.spine = ['nav', ch]

			epub.write_epub("chunks/{}.{}.epub".format(id, i + 1), chunkbook, {})
	except:
		print("Error with {}".format(filename))
