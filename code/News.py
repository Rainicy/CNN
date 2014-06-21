import urllib2
import re
from time import sleep

from bs4 import BeautifulSoup



def writeDictFile(url): 
	'''function for writing the new link to the Dict_Links'''
	# Add links to this file, and regrad them as unique ID 
	fileName = "../dict/Dict_Links"
	with open(fileName, 'a') as file:
		file.write(url + '\n')
		file.close()

def writeAuthors(url, author):
	'''function for writing author and url to the URL_Author'''
	fileName = '../dict/URL_Author'
	with open(fileName, 'a') as file:
		file.write(url + '\t' + author + '\n')
		file.close()

def writeArticle(url, topic, title, date, time, text):
	'''function for writing article's information '''
	fileName = '../dict/Articles'
	with open(fileName, 'a') as file:
		# print (url + '\n' + topic + '\n' + title + '\n' + date + '\n' + time + '\n' + text + '\n')
		file.write(url + '\t' + topic + '\t' + title + '\t' + date + '\t' + time + '\t' + text + '\n')
		file.close()

def buildArticleTables(url, count):
	'''
	Description: Build the related dictionaries for the given article url, including:
					1) Authors Table {url, authors_title}
					2) Articles Table {url, topic, title, date, timestamp, text}
	'''
	ifContainsDisqus = False
	disqus = 'disqus_identifier'
	headers = {'User-Agent' : 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)

	# avoid the error happens during the url open and read
	while True:
		try:
			content = urllib2.urlopen(req).read()
			break
		except:
			print "Waiting for 5 seconds until you can send the request again..."
			sleep(5)

	soup = BeautifulSoup(content)
	script = soup.script.string

	# if it is a disuqs system
	if disqus in script:
		# build the regex to get the info
		r_topic = re.compile(r'cnnSectionName="(.*)",')
		r_author = re.compile(r'cnnAuthor="(.*)",')	# regex author 
		r_publish_date = re.compile(r'publish_date: "(.*)",')	# regex publish date
		r_publish_time = re.compile(r'cnnFirstPub=new Date\(\'(.*)\'\),')
		topic = re.search(r_topic, script)
		author = re.search(r_author, script)
		date = re.search(r_publish_date, script)
		time = re.search(r_publish_time, script)
		# encode the strings
		if topic:
			topic = topic.group(1).encode('ascii', 'ignore')
		if author:
			author = author.group(1).encode('ascii', 'ignore')
		if date:
			date = date.group(1).encode('ascii', 'ignore')
		if time: 
			time = time.group(1).encode('ascii', 'ignore')

		title = soup.title.string.encode('ascii', 'ignore')

		# crawl the article's text
		text = ''
		for t in soup.find_all('p'):
			text += t.get_text().encode('ascii', 'ignore') + ' '
		text = text.replace('\n', ' ')

		# write the URL-Author to the file
		writeAuthors(url, author)
		# write the Article's info to the file
		writeArticle(url, topic, title, date, time, text)

		print '%d| %s | %s' % (count, topic, title)
		ifContainsDisqus = True

	else:
		ifContainsDisqus = False
	# print soup.prettify()
	return ifContainsDisqus

def readURLs(f):
	'''
	Description: Reading the urls by given file path
	'''
	# Reading feed url list from '/data/feedURLs'
	urlList = []
	with open(f, 'r') as file:
		lines = file.readlines()
		for line in lines:
			urlList.append(line.split('\n')[0])
	return urlList


# if __name__ == '__main__':

# 	feedURLs = '../data/feedURLs'
# 	urlList = readURLs(feedURLs)

# 	# Remove all the links of video 
# 	removeLink = 'http://www.cnn.com/video/'
# 	KEYWORD = 'politics'
		
# 	# List for the links, which already have been collected
# 	dictList = []
# 	dictLinksFile = '../dict/Dict_Links'
# 	with open(dictLinksFile, 'r') as file:
# 		lines = file.readlines()
# 		for line in lines: 
# 			dictList.append(line.split('\n')[0])

# 	count = 1
# 	while True:
# 		# go through all the feed URLs 
# 		for feedurl in urlList:
# 			# print the topic rss
# 			print '\n-------------\t%s\t-------------\n' % feedurl.split('/')[-1]
# 			# avoid the error happens during the url parsing
# 			while True:
# 				try:
# 					feed = feedparser.parse(feedurl)
# 					break
# 				except:
# 					print 'Parse feed Error... Wait 30 seconds to continue...'
# 					sleep(30)

# 			for item in feed['items']:
# 			    url =  item.guid
# 			    if url not in dictList:	# new links 
# 				    if (removeLink not in url):	# if it is not a video link
# 				    	if buildArticleTables(url): # Also if the article use the disqus system
# 				    		writeDictFile(url)	# write the Link
# 				    		dictList.append(dictList)

# 				    		# update the dictionary list and count 
# 				    		dictList.append(url) # add the link to the link list
# 				    		count += 1
# 				    		sleep(2)
				    		
# 		print 'Sleeping for 15 minutes......'
# 		sleep(900)
