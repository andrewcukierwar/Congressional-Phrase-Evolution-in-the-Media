import pickle

trigrams = pickle.load(open("trigrams.p", "rb"))
vocab_base = set(trigrams[106].keys()) | set(trigrams[107].keys())

new_trigrams = {}
for i in range(108,115):
    new_trigrams[i] = {k: v for k, v in trigrams[i].items() if k not in vocab_base}
    vocab_base = vocab_base | set(trigrams[i].keys())

pickle.dump(new_trigrams, open("new_trigrams.p", "wb"))
