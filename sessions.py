from collections import defaultdict
from nltk import word_tokenize
from nltk.stem import PorterStemmer
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

stemmer = PorterStemmer()

for i in range(106,115):
    speeches = {}
    bigrams = defaultdict(set)

    file_speakermap = open("hein-daily/" + str(i) + "_SpeakerMap.txt", 'r')
    next(file_speakermap)
    for line in file_speakermap.readlines():
        arr = line.split("|")
        speechID = arr[1]
        party = arr[7]
        if party in ('D', 'R'):
            speeches[speechID] = {'party': party}
    file_speakermap.close()

    file_descr = open("hein-daily/descr_" + str(i) + ".txt", 'r')
    next(file_descr)
    for line in file_descr.readlines():
        arr = line.split("|")
        speech_id = arr[0]
        if speech_id in speeches:
            date_string = arr[2]
            year = int(date_string[:4])
            month = int(date_string[4:6])
            day = int(date_string[6:])
            speeches[speech_id]['date'] = {"year": year, "month": month, "day": day}
    file_descr.close()

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
            tokens = [str(stemmer.stem(word)) for word in tokens if word not in stopword_set]
            for bigram in set(ngrams(tokens,2)):
                bigrams[bigram].add(speech_id)
    file_speeches.close()

    bigrams = {k: v for k, v in bigrams.items() if len(v) >= 10}

    pickle.dump(speeches, open("speeches" + str(i) + ".p", "wb"))
    pickle.dump(bigrams, open("bigrams" + str(i) + ".p", "wb"))