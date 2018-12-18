from datetime import date
from collections import defaultdict
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.util import ngrams
import string
import re
import pickle

stopword_set = set()
file = open("~/stop.txt", 'r')
for line in file.readlines():
    word = line[:line.find('|')] if '|' in line else line
    word = word.strip()
    if len(word) > 0:
        stopword_set.add(word)
file.close()

file_names = {}
file_names['speakermap'] = [str(i) + "_SpeakerMap.txt" for i in range(106, 115)]
file_names['descr'] = ["descr_" + str(i) + ".txt" for i in range(106, 115)]
file_names['speeches'] = ["speeches_" + str(i) + ".txt" for i in range(106, 115)]

speeches = {}
for file_name in file_names['speakermap']:
    file = open("~/hein-daily/" + file_name, 'r')
    next(file)
    for line in file.readlines():
        arr = line.split("|")
        speechID = arr[1]
        party = arr[7]
        if party in ['D', 'R']:
            speeches[speechID] = {'party': party}
    file.close()

for filename in file_names['descr']:
    file = open("~/hein-daily/" + filename, 'r')
    next(file)
    for line in file.readlines():
        arr = line.split("|")
        speech_id = arr[0]
        if speech_id in speeches:
            date_string = arr[2]
            year = int(date_string[:4])
            if year >= 2000:
                month = int(date_string[4:6])
                day = int(date_string[6:])
                speeches[speech_id]['date'] = date(year, month, day)
            else:
                speeches.pop(speech_id)
    file.close()

stemmer = PorterStemmer()
bigrams = defaultdict(set)
for filename in file_names['speeches']:
    file = open("~/hein-daily/" + filename, 'rb')
    next(file)
    for line in file.readlines():
        arr = line.decode("ascii", "ignore").split("|")
        speech_id = arr[0]
        if speech_id in speeches:
            text = arr[1].rstrip().lower()
            text = text.replace('-', '').replace('\'', '')
            text = re.sub('[' + string.punctuation + ']', ' ', text) # remove punctuation
            tokens = word_tokenize(text)
            tokens = [str(stemmer.stem(word)) for word in tokens if word not in stopwordSet]
            tokens = [word for word in tokens if word not in stopword_set]
            for bigram in set(ngrams(tokens,2)):
                bigrams[bigram].add(speech_id)
    file.close()

pickle.dump(bigrams, open("bigrams.p", "wb"))
pickle.dump(speeches, open("speeches.p", "wb"))