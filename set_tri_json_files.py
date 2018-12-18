from collections import defaultdict, Counter
from datetime import date
import pickle
import json

trigrams = pickle.load(open("trigrams.p", "rb"))
speeches = pickle.load(open("speeches.p", "rb"))
new_pearsons = pickle.load(open("new_tri_pearsons.p", "rb"))

sources = ["dkos", "motherjones", "nymag", "nypost", "townhall", "breitbart"]
news_articles = {source: pickle.load(open(source + '_trigrams_new.p', 'rb')) for source in sources}

# create a {trigram: [dates]} dictionary for each party, compiling sources into respective parties
d_news_trigrams = defaultdict(list)
for source in ('dkos', 'motherjones', 'nymag'):
    for article in news_articles[source]:
        for trigram in article['trigram']:
            d_news_trigrams[trigram].append(article['date'])
            
r_news_trigrams = defaultdict(list)
for source in ('nypost', 'townhall', 'breitbart'):
    for article in news_articles[source]:
        for trigram in article['trigram']:
            r_news_trigrams[trigram].append(article['date'])

congress_trigram_dates = {}
for current_session, pearsons in new_pearsons.items():
    for trigram in pearsons:
        d_dates = []
        r_dates = []
        for session in range(106,115):
            if trigram in trigrams[session]:
                speechIDs = trigrams[session][trigram]
                for speechID in speechIDs:
                    speech = speeches[session][speechID]
                    if speech['party'] == 'D':
                        d_dates.append(speech['date'])
                    else:
                        r_dates.append(speech['date'])
        congress_trigram_dates[trigram] = {'d_dates': d_dates, 'r_dates': r_dates}

news_trigram_dates = {}
for current_session, pearsons in new_pearsons.items():
    for trigram in pearsons:
        d_dates = d_news_trigrams[trigram] if trigram in d_news_trigrams else []
        r_dates = r_news_trigrams[trigram] if trigram in r_news_trigrams else []
        news_trigram_dates[trigram] = {'d_dates': d_dates, 'r_dates': r_dates}

for trigram in congress_trigram_dates:
    congress_date_dict = congress_trigram_dates[trigram]
    congress_d_dates = [date(d['year'], d['month'], d['day']) for d in congress_date_dict['d_dates']]
    congress_r_dates = [date(d['year'], d['month'], d['day']) for d in congress_date_dict['r_dates']]

    news_date_dict = news_trigram_dates[trigram]
    news_d_dates = [date(d['year'], d['month'], d['day']) for d in news_date_dict['d_dates']]
    news_r_dates = [date(d['year'], d['month'], d['day']) for d in news_date_dict['r_dates']]

    origin = min(congress_d_dates + congress_r_dates)

    congress_trigram_dates[trigram]['d_dates'] = [(d - origin).days for d in congress_d_dates]
    congress_trigram_dates[trigram]['r_dates'] = [(d - origin).days for d in congress_r_dates]
    news_trigram_dates[trigram]['d_dates'] = [(d - origin).days for d in news_d_dates]
    news_trigram_dates[trigram]['r_dates'] = [(d - origin).days for d in news_r_dates]

congress_tri_dates = {k[0] + " " + k[1] + " " + k[2]: v for k, v in congress_trigram_dates.items()}
news_tri_dates = {k[0] + " " + k[1] + " " + k[2]: v for k, v in news_trigram_dates.items()}
new_tri_pearsons = {}
for session, pearsons in new_pearsons.items():
    new_tri_pearsons[session] = {k[0] + " " + k[1] + " " + k[2]: v for k, v in pearsons.items()}

json.dump(congress_tri_dates, open('congress_tri_dates.json', 'w'))
json.dump(news_tri_dates, open('news_tri_dates.json', 'w'))
json.dump(new_tri_pearsons, open('new_tri_pearsons.json', 'w'))