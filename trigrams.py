from collections import defaultdict
from nltk import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.util import ngrams
import string
import re
import pickle

stopword_set = set()
file = open("stop.txt", 'r')
for line in file.readlines():
    word = line[:line.find('|')] if '|' in line else line
    word = word.strip()
    if len(word) > 0:
        stopword_set.add(word)
file.close()

procedural = set()
file = open("vocabulary/procedural.txt", 'r')
next(file)
for line in file.readlines():
    phrase = line[:line.find('|')] if '|' in line else line
    word1, word2 = phrase.split(" ")
    trigram = (word1, word2)
    procedural.add(trigram)
file.close()

all_speeches = pickle.load(open("speeches.p", "rb"))
stemmer = SnowballStemmer("english")
trigrams_dict = {}
for i in range(106,115):
    speeches = all_speeches[i]
    trigrams = defaultdict(list)
    file_speeches = open("hein-daily/speeches_" + str(i) + ".txt", 'rb')
    next(file_speeches)
    for line in file_speeches.readlines():
        arr = line.decode("ascii", "ignore").split("|")
        speech_id = arr[0]
        if speech_id in speeches:
            text = arr[1].rstrip().lower()
            text = text.replace('-', '').replace('\'', '') # delete hyphens and apostrophes
            text = re.sub('[' + string.punctuation + ']', ' ', text) # replace other punctuation with spaces
            text = re.sub("\([^)]*\)", ' ', text) # replace non-spoken parenthetical insertions
            tokens = word_tokenize(text)
            tokens = [str(stemmer.stem(word)) for word in tokens if word not in stopword_set] # stem using Porter2
            for trigram in ngrams(tokens,3):
                # ignore procedural trigrams and purely numerical trigrams
                if trigram[0].isdigit() and trigram[1].isdigit() and trigram[2].isdigit():
                    continue
                if trigram[:-1] in procedural or trigram[1:] in procedural:
                    continue
                trigrams[trigram].append(speech_id)
    file_speeches.close()
    trigrams = {k: v for k, v in trigrams.items() if len(v) >= 10} # remove trigrams that occur less than 10 times
    trigrams_dict[i] = trigrams

pickle.dump(trigrams_dict, open("trigrams.p", "wb"))