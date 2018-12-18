from collections import defaultdict
import pickle

all_speeches = pickle.load(open("speeches.p", "rb"))
bigram_dict = pickle.load(open("bigrams.p", "rb"))
new_bigrams = pickle.load(open("new_bigrams.p", "rb"))

pearsons = {}
for i in range(108,115):
    bigrams = bigram_dict[i]
    
    r_phrase_counts = defaultdict(int)
    d_phrase_counts = defaultdict(int)
    speeches = all_speeches[i]
    for bigram, speechIDs in bigrams.items():
        for speechID in speechIDs:
            party = speeches[speechID]["party"]
            if party == 'R':
                r_phrase_counts[bigram] += 1
            elif party == 'D':
                d_phrase_counts[bigram] += 1      
    r_sum = sum(r_phrase_counts.values())
    d_sum = sum(d_phrase_counts.values())

    pearson = {}
    for bigram in bigrams:
        f_plr = r_phrase_counts[bigram] if bigram in r_phrase_counts else 0
        f_pld = d_phrase_counts[bigram] if bigram in d_phrase_counts else 0
        f_nplr = r_sum - f_plr
        f_npld = d_sum - f_pld
        num = (f_plr*f_npld - f_pld*f_nplr)**2
        denom = (f_plr+f_pld)*(f_plr+f_nplr)*(f_pld+f_npld)*(f_nplr+f_npld)
        sign = 2*(f_plr > f_pld)-1 ## make democrat negative
        pearson[bigram] = sign * num/denom
    pearsons[i] = pearson    
pickle.dump(pearsons, open("bi_pearsons.p", "wb"))

new_pearsons = {}
for i in range(108,115):
    new_pearsons[i] = {k: v for k,v in pearsons[i].items() if k in new_bigrams[i]}
pickle.dump(new_pearsons, open("new_bi_pearsons.p", "wb"))