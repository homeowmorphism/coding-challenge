#!/usr/bin/python
import json
import string
from datetime import datetime
from datetime import timedelta

def parsehashtags(tweet):
	hashtags = []
	if 'entities' in tweet: 
		for j in range(len(tweet['entities']['hashtags'])): 
			hashtags.append(tweet['entities']['hashtags'][j]['text'])
		hashtags = list(set(hashtags)) 
	return hashtags

def parsetime(tweet):
	if 'created_at' in tweet: 
		t = tweet['created_at']
		T = string.split(t) #takes care of the timezone shenanigans with datetime
		t = datetime.strptime(T[0] + ' ' + T[1] + ' ' + T[2] + ' ' + T[3] + ' ' + T[5], "%a %b %d %H:%M:%S %Y")
		dth = int(T[4][1:3])
		dtm = int(T[4][3:5])
		dt = timedelta(hours = dth,minutes = dtm)
		if T[4][0] == '+':
			t = t + dt
		elif T[4][0] == '-':
			t = t - dt
		return t
	#else:
	#	print 'Could not find timestamp for: ' + str(tweet)

def parser():
	output = []
	with open('./tweet_input/tweets.txt') as tweets:
		for tweet in tweets:
			tweet = json.loads(tweet)
			if parsetime(tweet) is not None:
				output.append((parsetime(tweet),parsehashtags(tweet)))
	return output

