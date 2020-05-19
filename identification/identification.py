import json
import pycurl
import sys
from io import BytesIO
from pprint import pprint

use_bl = False
bl_fp = None

if len(sys.argv) == 3:
	if sys.argv[1] == "blacklist":
		use_bl = True
		bl_fp = sys.argv[2]

# A buffer to handle the recieved info
buffer = BytesIO()

# Create and make the request
c = pycurl.Curl()
# Search for all texts in German
c.setopt(c.URL, "http://localhost:8000/search/language+eq+de")
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

# Get the value from the buffer, transform into dict
response = buffer.getvalue()
data = json.loads(response.decode('iso-8859-1'))

bl = []

if (use_bl):
	with open(bl_fp, 'r', encoding='utf8') as bl_file:
		for line in bl_file.readlines():
			bl.append(line.strip())

ids = list(
		filter(lambda x: not(x in bl),
			map(lambda x: str(x['text_id']), data['texts'])))

with open("ids.txt", "w+", encoding='utf-8') as ids_file:
	ids_file.writelines(ids)
