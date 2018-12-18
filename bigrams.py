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
    bigram = (word1, word2)
    procedural.add(bigram)
file.close()

all_speeches = pickle.load(open("speeches.p", "rb"))
stemmer = SnowballStemmer("english")
bigrams_dict = {}
for i in range(106,115):
    speeches = all_speeches[i]
    bigrams = defaultdict(list)
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
            for bigram in ngrams(tokens,2):
                # ignore procedural bigrams and purely numerical bigrams
                if bigram in procedural or bigram[0].isdigit() and bigram[1].isdigit():
                    continue
                bigrams[bigram].append(speech_id)
    file_speeches.close()
    bigrams = {k: v for k, v in bigrams.items() if len(v) >= 10} # remove bigrams that occur less than 10 times
    bigrams_dict[i] = bigrams

pickle.dump(bigrams_dict, open("bigrams.p", "wb"))