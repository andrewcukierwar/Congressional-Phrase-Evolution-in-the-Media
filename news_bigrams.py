from nltk import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.util import ngrams
import string
import re
import json
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

new_bigrams = pickle.load(open("new_bigrams.p", "rb"))
all_keys = set()
for i in range(108,115):
    all_keys = all_keys | set(new_bigrams[i].keys())

stemmer = SnowballStemmer("english")

def preprocess(text):
    text = text.encode("ascii", "ignore") # remove all non-ascii characters
    text = text.decode("ascii")
    text = text.rstrip().lower()
    text = text.replace('\n', ' ').replace('\t', ' ')
    text = text.replace('-', '').replace('\'', '') # delete hyphens and apostrophes
    text = re.sub('[' + string.punctuation + ']', ' ', text) # replace other punctuation with spaces
    tokens = word_tokenize(text) # convert text to tokens
    tokens = [str(stemmer.stem(word)) for word in tokens if word not in stopword_set] # stem using Porter2
    bigrams = []
    for bigram in ngrams(tokens,2):
        # # ignore procedural bigrams and purely numerical bigrams
        # if bigram in procedural or bigram[0].isdigit() and bigram[1].isdigit():
        #     continue
        if bigram in all_keys:
            bigrams.append(bigram)
    return bigrams

for source in ("nypost", "nymag", "motherjones", "dkos", "townhall", "breitbart"):
    print("Loading", source)
    file = open(source + '_data.json', 'r')
    articles = json.load(file)
    file.close()

    bigram_articles = []
    for article in articles:
        if len(bigram_articles) % 1000 == 0:
            print(len(bigram_articles))
        bigram_article = article.copy()
        text = bigram_article.pop('text')
        bigrams = preprocess(text)
        bigram_article['bigram'] = bigrams
        bigram_articles.append(bigram_article)

    print("Writing", source)
    pickle.dump(bigram_articles, open(source + "_bigrams_new.p", "wb"))