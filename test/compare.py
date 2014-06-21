'''
Created on June 20, 2014

@author Rainicy
'''
import json


def main():
	'''
	Description:
		Crawling the comments from the same url: {http://www.cnn.com/2014/05/28/politics/phoenix-va-hospital/index.html}
		for twice: 
			1) first time I got Comments1, which is in './data/'. Total number of comments: 12,335.
			2) second time I got Comments2, which is in the same folder. Total number of comments: 10,431.
		This code is for filtering the different comments in Comments1 but not in Comments2.

		Output:
			1) diffComments: in json format, which is in 'output' folder.
			2) diffMessages: just raw_message, which is in the same folder.
	'''
	with open('./data/Comments2', 'r') as file:
		J1 = []
		lines = file.readlines()
		for line in lines:
			j = json.loads(line)
			if j['id'] not in J1:
				J1.append(j['id'])
		file.close()

	# compare and filter the deleted comments from Comments2
	out = open('./output/diffComments', 'w')
	out1 = open('./output/diffMessages', 'w')
	with open('./data/Comments1', 'r') as file2:
		lines2 = file2.readlines()
		count = 0
		for line in lines2:
			j = json.loads(line)
			if j['id'] not in J1:
				out.write(line)
				out1.write(j['raw_message'].encode('ascii', 'ignore') + '\n')
		file2.close()

	out.close()

if __name__ == '__main__':
	main()