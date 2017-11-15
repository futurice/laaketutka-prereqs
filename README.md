# This repo contains prerequisites for Laaketutka backend

Most interesting stuff in this repository is probably the drug and symptom dictionaries in the processed data folder. These files were produced with word_collector.py.

University affiliated researchers can download raw Suomi24 datasets from Kielipankki. If you are a university affiliated researcher, please contact us to get access to preprocessing scripts used with Suomi24 data. Unfortunately we can't release those scripts publicly. If you wish to work with some other dataset and you need help setting up, also contact us! This repo has a mock_data.json file to show roughly what the expected format should be.

The rest of this READme is focused on one thing:

# Expanding drug & symptom vocabularies

Vocabularies are intended to be expanded rarely, in large batches, and the process is somewhat laborious. If there is need to do more frequent updates, many steps here should be automated.

#### Understand what can go wrong

When you add a new word, Nettipuoskari tries to find different abbreviations for that word and put them all in the same basket. For most words this process works just fine, but some words are problematic. Let's declare 2 types of problems:
1. A basket contains words it’s not supposed to have (eg. basket for drug “valine” contains “valinta”, “valitsemismahdollisuudet”, “valikoiminen”, etc.)
2. We may have 2 baskets which should be joined together, but are not (eg. “jomottaa” and “jomotus” may become separate baskets)

This means that some manual testing (reading through baskets etc) should be done after expanding vocabularies. The first kind of errors often show up in “most common” plots, but the second kind of error is more difficult to spot.

#### Understand how to avoid problems

Drug and symptom words are handled in different ways when we group different abbreviations of the same word into baskets. In general, we are merge drug words liberally compared to symptom words, which are merged with a stricter set of rules. As an example, consider words “cac” and “cacao”. If you add “cac” into drug words, then all words which begin with “cac” are merged together (including their respective lemmatized and original forms, including “cacao”). However, if you add “cac” into symptom words, we don’t merge it with all words which begin with “cac”. If “cacao” is found in the data, but not in symptom words, then it’s unlikely that it will be merged with “cac”. This means that type 1 problems often appear with drug words, whereas type 2 problems often appear with symptom words.

Also, in the following cases, consider skipping a word or altering it:
- Is this word ambiguous in its meaning? (eg. “lukko” means “stuck muscle”, but also “physical lock”)
- Is the lemmatization of this word ambiguous (eg. “värinä” almost certainly means “shivers”, but it can technically also mean “as a colour”, so Finnish-dep-parser will unfortunately lemmatize it into “väri” (colour).)
- Will the stemming of this word cause problems? (eg. “valine” is stemmed into “valin”, which will be merged into “valinta”, “valinnat”, etc.)
- Is this word very close to other words which mean different things? (eg. “snri” is close to “ssri”, although they refer to different classes of drugs)

#### How to actually add words

The main files are drugs.txt and symptoms.txt, located in word_lists folder. You can add words manually, with word_collector, or with various preprocessing scripts. These files will be used to create drugs_stemmed.txt and symptoms_three_ways.txt, which are used by the backend.

#### How to add words with word collector

Word_collector takes an input word and uses a word2vec model to suggest words which appear in similar contexts. For example, if you start with baseword "burana", it may suggest many other medicine words to you. You accept/decline words and the accepted words are collected into a vocabulary. They are also used as new basewords to expand the search for new words. When you are seeing poor suggestions for the current "baseword", you can jump to the next baseword.

In order to use word_collector you need a pretrained word2vec model. First, run `json_to_txt` and use its output as input for [word2vec](https://code.google.com/archive/p/word2vec/). Place the model files in "models" directory.

#### How to process vocabulary files after adding words

- Run symptom_stemmer on drugs.txt to create drugs_stemmed.txt
- Run symptom_stemmer on symptoms.txt to create symptoms_stemmed.txt
- Run [Finnish-Dep-Parser](http://turkunlp.github.io/Finnish-dep-parser/) on symptoms.txt to create symptoms_lemmatized.txt: cat symptoms.txt | ./parser_wrapper.sh > symptoms_lemmatized.txt
- Run preprocess5 on symptoms_lemmatized.txt to create symptoms_lemmatized_processed.txt
- Create symptoms_three_ways.txt by combining the following files: symptoms_lemmatized_processed.txt, symptoms.txt, symptoms_stemmed.txt
