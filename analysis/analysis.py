import collections
import json
import os
import re
import zlib
from base64 import b64encode
from collections import Counter
from common_words import most_common_words
from options import groupedRules
from pprint import pprint

rules = {}


for group in groupedRules:
    # Fills out rules dictionary with the rules in options.py
    rules.update(groupedRules[group])

def make_ruleGroupDefs():
    # Creates ruleGroupDefs.json with all of the rule descriptions in options.py
    i = 0
    ruleGroupDefs = {}

    for group in groupedRules:
        ruleGroup = []
        for rule in groupedRules[group]:
            ruleGroup.append({'title': rule, 'description': groupedRules[group][rule]['description'], 'i': i})
            i += 1
        ruleGroupDefs.update({group: ruleGroup})

    with open('ruleGroupDefs.json', 'w+', encoding='utf-8') as ruleGroupDefsFile:
        json.dump(ruleGroupDefs, ruleGroupDefsFile)

def make_ruleDefs():
    # Creates ruleDefs.json with all of the information in options.py except the regex pattern
    ruleDefs = []
    for rule in rules:
        ruleDefs.append({'title': rule, 'description': rules[rule]['description']})
    with open('ruleDefs.json', 'w+', encoding='utf-8') as ruleDefsFile:
        json.dump(ruleDefs, ruleDefsFile)

def compressDict(blob):
    # Compresses a dictionary
    return b64encode(
        zlib.compress(json.dumps(blob)
                      .encode('utf-8'))
    ).decode('ascii')

def search(text):
    # Searches through text and returns important information
    rule_stats = []
    match_counts = []

    for rule in rules:
        # Find all matches of a rule in the text
        matches = rules[rule]["pattern"].findall(text)

        match_count = len(matches)
        parsed_matches = []
        match_counts.append(match_count)

        parsed_text = text
        for match in matches[:7]:
            # Find the first seven matches in the context of the surrounding text
            t_match = match if type(match) == str else match[0]
            parsed_matches.append(makeContext(parsed_text, t_match))
            parsed_text = parsed_text.partition(t_match)[2]

        rule_stats.append(parsed_matches)
    return rule_stats, match_counts

def makeContext(text, target):
    # Pads a rule match with context around it
    padding = 100
    pre, the_match, post = text.partition(target)
    return (pre[-padding:], the_match, post[0:padding])


def textSearch():
    # Iterates through all downloaded texts, collecting various statistics and information
    all_rules = {}    # Used to count all rule matches for all texts
    text_info = {}    # Used to record metadata for each text

    # Read in json file output.json
    with open("./../collection/output.json", "r", encoding='utf8') as file:
        json_file = json.load(file)

    # For each text, do some processing
    total = len(list(json_file['texts']))
    for c, text_id in enumerate(list(json_file['texts'])):

        print("{}%".format(round(100 * c/total, 2)))
        all_rules[text_id] = {}

        print("Processing Text ID #%s" % text_id)

        text_info[text_id] = {'id': text_id, 'metadata': json_file['texts'][text_id]['metadata'], 'isSect': False, 'lCnt': 0, 'wCnt': 0, 'sCnt': 0}

        # Accesses the source for each text
        file_source = json_file['texts'][text_id]["source"]

        file_stats = {}

        # Process by subsection .txt file
        for file_name in os.listdir("./../collection/%s" % file_source):
            file_number = file_name[:-4]

            # Opens each .txt file in a text_id
            with open("./../collection/{}{}".format(file_source, file_name), "r", encoding='utf8') as text:
                read_text = text.read()

            # Find and count all words
            words = read_text.replace('\"', '').split()
            word_count = len(words)

            letter_count = 0

            # Count number of letters
            for word in words:
                letter_count += len(word)

            # Find number of sentences (by finding ending punctuation)
            sentence_count = len(re.findall(r'[.!?] +', read_text))

            text_info["{}.{}".format(text_id, file_number)] = {'id': "{}.{}".format(text_id, file_number), 'parent': text_id, 'isSect': True, 'sectNumber': file_number, 'lCnt': letter_count, 'wCnt': word_count, 'sCnt': sentence_count}

            text_info[text_id]['lCnt'] = text_info[text_id]['lCnt'] + letter_count
            text_info[text_id]['wCnt'] = text_info[text_id]['wCnt'] + word_count
            text_info[text_id]['sCnt'] = text_info[text_id]['sCnt'] + sentence_count

            # Do rule matching
            rule_stats, rule_match_count = search(read_text)

            # Appends stats to file_stats
            file_stats[file_number] = [letter_count, word_count, sentence_count, rule_stats]

            all_rules[text_id][file_number] = rule_match_count
            if 'whole' not in all_rules[text_id]:
                all_rules[text_id]['whole'] = [0] * len(rules)
            else:
                all_rules[text_id]['whole'] = [w + n for w, n in zip(all_rules[text_id]['whole'], rule_match_count)]

        # Compress file_stats
        frag_text = compressDict(file_stats)

        # Write the file stats in compressed format to a separate subdirectory
        frag_fn = "rules/%s.txt" % int(file_source[10:-1])
        os.makedirs(os.path.dirname(frag_fn), exist_ok=True)
        with open(frag_fn, "w+", encoding='utf8') as frag:
            frag.write(frag_text)

    # Output json file with letter counts, word counts, and sentence counts
    with open("texts_meta.json", "w+", encoding='utf-8') as texts_file:
        json.dump(text_info, texts_file)

    # Output json file with rule counts
    with open("rule_counts.json", "w+", encoding='utf-8') as rules_file:
        json.dump(all_rules, rules_file)

make_ruleDefs()
make_ruleGroupDefs()
textSearch()
