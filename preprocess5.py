'''
Input: a file produced by Turku NLP Stemmer, such as:
    1   This    This   SUBJECT NOUN    CASE ...
    2   is      is    ADV     -       ...
    3   a       a      ...
    4   posting post
    ...         ^^ Stemmed words
Output: a file with stemmed words only, in this format:
    This is a post
    I hate ice cream. And also hate hamburger.
    ...
Instructions for Turku NLP parser: cat input_raw.txt | ./parser_wrapper.sh > input_turku.txt
'''

import os
from custom_utils import *

file_name = raw_input("Give filename: ")
input_turku = os.path.join('labeled_data', file_name + '.txt')
output_file = os.path.join('labeled_data', file_name + '_processed.txt')

print 'This will overwrite ', output_file
user_action = raw_input('Press q to quit or any key to continue.')
if user_action == 'q':
    raise EnvironmentError

with open(input_turku, 'r') as infile:
    raw = [x.strip() for x in infile.readlines()]


with open(output_file, "w") as outfile:
    for line in raw:
        if len(line.strip()) == 0:
            outfile.write('\r\n')
            continue
        tokens = line.split('\t')
        if len(tokens) < 3:
            out('Error parsing line ', line)
        else:
            if len(tokens[2].strip()) == 0:
                out('Error parsing line ', line)
            outfile.write(tokens[2].replace('#', '') + ' ')

