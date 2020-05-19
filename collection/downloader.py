import requests

# For each German text found, download the epub and write it to downloads subdirectory
with open("./../identification/ids.txt", "r", encoding='utf8') as id_file:
	for id_line in id_file:
		g_id = id_line.strip()
		url = "https://www.gutenberg.org/ebooks/{}.epub.images".format(g_id)

		print('Requesting ebook #{}'.format(g_id), end='... ')
		r = requests.get(url)

		with open('./downloads/{}.epub'.format(g_id), 'wb') as f:
			f.write(r.content)

		# Retrieve HTTP metadata
		print("Server responded with status {}".format(r.status_code), end='... ')
		print("Done.")
