# This script reads a drug name list from internet_drug_list.txt and checks
# which words actually appear in the vocabulary (from Suomi24 data)
# Outputs to filtered_internet_drug_list.txt
# A small portion of the drugs in our dictionary were added like this

import io, json, os, re
from custom_utils import *

print 'Loading input files....'

path_vocab = os.path.join('processed_data', 'vocab.txt')
path_vocab_stemmed = os.path.join('processed_data', 'vocab_stemmed.txt')
path_raw_list = os.path.join('processed_data', 'internet_drug_list.txt')
path_filtered_list = os.path.join('processed_data', 'filtered_internet_drug_list.txt')

# Read vocabulary into set
vocab = set()
with io.open(path_vocab, 'r') as f:
    for line in f.readlines():
        vocab.add(line.strip())
with io.open(path_vocab_stemmed, 'r') as f:
    for line in f.readlines():
        vocab.add(line.strip())

# Collect a set from internet_drug_list words which appear in vocab
collected = set()
with open(path_raw_list, 'r') as raw:
    for line in raw.readlines():
        for element in re.split(r'\s{2,}', line):
            print element
            # tab separated lines with 3 elements: english, latin and finnish
            if len(element.split()) != 1:
                # skip elements containing expressions of multiple words
                continue
            if len(element) <= 2:
                continue
            if element in vocab:
                print 'adding', element
                collected.add(element)

# Confirm short words from user
collected2 = set()
for word in collected:
    if len(word) < 5:
        if raw_input('Collect short word ' + word + '? Enter y/n: ') == 'n':
            continue
    print 'Adding word ', word
    collected2.add(word)


# Write set to file
with open(path_filtered_list, 'wb') as filtered:
    lines = u'\n'.join(collected2)
    filtered.write(lines.encode('utf-8'))