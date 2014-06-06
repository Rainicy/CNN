'''
Created on June 6, 2014

@author Rainicy
'''

def writeLog(time, startCount, endCount):
	log = '../log/news.log'

	totalCount = endCount - startCount
	# the IDs for new Articles
	IDs = (',').join('%d' %i for i in range(startCount, endCount))

	with open(log, 'a') as file:
		file.write('%s\ttotal: %d\tIDs: %s\n'% (time, totalCount, IDs))
		file.close()
