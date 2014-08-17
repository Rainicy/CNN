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
consumer_key = "Qe1eSWXdm76twMOGGmmLQ"
consumer_secret = "FitIcbiucVSquySRstj0dhBgv63EahcZ9dLqZw7nec"
access_key = "1404317106-tTeL8nxQjYJPvuQIOCy8LlFEfvDpfg9EWBazHdw"
access_secret = "0vocin7EMHxkcfUSOWFbsmTmzt53UGf5IgZ7QncjPg0ZE"

logFile = '../log/ids.log'
 
# @classmethod
# class JsonParser(Parser):
#     def parse(self, method, payload):
#         return json.loads(payload)
 
def get_all_ids(user_id, out_friends, out_followers, api):
	'''
	Description: Given the user_id, find his/her firends or followers Ids and save 
				them to the files.
	'''
	if not (os.path.isfile(out_friends)):
		#initialize a list to hold all the tweepy Tweets
		friends_ids = []
		pages = tweepy.Cursor(api.friends_ids, user_id = user_id).pages()
		while True:
			try:
				for page in pages:
					friends_ids.extend(page)
					print len(friends_ids)
				break
			except tweepy.TweepError as e:
				if e.response.status == 401:
					with open(logFile, 'a') as file:
						file.write(out_friends + '\t' + str(e.response.status) + '\n')
						file.close()
					break
				elif e.response.status == 429:			# rate limit message code = 88
					print "Waiting for one minutes until you can send the request again..."
					time.sleep(60)
					continue
				else:
					with open(logFile, 'a') as file:
						file.write(out_friends + '\t' + str(e.response.status) + '\n')
						file.close()
					break

		with open(out_friends, 'w') as file:
			file.writelines("%s\n" % item for item in friends_ids)
			file.close()

	if not (os.path.isfile(out_followers)):
		followers_ids = []
		pages = tweepy.Cursor(api.followers_ids, user_id = user_id).pages()
		while True:
			try:
				for page in pages:
					followers_ids.extend(page)
					print len(followers_ids)
				break
			except tweepy.TweepError as e:
				if e.response.status == 401:
					with open(logFile, 'a') as file:
						file.write(out_followers + '\t' + str(e.response.status) + '\n')
						file.close()
					break
				elif e.response.status == 429:			# rate limit message code = 88
					print "Waiting for one minutes until you can send the request again..."
					time.sleep(60)
					continue
				else:
					with open(logFile, 'a') as file:
						file.write(out_followers + '\t' + str(e.response.status) + '\n')
						file.close()
					break

		with open (out_followers, 'w') as file:
			file.writelines("%s\n" % item for item in followers_ids)
			file.close()


 
if __name__ == '__main__':
	'''
	Description: This is for crawling all the friends & followers IDs by given users' IDs.

	'''

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	# read list
	user_ids = []
	fin = open('../data/top-friends', 'r')
	lines = fin.readlines()
	for line in lines:
		user_id = line.split('\t')[0]
		user_ids.append(user_id)

	total = len(user_ids)
	print '%s users' % str(total)

	s_out_dir = '../data/ids/'

	#pass in the userid of the account you want to download
	count = 1
	for user_id in user_ids:
		print 'Working on: \t ({} / {})'.format(count, total)
		count += 1
		s_out_friends_ids = s_out_dir + str(user_id) + '_friends_ids'
		s_out_followers_ids = s_out_dir + str(user_id) + '_followers_ids'
		if (os.path.isfile(s_out_friends_ids)) and (os.path.isfile(s_out_followers_ids)):
			continue

		print user_id
		get_all_ids(user_id, s_out_friends_ids, s_out_followers_ids, api)