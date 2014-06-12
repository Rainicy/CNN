'''
Created on June 8, 2014

@author Rainicy
'''

import time
from datetime import datetime

from Comments import *
from Log import *


def main():
	'''
	Description: Crawling the comments
	'''

	LogName = '../log/comments.log'

	writeStartTime(LogName, datetime.now())
	# Step 0. Crawling cooments, which is not in News.log
	## News IDs arange (1 - 957)

	## Read urls following line's number(ID) in Dict_Links
	print 'Reading URLs from Dict_Links......'
	with open('../dict/Dict_Links', 'r') as file:
		lines = file.readlines()
		file.close()

	## Crawling the comments
	print 'Starting Crawling Comments......'
	for i in range(957):
		print str(i+1) + ' : in processing...'
		url = lines[i].split('\n')[0]
		startTime = datetime.now()
		# write the comments to the file
		fileName = '../data/comments/' + str(i+1)
		count = writeComments(fileName, url)
		# write the log to comments.log
		writeCommentsLog(LogName, str(i+1), startTime, datetime.now(), count)



	# Step 1. Read the last time line number from News.log


if __name__ == '__main__':
	main()