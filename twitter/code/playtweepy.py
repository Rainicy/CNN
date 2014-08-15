import tweepy
import time
import os
import sys
import os.path

if __name__ == '__main__':
	# using gyp7364@gmail.com
	consumer_key = 'EmEvdgcg4QHL7zkQA8ZaEw'
	consumer_secret = 'Dy4Zdb2BFWpzH84T9k3bfO0ESx8eWrXzKM9iAEzw'
	access_token = '1536493429-9CsKdJkQSYf5o9TsXJCvAz5ZFvhunuWTZlgxpcM'
	access_token_secret = 'rPy8TMpa74hvlYEhQVz8nGdDb132TwQQil39I9Hf1zcK0'

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	# read list
	user_ids = []
	fin = open('../data/top-friends', 'r')
	lines = fin.readlines()
	for line in lines:
		user_id = line.split('\t')[0]
		user_ids.append(user_id)

	print '%s users' % str(len(user_ids))

	# crawl
	s_out_dir = '../data/tweets/'
	for user_id in user_ids:
		print user_id

		s_out_tweet = s_out_dir + str(user_id) + '.tweets'

		if os.path.isfile(s_out_tweet):
			continue

		f_out_tweet = open(s_out_tweet, 'w')

		try:
			user = api.get_user(user_id)
		except tweepy.error.TweepError as e:
			if e.message[0]['code'] == 34:			# page doesn't exist
				continue
		else:
			pass

		# tweet
		pages = tweepy.Cursor(api.user_timeline, user_id).pages()

		n = 1
		for page in pages:
			print n
			n += 1
			for status in page:
				print status
				raw_input()
				# continue


		# count1 = 1
# 		while True:
# 			# print 'C: ' + str(count1)
# 			# count1 +=1 
# 			try:
# 				count = 1
# 				for page in pages:
# 					print 'I am here...'
# 					# print 'a:' + str(count)
# 					# count += 1
# 					for status in page:
# #						status = user.status					# first status

# 						tid = status.id_str					# id of the status
# 						text = status.text					# text 
# 						if status.truncated == True:
# 							text = status.retweeted_status.text
# 						coord = [0,0]
# 						if status.coordinates:
# 							try:
# 								coord = status.coordinates['coordinates']
# 							except AttributeError:
# 								coord = [0,0]

# 						entities = status.entities				# Entities from the text
# 						mentions = []; hashtags = []; urls = [];
# 						mention_length = 0; hashtag_length = 0; url_length = 0;
# 						if entities['user_mentions']:
# 							mention_length = len(entities['user_mentions'])
# 							for m in entities['user_mentions']:
# 								mentions.append(m['id_str'])
# 						if entities['hashtags']:
# 							hashtag_length = len(entities['hashtags'])
# 							for h in entities['hashtags']:
# 								hashtags.append(h['text'])
# 						if entities['urls']:
# 							url_length = len(entities['urls'])
# 							for u in entities['urls']:
# 								urls.append(u['expanded_url'])
				
# 						created_time = status.created_at			# UTC time when this Tweet was created
# #						print created_time
# #						print dir(created_time)
# #						print created_time.year, created_time.month, created_time.day
# #						gu = raw_input()
# 						favorite_count = status.favorite_count			# Number of times this Tweet has been favorited (0,1,2,...)
# 						retweet_count = status.retweet_count			# Number of times this Tweet has been retweeted (0,1,2,...)
# 						try:
# 							retweeted_status = status.retweeted_status	# see if it's not a rt
# 						except AttributeError:
# 							is_retweet = 0					# False
# 						else:
# 							is_retweet = 1					# True
# 							text = status.retweeted_status.text
# 						if is_retweet:
# 							retweet_from = retweeted_status.user.id_str
# 						else:
# 							retweet_from = '-1'

# 						# check for unicode error
# 						if (not isinstance(text, str)):				# if type of status.text is not <type 'str'>
# 							text = text.encode('ascii', 'ignore')
# 						text = text.replace('\n', ' ')
# 						text = text.replace('\t', ' ')

# 						newline = tid + '\t' + text + '\t' + str(coord[0]) + '\t' + str(coord[1]) + '\t'
# 						newline = newline + str(favorite_count) + '\t' + str(retweet_count) + '\t'
# 						newline = newline + str(is_retweet) + '\t' + retweet_from + '\t'

# 						newline = newline + str(mention_length) + '\t'
# 						if mention_length != 0:
# 							for m in mentions:
# 								newline = newline + m + '\t'
# 						newline = newline + str(hashtag_length) + '\t'
# 						if hashtag_length != 0:
# 							for h in hashtags:
# 								newline = newline + h + '\t'
# 						newline = newline + str(url_length) + '\t'
# 						if url_length != 0:
# 							for u in urls:
# 								newline = newline + u + '\t'
# 						newline = newline + str(created_time.year) + '\t' + str(created_time.month) + '\t' + str(created_time.day) + '\n'
# 						f_out_tweet.write(newline)

# 			except tweepy.error.TweepError as e:
# 				continue
# #				if e.message[0]['code'] == 88:			# rate limit
# #					print "Waiting for one minute until you can send the request again..."
# #					time.sleep(60)
# #					continue
# #				else:
# #					break
# 			except UnicodeEncodeError:
# 				print 'unicode error'
# 				continue
# 			except StopIteration:
# 				break
# 			else:
# 				continue
#				break

