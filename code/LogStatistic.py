'''
Created on July 12, 2014

@author Rainicy
'''

import re
from datetime import *

import json

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

def averageUsers():
	'''
	Description: Calculate the average active users replying comments per day.

	@input:
		news.log
		comments folder
	@print:
		Total Days:
		Total Active Users:
		Average Active Users Per Day:
	'''
	startTime = datetime(2014, 06, 07, 00, 00, 00)
	r_ids = re.compile(r'IDs: (.*)')

	with open('../log/news.log', 'r') as file:
		news_log_lines = file.readlines()
		file.close()

	count_by_day = []
	list_user_ids = []
	day = 0
	for line in news_log_lines:
		line = line.split('\n')[0]
		items = line.split('\t')
		time = datetime.strptime(items[0], "%Y-%m-%d %H:%M:%S.%f")
		delta_day = (time - startTime).days
		if (delta_day>=0) and (delta_day<=31):
			if items[1] == 'total: 0':
				continue
			else:
				ids = re.search(r_ids, items[2])
				ids = ids.group(1)
				if delta_day == day:
					list_user_ids = calTotalUsers(ids.split(','), list_user_ids)
				else:
					print str(day) + '\t' + str(len(list_user_ids))
					count_by_day.append(len(list_user_ids))
					day += 1
					list_user_ids = []
					list_user_ids = calTotalUsers(ids.split(','), list_user_ids)

	total = 0
	for c in count_by_day:
		total += c

	print "Total Days: {} \t Total Active Users: {}".format(len(count_by_day), total)
	print "Average Active Users Per Day: {}".format(total/len(count_by_day))



def calTotalUsers(ids, list_user_ids):
	'''
	Description: Given the news ids and append the active user ids to the 
				list_user_ids. And return the list_user_ids.
	@param:
		ids: news ids list
		list_user_ids: users ids list
	@return:
		list_user_ids: updated the active user ids list
	'''

	for id in ids:
		with open('../data/comments/' + id, 'r') as file:
			lines = file.readlines()
			file.close()
		count = 0
		for line in lines:
			comments = json.loads(line)
			try:
				user_id = comments['author']['id']
			except Exception:
				continue
			if user_id not in list_user_ids:
				list_user_ids.append(user_id)
	
	return list_user_ids

