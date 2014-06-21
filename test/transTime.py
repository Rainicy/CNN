'''
Created on June 20, 2014

@author Rainicy
'''
from datetime import *


def main():
	'''
	Description: 
		To test the comments replying gaps. 

		Input:
			60 News comments replies times in folder './timestamps'.

		Output:
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
	main()
