import pickle

bigrams = pickle.load(open("bigrams.p", "rb"))
vocab_base = set(bigrams[106].keys()) | set(bigrams[107].keys())

new_bigrams = {}
for i in range(108,115):
    new_bigrams[i] = {k: v for k, v in bigrams[i].items() if k not in vocab_base}
    vocab_base = vocab_base | set(bigrams[i].keys())

pickle.dump(new_bigrams, open("new_bigrams.p", "wb"))
