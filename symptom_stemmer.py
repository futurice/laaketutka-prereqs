# coding=utf-8
# This file produces ad hoc stemming for a list of words. Intended for symptom stemming.
import os
import io
from custom_utils import *

file_name = raw_input('Give filename: ')
input_file_path = os.path.join('word_lists', file_name + '.txt')
output_file_path = os.path.join('word_lists', file_name + '_stemmed.txt')

strip_dashes = raw_input('Strip dash (-) characters? Enter y/n: ')

print 'Reading from ' + input_file_path + " and overwriting " + output_file_path
user_action = raw_input('Press q to abort or any key to continue: ')
if user_action == 'q':
    raise EnvironmentError


with io.open(input_file_path, "r", encoding="utf-8") as f:
    raw = [x.strip() for x in f.readlines()]

stems = set()
for raw_symptom in raw:
    symptom = raw_symptom
    if strip_dashes:
        symptom = symptom.replace('-', '')
    i = len(symptom)
    if symptom[:i].endswith('det'):
        i -= 3
    elif symptom[:i].endswith('et'):
        i -= 2
    elif symptom[:i].endswith('t'):
        i -= 1
    elif symptom[:i].endswith('nen'):
        i -= 3
    elif symptom[:i].endswith('suus'):
        i -= 4
    elif symptom[:i].endswith('uus'):
        i -= 3
    elif symptom.endswith('us'):
        i -= 2
    while i >= 1 and symptom[i-1] in ('a', 'i', 'o', 'u', 'y', 'e', u'ä', u'ö', u'å'):
        i -= 1
    symptom = symptom[:max(i,6)] # Dont shorten under 6 characters
    stems.add(symptom)
    print 'Stemmed ', raw_symptom, ' -> ', symptom

with open(output_file_path, "w") as f:
    for stem in stems:
        f.write(stem.encode('utf-8') + "\r\n")