'''
Created on June 20, 2014

@author Rainicy
'''
from datetime import *
import matplotlib.pyplot as plt

def plotReplies():
	'''
	Description: Plot the comments replies timestamps curve. 

	@Input: 
		60 News comments replies times in folder './timestamps/'.
	@Output:
		60 Nes comments replies times png files in the folder './plots/'.
	'''
	for i in range(1, 61):
		# open one timestamp as the example.
		with open('./timestamps/' + str(i), 'r') as file:
			lines = file.readlines()
			listTimes = []
			for line in lines:
				line = line.split('\n')[0]
				line = line.replace('T', ' ')
				time = datetime.strptime(line, "%Y-%m-%d %H:%M:%S")
				listTimes.append(time)

			# sort the times
			listTimes.sort()
			# print listTimes
			startTime = listTimes[0]
			x = []
			y = []
			# go through the timestamps
			count = 0
			deltaSeconds = 3600
			for time in listTimes[1:-1]:
				# within the delta time, count++
				if (time - startTime).seconds <= deltaSeconds:
					count += 1
				# append the current time and the count to the x and y
				else:
					x.append(time)
					y.append(count)
					count = 0
					deltaSeconds += 3600
					if deltaSeconds > 86399:
						deltaSeconds %= 3600
						startTime = time

			# print len(x)
			plt.clf()
			plt.plot(x, y)
			# beautify the x-labels
			plt.gcf().autofmt_xdate()

			plt.savefig('./plots/' + str(i))
			# plt.show()



def estimateRelies():
	'''
	Description: 
		To test the comments replying gaps. 

		@Input:
			60 News comments replies times in folder './timestamps'.

		@Output:
			stattimes: #total comments | # within 7 days | # out 7 days | percent of 7 days
	'''
	totalDays = 0
	totalwithinDays = 0
	totalOutDays = 0

	out = open('./output/stattimes', 'w')
	for i in range(60):
		with open('./timestamps/' + str(i+1), 'r') as file:
			lines = file.readlines()
			listTimes = []
			for line in lines:
				line = line.split('\n')[0]
				line = line.replace('T', ' ')
				time = datetime.strptime(line, "%Y-%m-%d %H:%M:%S")
				listTimes.append(time)

			listTimes.sort()
			# count within 7 days and out 7 days
			days = len(listTimes)
			withinDays = 0
			outDays = 0
			for day in listTimes:
				deltaDay = (day - listTimes[0]).days
				if deltaDay <= 7:
					withinDays += 1
				else:
					outDays += 1

			out.write("total: {:>5}\tin: {:>5}\tout: {:>3}\tpercent: {}\n".format(days, withinDays, outDays, float(withinDays)/days))

			totalDays += days
			totalwithinDays += withinDays
			totalOutDays += outDays


	out.write("-----------------------------------------------------------------\n")
	out.write("TOTAL: {}\nIN: {}\nOUT: {}\nPERCENT: {}\n".format(totalDays, totalwithinDays, totalOutDays, float(totalwithinDays)/totalDays))

	out.close()

if __name__ == '__main__':
	plotReplies()
