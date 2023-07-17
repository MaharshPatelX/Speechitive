import os
import json
from operator import itemgetter

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from datetime import datetime

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SyntaxOptions, SyntaxOptionsTokens, CategoriesOptions, ConceptsOptions
import sys
import time



start = time.time()
tmp_fil = sys.argv[1:]
if tmp_fil == []:
	exit()
fil_path='../../'+tmp_fil[0]
global path_store
path_store = fil_path.replace('up_videos','output')
path2_s = path_store.replace('output','hls')


apikey = 'Your-API-Key'
url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/bcc8c7cc-7256-4b3d-a66e-a7cfcbe7ce66'

# Natural Language Understanding
authenticator = IAMAuthenticator(apikey)
natural_language_understanding =  NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
# stt =  NaturalLanguageUnderstandingV1(authenticator=authenticator)
natural_language_understanding.set_service_url(url)

with open(path_store+'/txt/output.txt', 'r') as text_file:
	text = text_file.read()

# print(text)

myJsonDict = {}

''' Extract Category with NLU '''

try:
	response = natural_language_understanding.analyze(
		language='en',
		text=text,
		features=Features(categories=CategoriesOptions(limit=1))).get_result()

	category = response['categories'][0]

	myJsonDict.update({"category": category})

except:
	myJsonDict.update({"category": "Text too small to extract category"})


try:
	response = natural_language_understanding.analyze(
		language='en',
		text=text,
		features=Features(concepts=ConceptsOptions(limit=3))).get_result()

	concepts = sorted(response['concepts'], key=itemgetter('relevance'), reverse=True)

	myJsonDict.update({"concepts": concepts})

except:
	myJsonDict.update({"concepts": "Text too small to extract concepts"})


try:
	response = natural_language_understanding.analyze(
		language='en',
		text=text,
		features=Features(entities=EntitiesOptions(limit=1))).get_result()

	entity = sorted(response['entities'], key=itemgetter('relevance'), reverse=True)

	myJsonDict.update({"entity": entity[0]})

except:
	myJsonDict.update({"entity": "Text too small to extract entity"})


try:
	response = natural_language_understanding.analyze(
		language='en',
		text=text,
		features=Features(keywords=KeywordsOptions(sentiment=True, emotion=True, limit=10))).get_result()

	keywords = sorted(response['keywords'], key=itemgetter('relevance'), reverse=True)

	keywords_sentiments_emotions = []
	
	for i in keywords:
	
		keywords_sentiments_emotions_buffer = {'keyword': i['text'],'sentiment': i['sentiment']['label'],'emotion': ''}
		maximum = i['emotion']['sadness']
		keywords_sentiments_emotions_buffer['emotion'] = 'sadness'
	
		if i['emotion']['joy'] > maximum:
			maximum = i['emotion']['joy']
			keywords_sentiments_emotions_buffer['emotion'] = 'joy'
		
		elif i['emotion']['fear'] > maximum:
			maximum = i['emotion']['fear']
			keywords_sentiments_emotions_buffer['emotion'] = 'fear'
		
		elif i['emotion']['disgust'] > maximum:
			maximum = i['emotion']['disgust']
			keywords_sentiments_emotions_buffer['emotion'] = 'disgust'
		
		elif i['emotion']['anger'] > maximum:
			maximum = i['emotion']['anger']
			keywords_sentiments_emotions_buffer['emotion'] = 'anger'
	
		keywords_sentiments_emotions.append(keywords_sentiments_emotions_buffer)

	myJsonDict.update({"sentiments": keywords_sentiments_emotions})

except:
	myJsonDict.update({"sentiments": "Text too small to extract sentiments"})


try:
	response = natural_language_understanding.analyze(
		language='en',
		text=text,
		features=Features(keywords=KeywordsOptions(sentiment=True, emotion=True))).get_result()

	keywords = sorted(response['keywords'], key=itemgetter('relevance'), reverse=True)

	keywords_sentim_pos = []
	keywords_sentim_neg = []
	
	for i in keywords:

		keywords_sentiments = {'keyword': i['text'],'sentiment': i['sentiment']['label']}

		if i['sentiment']['label']=='positive':
			keywords_sentiments['sentiment'] = 'positive'
			keywords_sentim_pos.append(keywords_sentiments)

		if i['sentiment']['label']=='negative':
			keywords_sentiments['sentiment'] = 'negative'
			keywords_sentim_neg.append(keywords_sentiments)

	myJsonDict.update({"positive_sentiments": keywords_sentim_pos})
	myJsonDict.update({"negative_sentiments": keywords_sentim_neg})

