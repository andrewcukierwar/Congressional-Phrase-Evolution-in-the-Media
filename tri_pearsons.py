from collections import defaultdict
import pickle

all_speeches = pickle.load(open("speeches.p", "rb"))
trigram_dict = pickle.load(open("trigrams.p", "rb"))
new_trigrams = pickle.load(open("new_trigrams.p", "rb"))

pearsons = {}
for i in range(108,115):
    trigrams = trigram_dict[i]
    
    r_phrase_counts = defaultdict(int)
    d_phrase_counts = defaultdict(int)
    speeches = all_speeches[i]
    for trigram, speechIDs in trigrams.items():
        for speechID in speechIDs:
            party = speeches[speechID]["party"]
            if party == 'R':
                r_phrase_counts[trigram] += 1
            elif party == 'D':
                d_phrase_counts[trigram] += 1      
    r_sum = sum(r_phrase_counts.values())
    d_sum = sum(d_phrase_counts.values())

    pearson = {}
    for trigram in trigrams:
        f_plr = r_phrase_counts[trigram] if trigram in r_phrase_counts else 0
        f_pld = d_phrase_counts[trigram] if trigram in d_phrase_counts else 0
        f_nplr = r_sum - f_plr
        f_npld = d_sum - f_pld
        num = (f_plr*f_npld - f_pld*f_nplr)**2
        denom = (f_plr+f_pld)*(f_plr+f_nplr)*(f_pld+f_npld)*(f_nplr+f_npld)
        sign = 2*(f_plr > f_pld)-1 ## make democrat negative
        pearson[trigram] = sign * num/denom
    pearsons[i] = pearson    
pickle.dump(pearsons, open("tri_pearsons.p", "wb"))

new_pearsons = {}
for i in range(108,115):
    new_pearsons[i] = {k: v for k,v in pearsons[i].items() if k in new_trigrams[i]}
pickle.dump(new_pearsons, open("new_tri_pearsons.p", "wb"))