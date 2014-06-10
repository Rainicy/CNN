'''
Created on June 8, 2014

@author Rainicy
'''

from time import sleep
from datetime import datetime

from Comments import *

def main():
	'''
	Description: Crawling the comments.
	'''

	count = 1

	# List for the links, which already have been collected
	dictList = []
	dictFile = '../dict/Dict_Comments_Links'
	with open(dictFile, 'r') as file:
		lines = file.readlines()
		for line in lines: 
			dictList.append(line.split('\n')[0])
			count += 1
		file.close()

	# read the url from Articles file
	articleFile = '../dict/Articles'
	with open(articleFile, 'r') as file:

