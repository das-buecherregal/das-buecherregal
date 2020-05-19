import re
import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(requests.get("https://1000mostcommonwords.com/1000-most-common-german-words").text, features="lxml")
most_common_words = list()
clean = re.compile('<.*?>')

# Creates list of 1000 most common words in German from the above website
for tr in soup.findAll('table')[0].findAll('tr'):
  most_common_words.append(re.sub(clean, '', str(tr.findAll('td')[1])))

most_common_words.remove('German')
