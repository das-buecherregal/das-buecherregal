import json
import os
from collections import Counter
from nltk.corpus import stopwords

# the ints returned by ord() for ['a', 'd', 'g', 'j', 'm', 'p', 's', 'v', 'y']
starts = [97, 100, 103, 106, 109, 112, 115, 118, 121]
# the ints returned by ord() for ['c', 'f', 'i', 'l', 'o', 'r', 'u', 'x', 'ü']
stops = [99, 102, 105, 108, 111, 114, 117, 120, 252]

# Loops through each pair of start and stop points, such that a-c is considered,
# then d-f is considered, then g-i is considered, and so on...
for start, stop in zip(starts, stops):
    words = dict()

    # Looping through each json file in words subdirectory
    for text_id in os.listdir("./../analysis/words"):
        with open("./../analysis/words/%s" % text_id, "r", encoding='utf8') as json_file:
            f = json.load(json_file)

            print("Tallying words from %s" % text_id)

            # Tallies word counts and in which section/subsection the word can be found
            for section in f:
                for word in f[section]:
                    word.lower()
                    if word not in stopwords.words('german') and start <= ord(word[:1]) and ord(word[:1]) <= stop:
                        if word not in words:
                            words[word] = list()
                        if "{}.whole".format(text_id) not in words[word]:
                            words[word].append("{}.whole".format(text_id))
                        words[word].append("{}.{}".format(text_id, section))

    # Outputs json files of word counts to subdirectory wordcounts
    os.makedirs('wordcounts', exist_ok=True))
    with open("wordcounts{}.json".format(start), "w+", encoding='utf8') as words_file:
        json.dump(words, words_file)
