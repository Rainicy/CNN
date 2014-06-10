'''
Created on June 6, 2014

@author Rainicy
'''

from time import sleep
from datetime import datetime

import feedparser

from News import *
from Log import *


def main():

	feedURLs = '../data/feedURLs'
	urlList = readURLs(feedURLs)

	# Remove all the links of video 
	removeLink = 'http://www.cnn.com/video/'
		
	count = 1
	# List for the links, which already have been collected
	dictList = []
	dictLinksFile = '../dict/Dict_Links'
	with open(dictLinksFile, 'r') as file:
		lines = file.readlines()
		for line in lines: 
			dictList.append(line.split('\n')[0])
			count += 1

	while True:
		startTime = datetime.now()
		startCount = count

		# go through all the feed URLs 
		for feedurl in urlList:
			# print the topic rss
			print '\n-------------\t%s\t-------------\n' % feedurl.split('/')[-1]
			# avoid the error happens during the url parsing
			while True:
				try:
					feed = feedparser.parse(feedurl)
					break
				except:
					print 'Parse feed Error... Wait 30 seconds to continue...'
					sleep(30)

			for item in feed['items']:
			    url =  item.guid
			    if url not in dictList:	# new links 
				    if (removeLink not in url):	# if it is not a video link
				    	if buildArticleTables(url, count): # Also if the article use the disqus system
				    		writeDictFile(url)	# write the Link
				    		dictList.append(dictList)

				    		# update the dictionary list and count 
				    		dictList.append(url) # add the link to the link list
				    		count += 1
				    		sleep(2)
				    		
		writeLog(startTime, startCount, count)

		print 'Sleeping for 15 minutes......'
		sleep(900)

if __name__ == '__main__':
	main()