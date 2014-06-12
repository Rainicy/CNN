'''
Created on June 6, 2014

@author Rainicy
'''

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
