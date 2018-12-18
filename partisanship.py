from collections import defaultdict
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.util import ngrams
import string
import re
import pickle

for i in range(106,115):
    speeches = {}

    file_speakermap = open("hein-daily/" + str(i) + "_SpeakerMap.txt", 'r')
    next(file_speakermap)
    for line in file_speakermap.readlines():
        arr = line.split("|")
        speechID = arr[1]
        party = arr[7]
        if party in ('D', 'R'):
            speeches[speechID] = {'party': party}
    file_speakermap.close()

    r_phrase_counts = defaultdict(int)
    d_phrase_counts = defaultdict(int)

    bigrams = pickle.load(open("bigrams" + str(i) + ".p", "rb"))

    for bigram, speechIDs in bigrams.items():
        for speechID in speechIDs:
            party = speeches[speechID]['party']
            if party == 'R':
                r_phrase_counts[bigram] += 1
            elif party == 'D':
                d_phrase_counts[bigram] += 1
                
    r_count_sum = sum(r_phrase_counts.values()) # m_t: the total amount of speech in session t
    r_phrase_freqs = {bigram: count / r_count_sum for bigram, count in r_phrase_counts.items()} # q_t

    d_count_sum = sum(d_phrase_counts.values()) # m_t: the total amount of speech in session t
    d_phrase_freqs = {bigram: count / d_count_sum for bigram, count in d_phrase_counts.items()} # q_t

    posteriors = {}

    full_summation = 0
    for bigram_k in bigrams:
        q_kr = r_phrase_freqs[bigram_k] if bigram_k in r_phrase_freqs else 0
        q_kd = d_phrase_freqs[bigram_k] if bigram_k in d_phrase_freqs else 0
        rho_k = q_kr / (q_kr + q_kd)
        full_summation += (q_kr/(1-q_kr) + q_kd/(1-q_kd)) * rho_k

    for bigram_j in bigrams:
        q_jr = r_phrase_freqs[bigram_j] if bigram_j in r_phrase_freqs else 0
        q_jd = d_phrase_freqs[bigram_j] if bigram_j in d_phrase_freqs else 0
        rho_j = q_jr / (q_jr + q_jd)
        summation = full_summation - (q_jr/(1-q_jr) + q_jd/(1-q_jd)) * rho_j
        posteriors[bigram_j] = 0.5 - 0.5*summation

    pickle.dump(speeches, open("posteriors" + str(i) + ".p", "wb"))