except:
	myJsonDict.update({"positive_sentiments": "Text too small to extract sentiments"},{"negative_sentiments": "Text too small to extract sentiments"})



''' Pre-Processing parts of speech to plot Word Cloud '''

try:
	response = natural_language_understanding.analyze(
		language='en',
		text=text,
		features=Features(syntax=SyntaxOptions(sentences=True,tokens=SyntaxOptionsTokens(lemma=True,part_of_speech=True)))).get_result()
	
	verbs = []
	for i in response['syntax']['tokens']:
		if i['part_of_speech'] == 'VERB':
			verbs.append(i['text'])
	
	nouns = []
	for i in response['syntax']['tokens']:
		if i['part_of_speech'] == 'NOUN':
			 nouns.append(i['text'])
	
	adj = []
	for i in response['syntax']['tokens']:
		if i['part_of_speech'] == 'ADJ':
			adj.append(i['text'])
	
	nouns_adjectives = []
	for x in nouns:
		nouns_adjectives.append(x)
	
	for y in adj:
		nouns_adjectives.append(y)
	
	comment_words_verbs = ' '
	comment_words_nouns_adj = ' '
	stopwords = set(STOPWORDS)
	
	for val in verbs:
		val = str(val)
		tokens = val.split()
		for i in range(len(tokens)):
			tokens[i] = tokens[i].lower()
		for words in tokens:
			comment_words_verbs = comment_words_verbs + words + ' '
	
	for val in nouns_adjectives:
		val = str(val)
		tokens = val.split()
		for i in range(len(tokens)):
			tokens[i] = tokens[i].lower()
		for words in tokens:
			comment_words_nouns_adj = comment_words_nouns_adj + words + ' '
	
	wordcloud_verbs = WordCloud(width=800, height=800,
		background_color='white',
		stopwords=stopwords,
		min_font_size=10,
		max_font_size=150,
		random_state=42).generate(comment_words_verbs)
	
	wordcloud_nouns_adj = WordCloud(width=800, height=800,
		background_color='white',
		stopwords=stopwords,
		min_font_size=10,
		max_font_size=150,
		random_state=42).generate(comment_words_nouns_adj)
	
	verbsWC = path_store+"/img/verbs.png"
	plt.switch_backend('Agg')
	plt.figure(figsize=(5, 5), facecolor=None)
	plt.imshow(wordcloud_verbs)
	plt.axis("off")
	plt.tight_layout(pad=0)
	plt.savefig(verbsWC)
	
	nounsAdjWC = path_store+"/img/nouns_adjectives.png"
	plt.switch_backend('Agg')
	plt.figure(figsize=(5, 5), facecolor=None)
	plt.imshow(wordcloud_nouns_adj)
	plt.axis("off")
	plt.tight_layout(pad=0)
	plt.savefig(nounsAdjWC)
	
	wordclouds = [nounsAdjWC, verbsWC]
	
	myJsonDict.update({"wordclouds": wordclouds})

except:
	myJsonDict.update({"wordclouds": "Text too small to extract wordclouds"})



with open(path_store+"/json/output.json", "w") as outfile:
	json.dump(myJsonDict, outfile,indent=4)


import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["CGC"]
vdata = mydb["video_data"]
y = vdata.find_one({'new_name':path2_s.split('/')[-1]})

os.system('mkdir "'+path2_s+'/sub"')
os.system('copy "'+path_store+'/vtt/" "'+path2_s+'/sub/"')
m3u8_cont = '#EXTM3U\n#EXT-X-TARGETDURATION:'+y['video_lenth'].split('.')[0]+'\n#EXT-X-VERSION:3\n#EXT-X-MEDIA-SEQUENCE:1\n#EXT-X-PLAYLIST-TYPE:VOD\n#EXTINF:'+y['video_lenth']+',\ntmp.vtt'+'\n#EXT-X-ENDLIST'
f = open(path2_s+"/sub/index_sub.m3u8", "a")
f.write(m3u8_cont)
f.close()

end = time.time()
print((end - start)/60)
