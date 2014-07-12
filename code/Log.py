'''
Created on June 6, 2014

@author Rainicy
'''

import re
from datetime import *

def writeLog(log, time, startCount, endCount):
	'''
	Description: Record a log in one-time crawling News Articles. 
				 And write it to the news.log

	@param: 
		log: the log file to keep record
		time: the starting time
		startCount: starting ID or Count
		endCount:	ending ID or Count
	@procedure:
		log: example {2014-06-06 14:21:29.907320 total: 1 IDs: 958}
	'''

	totalCount = endCount - startCount
	# the IDs for new Articles
	IDs = (',').join('%d' %i for i in range(startCount, endCount))

	with open(log, 'a') as file:
		file.write('%s\ttotal: %d\tIDs: %s\n'% (time, totalCount, IDs))
		file.close()

def writeCommentsLog(log, Id, startTime, endTime, count):
	'''
	Description: Record a log in one-time crawling Comments. 
				 And write it to the comments.log

	@param: 
		log: the log file to keep record
		Id: News' ID
		startTime: starting crawling comments time
		endCount: ending crawling comments time
	@procedure:
		log: example {1	2014-06-12 14:42:24.937278	2014-06-12 14:44:30.317590}
	'''	

	with open(log, 'a') as file: 
		file.write('ID: %s\ttotal: %d\t%s\t%s\t\n'% (Id, count, startTime, endTime))
		file.close()

def writeStartTime(log, startTime):
	'''
	Description: Record a log in one-time crawling Comments. 
				 And write it to the comments.log

	@param: 
		log: the log file to keep record
		startTime: starting crawling comments time
	@procedure:
		log: example {Start Crawling At: 2014-06-12 14:42:24.937278}
	'''	

	with open(log, 'a') as file: 
		file.write('Start Crawling At: %s\n'% startTime)
		file.close()

def averageComments():
	'''
	Description: Calculate the average comments per news.

	@input:
		comments.log
	@print
		Total News:
		Total Comments:
		Average Comments Per News:
	'''
	with open('../log/comments.log', 'r') as file:
		lines = file.readlines()
		file.close()

	count = 0
	total_count = 0
	r_total = re.compile(r'total: (.*)')
	for line in lines:
		line = line.split('\n')[0]
		items = line.split('\t')
		if len(items) == 5:
			total = re.search(r_total, items[1])
			total = int(total.group(1))
			total_count += total
			count += 1

	print "Total News: {} \t Total Comments: {}".format(count, total_count)
	print "Average Comments Per News: {}".format(total_count/count)


def averageNews():
	'''
	Description: Calculate how many news crawling for one day.

	@input:
		'news.log'
	@print:
		Total Days:
		Total News:
		Average News per Day:
	'''
	with open('../log/news.log', 'r') as file:
		lines = file.readlines()
		file.close()

	startTime = datetime(2014, 06, 07, 00, 00, 00)
	r_total = re.compile(r'total: (.*)')
	count_by_day = []
	day = 0
	count = 0
	for line in lines:
		line = line.split('\n')[0]
		items = line.split('\t')
		time = datetime.strptime(items[0], "%Y-%m-%d %H:%M:%S.%f")
		delta_day = (time - startTime).days
		if delta_day >= 0:
			if delta_day == day:
				total = re.search(r_total, items[1])
				total = int(total.group(1))
				count += total
			else:
				count_by_day.append(count)
				day += 1
				count = 0
				total = re.search(r_total, items[1])
				total = int(total.group(1))
				count += total

	total = 0
	for c in count_by_day:
		total += c
	print "Total Days: {} \t Total News: {}".format(len(count_by_day), total)
	print "Average News Per Day: {}".format(total/len(count_by_day))