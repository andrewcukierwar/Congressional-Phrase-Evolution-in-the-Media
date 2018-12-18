# Filter by speaker
import pickle

bigrams = pickle.load(open("bigrams.p", "rb"))
speeches = pickle.load(open("speeches.p", "rb"))

for i in range(106,115):
    bigram_speakers = {}
    for bigram, speech_ids in bigrams[i].items():
        speakers = set()
        for speech_id in speech_ids
            speaker = speeches[i][speech_id]['speakerID']
            speakers.add(speaker)
        bigram_speakers[bigram] = speakers
    bigrams[i] = {k: v for k, v in bigrams[i].items() if len(bigram_speakers[k]) >= 10}
    
pickle.dump(bigrams, open("bigrams.p", "wb"))