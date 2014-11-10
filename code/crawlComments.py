'''
Created on June 8, 2014

@author Rainicy
'''

import re
from time import sleep
from datetime import datetime

from Comments import *
from Log import *


def main():
	'''
	Description: Crawling the comments
	'''

	LogName = '../log/comments.log'

	writeStartTime(LogName, datetime.now())
	## Read urls following line's number(ID) in Dict_Links
	print 'Reading URLs from Dict_Links......'
	with open('../dict/Dict_Links', 'r') as file:
		links = file.readlines()
		file.close()

	print 'Starting Crawling Comments......'
	# Step 0. Crawling cooments, which is not in News.log
	## News IDs arange (1 - 957)
	## Crawling the comments
	# for i in range(260, 957):
	# 	print str(i+1) + ' : in processing...'
	# 	url = links[i].split('\n')[0]
	# 	startTime = datetime.now()
	# 	# write the comments to the file
	# 	fileName = '../data/comments/' + str(i+1)
	# 	count = writeComments(fileName, url)
	# 	# write the log to comments.log
	# 	writeCommentsLog(LogName, str(i+1), startTime, datetime.now(), count)



	# Step 1: Read the last time line number in news.log
	lastLine = 0
	with open('../data/lineNumOfNews', 'r') as file:
		lines = file.readlines()
		lastLine = int(lines[-1].split('\n')[0])
		file.close()

	# print lastLine 
	# raw_input()
	# Step 2: Open news.log to find the line in last time
	with open('../log/news.log', 'r') as file:
		newsLogs = file.readlines()
		file.close()

	# Step 3: Seeking the logs until:
	####	1) no more lines
	####	2) the data gap is smaller than 7 days
	today = datetime.today()
	fmt = '%Y-%m-%d %H:%M:%S.%f'
	for i in range(lastLine, len(newsLogs)):	# condition 1)
		date, count, ids = newsLogs[i].split('\t')
		date = datetime.strptime(date, fmt)
		deltaDays = (today - date).days
		# if the deltaDays is in one week gap, crawl comments
		# and the total count news not equal to 0
		if deltaDays >= 7:
			# there exits news new
			if count != 'total: 0':
				# get the ids
				r_ids = re.compile(r'IDs: (.*)')
				ids = re.search(r_ids, ids.split('\n')[0])
				ids = ids.group(1)
				for cur_id in ids.split(','):
					print cur_id + ' : in processing...'
					url = links[int(cur_id)-1].split('\n')[0]
					startTime = datetime.now()
					# write the comments to the file
					fileName = '../data/comments/' + cur_id
					count = writeComments(fileName, url)
					# write the log to comments.log
					writeCommentsLog(LogName, cur_id, startTime, datetime.now(), count)
					sleep(3)

			# save current line number to the lineNumOfNews for next time.
			with open('../data/lineNumOfNews', 'a') as file:
				file.write(str(i)+'\n')
				file.close()
		# stop crawling comments
		else:
			# save current line number to the lineNumOfNews for next time.
			with open('../data/lineNumOfNews', 'a') as file:
				file.write(str(i)+'\n')
				file.close()
			break



if __name__ == '__main__':
	while True:
		print '------------Waiting for 3 hours-----------'
		sleep(10800)
		print '-------------Crawling Comments------------'
		main()