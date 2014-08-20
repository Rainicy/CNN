#!/usr/bin/env python
# encoding: utf-8

import os
import time
import tweepy #https://github.com/tweepy/tweepy
import json
from tweepy.parsers import Parser
 

'''
	Refer	1) http://blog.caoyue.me/post/tweepy-raw-json
			2) https://gist.github.com/yanofsky/5436496
'''

#Twitter API credentials
consumer_key = "EmEvdgcg4QHL7zkQA8ZaEw"
consumer_secret = "Dy4Zdb2BFWpzH84T9k3bfO0ESx8eWrXzKM9iAEzw"
access_key = "1536493429-9CsKdJkQSYf5o9TsXJCvAz5ZFvhunuWTZlgxpcM"
access_secret = "rPy8TMpa74hvlYEhQVz8nGdDb132TwQQil39I9Hf1zcK0"

logFile = '../log/tweets.log'
 
# @classmethod
class JsonParser(Parser):
    def parse(self, method, payload):
        return json.loads(payload)
 
def get_all_tweets(user_id, outfile, api):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	

	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	while True:
		try:
			new_tweets = api.user_timeline(user_id = user_id,count=200)
			break
		except tweepy.TweepError as e:
			print e 
			if e.response.status == 401:
				with open(outfile, 'w') as file:
					file.close()
				with open(logFile, 'a') as file:
					file.write(outfile + '\t' + str(e.response.status) + '\n')
					file.close()
				return
			elif e.response.status == 429:			# rate limit message code = 88
				print "Waiting for one minutes until you can send the request again..."
				time.sleep(60)
				continue
			else:
				with open(logFile, 'a') as file:
					file.write(outfile + '\t' + str(e.response.status) + '\n')
					file.close()
				return
		except StopIteration:
			break

	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	try:
		oldest = alltweets[-1]['id'] - 1
	except IndexError as e:
		with open(outfile, 'w') as file:
			file.close()
		with open(logFile, 'a') as file:
			file.write(outfile + '\t' + str(e) + '\n')
			file.close()
		return
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		while True:
			try:
				new_tweets = api.user_timeline(user_id = user_id,count=200,max_id=oldest)
				break
			except tweepy.TweepError as e:
				print e 
				if e.response.status == 401:
					with open(outfile, 'w') as file:
						file.close()
					with open(logFile, 'a') as file:
						file.write(outfile + '\t' + str(e.response.status) + '\n')
						file.close()
					return
				elif e.response.status == 429:			# rate limit
					print "Waiting for one minutes until you can send the request again..."
					time.sleep(60)
					continue
				else:
					with open(logFile, 'a') as file:
						file.write(outfile + '\t' + str(e.response.status) + '\n')
						file.close()
					return
			except StopIteration:
				break
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1]['id'] - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	

	with open(outfile, 'w') as file:
		for i in range(len(alltweets)):
			file.write(json.dumps(alltweets[i],file,) + '\n')
		file.close()
	# pass
 
 
if __name__ == '__main__':

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth, parser=JsonParser())

	# read list
	user_ids = []
	fin = open('../data/split/0', 'r')
	lines = fin.readlines()
	for line in lines:
		user_id = line.split('\t')[0]
		user_id = user_id.strip('\n')
		user_ids.append(user_id)

	total = len(user_ids)
	print '%s users' % str(total)

	s_out_dir = '../data/tweets/'

	#pass in the userid of the account you want to download
	count = 1
	for user_id in user_ids:
		print 'Working on: \t ({} / {})'.format(count, total)
		count += 1
		s_out_tweet = s_out_dir + str(user_id) + '_tweets.json'
		if os.path.isfile(s_out_tweet):
			continue

		print user_id
		get_all_tweets(user_id, s_out_tweet, api)