from bs4 import BeautifulSoup
import feedparser
import urllib2
import re
import time
from socket import error as SocketError


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

def writeArticle(url, title, date, text):
	'''function for writing article's information '''
	fileName = '../dict/Articles'
	with open(fileName, 'a') as file:
		file.write(url + '\t' + title + '\t' + date + '\t' + text + '\n')
		file.close()

def buildArticleTables(url):
	ifContainsDisqus = False
	keyword = 'disqus_identifier'
	headers = {'User-Agent' : 'Mozilla/5.0'}
	req = urllib2.Request(url, None, headers)
	while True:
		try:
			content = urllib2.urlopen(req).read()
			break
		except SocketError:
			print "Waiting for 5 seconds until you can send the request again..."
			time.sleep(5)
			continue
	soup = BeautifulSoup(content)
	script = soup.script.string
	# if it is a disuqs system
	if keyword in script:
		print str(count) + '. ' + soup.title.string
		# print url
		ifContainsDisqus = True
		r_author = re.compile(r'cnnAuthor="(.*)",')	# regex author 
		r_publish_date = re.compile(r'publish_date: "(.*)",')	# regex publish date
		author = re.search(r_author, script)
		date = re.search(r_publish_date, script)
		# write the URL-Author to the file
		writeAuthors(url, author.group(1))
		# write the Article 
		text = ''
		for t in soup.find_all('p'):
			text += t.get_text().encode('ascii', 'ignore') + ' '
		writeArticle(url, soup.title.string, date.group(1), text)

	else:
		ifContainsDisqus = False
	# print soup.prettify()
	return ifContainsDisqus

if __name__ == '__main__':
	# Feed from CNN politics
	policyURL = "http://rss.cnn.com/rss/cnn_allpolitics.rss"

	# Remove all the links of video 
	removeLink = 'http://www.cnn.com/video/'
	KEYWORD = 'politics'
		
	# List for the links, which already have been collected
	dictList = []


	count = 1
	while True:
		feed = feedparser.parse(policyURL)
		for item in feed['items']:
		    url =  item.guid
		    if url not in dictList:	# new links 
			    if (removeLink not in url) and (KEYWORD in url):	# if it is not a video link
			    	if buildArticleTables(url): # Also if the article use the disqus system
			    		writeDictFile(url)	# write the Link
			    		dictList.append(dictList)
			    		# raw_input()
			    		dictList.append(url) # add the link to the link list
			    		count += 1
		time.sleep(1800)

    
    
