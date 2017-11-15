# -*- coding: utf-8 -*-
# This script is for collecting related words into dictionaries.
# For example, you can start with 'ibuprofeeni' and it will suggest
# words which appear in similar contexts. You accept/decline
# suggested words and the words you accept will be used to widen
# the search as well. There are some things to reduce manual
# labor (for example, skipped words are not suggested again).

import matplotlib.pyplot as plt
import os
from gensim.models import Word2Vec
from collections import deque
from pygtrie import PrefixSet

fname = 'models/word2vecmodel'
if os.path.isfile(fname):
    print 'Reading model from disk...'
    model = Word2Vec.load(fname)
else:
    raise Exception('No model found from ' + fname + '. This script expects a word2vec model to have been previously created.')



def compare(a, b):
    return model.wv.vocab[b].count - model.wv.vocab[a].count

def sort_by_freq(res):
    return sorted(res, cmp=compare)

class SkipWords(object):
    # This class exists because we don't want to treat short words as wildcards.
    # As we skip words, long words are used as wildcards, short words are used as is.
    def __init__(self):
        self.exact = set()
        self.prefix = PrefixSet()

    def add(self, word):
        if len(word) < 7:
            self.exact.add(word)
        else:
            self.prefix.add(word)

    def __contains__(self, word):
        return word in self.exact or word in self.prefix

print 'Running word collector'
collectedSymptoms = PrefixSet()
skipWords = SkipWords()
basewords = deque()
directory = 'word_lists'
if not os.path.exists(directory):
    os.makedirs(directory)
filename = raw_input('Using directory ' + directory + '. Please enter filename. If it exists, it will be loaded into memory: ')
if filename.endswith('.txt'):
    filename = filename[:-4]

# We will save 3 files: main file with collected words, skipwords and unspent basewords for future searches.
acc_path = os.path.join(directory, filename + '.txt')
skip_path = os.path.join(directory, filename + '_skipWords.txt')
basew_path = os.path.join(directory, filename + '_baseWords.txt')

# Try to load previously created files
if os.path.isfile(acc_path):

    # Gather previously collected words from the main file
    with open(acc_path, 'r') as f:
        file_contents = [x.strip() for x in f.readlines()]
    for line in file_contents:
        collectedSymptoms.add(line)
        skipWords.add(line) # For backwards compatibility

    # Gather skipwords from the skipwords file
    if os.path.isfile(skip_path):
        with open(skip_path, 'r') as f:
            file_contents = [x.strip() for x in f.readlines()]
        for line in file_contents:
            skipWords.add(line)
        print('Succesfully read skipwords list from ' + skip_path)
    else:
        print('Couldn\'t find skipwords file ' + skip_path)
        print('Proceeding with an empty skipwords list...')

    # Gather unspent basewords from the basewords file
    if os.path.isfile(basew_path):
        with open(basew_path, 'r') as f:
            file_contents = [x.strip() for x in f.readlines()]
        for line in file_contents:
            basewords.append(line)
        print('Succesfully read unspent basewords from ' + basew_path)
    else:
        print('Couldn\'t find basewords file ' + basew_path)

if not basewords:
    baseword = raw_input('Please enter first baseword: ')
    basewords.append(baseword)
    collectedSymptoms.add(baseword)
    skipWords.add(baseword)

# The actual work
with open(acc_path, 'a') as accFile, open(skip_path, 'a') as skipFile, open(basew_path, 'w') as basewFile:
    try:
        while True:

            # Search for words which are found in similar contexts as the first word in basewords
            maxhits = 600
            try:
                results = map(lambda x: x[0], model.most_similar(basewords[0], topn=maxhits))
                results = sort_by_freq(results)
            except KeyError:
                print 'Baseword not found', basewords[0]
                basewords.popleft()
                print 'Using baseword ', basewords[0]
                continue

            # Iterate results, ask user to accept/skip each word.
            for i in range(maxhits):
                if results[i] in skipWords or results[i] in collectedSymptoms:
                    continue
                skipWords.add(results[i])
                skipFile.write(results[i] + '\r\n')
                skipFile.flush()
                print results[i], '(' + str(model.wv.vocab[results[i]].count) + ') <<< Enter 1 to accept word, 2 to skip word, 3 to jump to next baseword (current baseword', basewords[0], '), q to quit'
                command = raw_input()
                if command == '1':
                    collectedSymptoms.add(results[i])
                    accFile.write(results[i] + '\r\n')
                    accFile.flush()
                    basewords.append(results[i])
                elif command == '2':
                    continue
                elif command == '3':
                    break
                elif command == 'q':
                    raise ValueError('Exiting')
            basewords.popleft()
            print 'Using baseword ', basewords[0]

    finally:
        # Write unspent basewords to file
        for baseword in basewords:
            basewFile.write(baseword + '\r\n')
        basewFile.flush()