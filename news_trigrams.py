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

new_trigrams = pickle.load(open("new_trigrams.p", "rb"))
all_keys = set()
for i in range(108,115):
    all_keys = all_keys | set(new_trigrams[i].keys())

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
    trigrams = [trigram for trigram in ngrams(tokens,3) if trigram in all_keys]
    return trigrams

# for source in ("nypost", "nymag", "motherjones", "dkos", "townhall", "breitbart"):
for source in ("townhall", "breitbart"):
    print("Loading", source)
    file = open('news/' + source + '/' + source + '_data.json', 'r')
    articles = json.load(file)
    file.close()

    trigram_articles = []
    for article in articles:
        if len(trigram_articles) % 1000 == 0:
            print(len(trigram_articles))
        trigram_article = article.copy()
        text = trigram_article.pop('text')
        trigrams = preprocess(text)
        trigram_article['trigram'] = trigrams
        trigram_articles.append(trigram_article)

    print("Writing", source)
    pickle.dump(trigram_articles, open(source + "_trigrams_new.p", "wb"))