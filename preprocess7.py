# coding=utf-8
import io, os, operator

from pygtrie import PrefixSet

from custom_utils import *

spec_folder = "word_lists"

filename = raw_input("Give file name eg. \"symptoms\" - This script will produce a bucket list file which contains potentially related words for each input word.")
output_file = os.path.join(spec_folder, filename + "_raw_buckets.txt")
abort = raw_input("Press q to abort or any key to continue. Following file will be overwritten: " + output_file)
if abort == 'q':
    raise EnvironmentError

def read_special_words(file_path):
    words = set()
    with io.open(file_path) as file:
        file_contents = [x.strip() for x in file.readlines()]
        for word in file_contents:
            words.add(word)
    return words

def stem_word(word):
    i = len(word)
    if word[:i].endswith('det'):
        i -= 3
    elif word[:i].endswith('et'):
        i -= 2
    elif word[:i].endswith('t'):
        i -= 1
    elif word[:i].endswith('nen'):
        i -= 3
    elif word[:i].endswith('suus'):
        i -= 4
    elif word[:i].endswith('uus'):
        i -= 3
    elif word.endswith('us'):
        i -= 2
    while i >= 1 and word[i - 1] in ('a', 'i', 'o', 'u', 'y', 'e', u'ä', u'ö', u'å'):
        i -= 1
    return word[:max(i,5)] # Dont shorten under 5 characters

def stem_all(raw_set):
    stem_set = set()
    for raw in raw_set:
        stem_set.add(stem_word(raw))
    return stem_set

def starts_with_any(word, words):
    for word2 in words:
        if word == word2 or stem_word(word) == word2:
            continue
        if word.startswith(word2):
            print '            Skipping ' + word + ' because it starts with ' + word2 + ' which we have a separate word for.'
            return True
    return False

def prune_by_startswith(stem_set, raw_set):
    pruned = set()
    for word in raw_set:
        if starts_with_any(word, stem_set):
            continue
        pruned.add(word)
    return pruned

symptoms_raw = read_special_words(os.path.join(spec_folder, filename + ".txt"))
symptoms_stemmed = stem_all(symptoms_raw)
symptoms_pruned = prune_by_startswith(symptoms_stemmed, symptoms_raw)

vocab = {}
with io.open(os.path.join('processed_data', 'vocab_counts.txt'), "r") as f:
    for line in f.readlines():
        splitted = line.split()
        if len(splitted) != 2:
            print 'Skipping erroneous line', line
            continue
        word = splitted[0]
        count = splitted[1]
        vocab[word] = int(count)

sorted_vocab = sorted(vocab.items(), key=operator.itemgetter(1), reverse=True)


duplicate_stems = set()
with io.open(output_file, "w", encoding="utf-8") as f:
    for raw in symptoms_pruned:
        stem = stem_word(raw)

        if stem in duplicate_stems:
            print 'Skipping ' + raw + ' because another previously processed word had the same stem.'
            continue
        duplicate_stems.add(stem)

        auto_choice = False
        print 'Current source word: ' + raw
        f.write('\n' + raw + '\n')
        for tuple in sorted_vocab:
            word = tuple[0]
            word_info = '    ' + word + ' (' + str(vocab[word]) + ') '
            if word.startswith(stem):
                print word_info
                f.write(word + ' ' + str(vocab[word]) + '\n')