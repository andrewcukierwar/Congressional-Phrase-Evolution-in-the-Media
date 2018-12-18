from collections import defaultdict, Counter
from datetime import date
import pickle
import json

bigrams = pickle.load(open("bigrams.p", "rb"))
speeches = pickle.load(open("speeches.p", "rb"))
new_pearsons = pickle.load(open("new_bi_pearsons.p", "rb"))

sources = ["dkos", "motherjones", "nymag", "nypost", "townhall", "breitbart"]
news_articles = {source: pickle.load(open(source + '_bigrams_new.p', 'rb')) for source in sources}

# create a {bigram: [dates]} dictionary for each party, compiling sources into respective parties
d_news_bigrams = defaultdict(list)
for source in ('dkos', 'motherjones', 'nymag'):
    for article in news_articles[source]:
        for bigram in article['bigram']:
            d_news_bigrams[bigram].append(article['date'])
            
r_news_bigrams = defaultdict(list)
for source in ('nypost', 'townhall', 'breitbart'):
    for article in news_articles[source]:
        for bigram in article['bigram']:
            r_news_bigrams[bigram].append(article['date'])

congress_bigram_dates = {}
for current_session, pearsons in new_pearsons.items():
    for bigram in pearsons:
        d_dates = []
        r_dates = []
        for session in range(106,115):
            if bigram in bigrams[session]:
                speechIDs = bigrams[session][bigram]
                for speechID in speechIDs:
                    speech = speeches[session][speechID]
                    if speech['party'] == 'D':
                        d_dates.append(speech['date'])
                    else:
                        r_dates.append(speech['date'])
        congress_bigram_dates[bigram] = {'d_dates': d_dates, 'r_dates': r_dates}

news_bigram_dates = {}
for current_session, pearsons in new_pearsons.items():
    for bigram in pearsons:
        d_dates = d_news_bigrams[bigram] if bigram in d_news_bigrams else []
        r_dates = r_news_bigrams[bigram] if bigram in r_news_bigrams else []
        news_bigram_dates[bigram] = {'d_dates': d_dates, 'r_dates': r_dates}

for bigram in congress_bigram_dates:
    congress_date_dict = congress_bigram_dates[bigram]
    congress_d_dates = [date(d['year'], d['month'], d['day']) for d in congress_date_dict['d_dates']]
    congress_r_dates = [date(d['year'], d['month'], d['day']) for d in congress_date_dict['r_dates']]

    news_date_dict = news_bigram_dates[bigram]
    news_d_dates = [date(d['year'], d['month'], d['day']) for d in news_date_dict['d_dates']]
    news_r_dates = [date(d['year'], d['month'], d['day']) for d in news_date_dict['r_dates']]

    origin = min(congress_d_dates + congress_r_dates)

    congress_bigram_dates[bigram]['d_dates'] = [(d - origin).days for d in congress_d_dates]
    congress_bigram_dates[bigram]['r_dates'] = [(d - origin).days for d in congress_r_dates]
    news_bigram_dates[bigram]['d_dates'] = [(d - origin).days for d in news_d_dates]
    news_bigram_dates[bigram]['r_dates'] = [(d - origin).days for d in news_r_dates]

congress_bi_dates = {k[0] + " " + k[1]: v for k, v in congress_bigram_dates.items()}
news_bi_dates = {k[0] + " " + k[1]: v for k, v in news_bigram_dates.items()}
new_bi_pearsons = {}
for session, pearsons in new_pearsons.items():
    new_bi_pearsons[session] = {k[0] + " " + k[1]: v for k, v in pearsons.items()}

json.dump(congress_bi_dates, open('congress_bi_dates.json', 'w'))
json.dump(news_bi_dates, open('news_bi_dates.json', 'w'))
json.dump(new_bi_pearsons, open('new_bi_pearsons.json', 'w'))