import pandas
import sys
import numpy
import sympy
from collections import Counter


list_of_people = ['Naman', 'Sumit', 'Dev', 'Maytag', 'Sam', 'Buzz']
table = {}
money_spent_each = {}
for people in list_of_people:
	table[people] = {}
	money_spent_each[people] = numpy.float64(0)
	for peep in list_of_people:
		table[people][peep] = numpy.float64(0)

name_file = sys.argv[1]
df = pandas.read_excel(name_file)
data = df.as_matrix()

#numpy printing
float_formatter = lambda x: "%.2f" % x
numpy.set_printoptions(formatter={'float_kind':float_formatter})

#Assumptions
skip_index = 4
user_index = 3
payer_index = 2
cost_index = 1
item_index = 0

for point in data:	
	if point[skip_index] == 'y':		
		continue

	print ""

	item_name = point[item_index].strip()
	print "Item name: ", item_name

	#finding list of people who used the service
	users = point[user_index].split(',')
	#map(str.strip, users)
	print "These people are paying for it: ", users

	#finding who paid
	payer = point[payer_index].strip()
	print "This person paied for it: ", payer

	#finding cost of item	
	cost = numpy.float64(str(point[cost_index]).strip())
	per_cost = numpy.divide(cost , len(users))
	print "Per person is paying this: ", per_cost	

	#Adding cost to money_spent_each
	money_spent_each[payer] += cost

	for i in range(len(users)):
		users[i] = users[i].strip()
	for paying in users:
		if paying != payer:
			#Naman does not owe money. He has already paid himself
			table[paying][payer] += per_cost
			if table[paying][payer] > table[payer][paying]:
				table[paying][payer] -= table[payer][paying]
				table[payer][paying] = 0
			else:
				table[payer][paying] -= table[paying][payer]
				table[paying][payer] = 0				

#Cleaning table
#Dropping values less than 1
for (item, value) in table.items():
	money_spent_each[item] = (int(money_spent_each[item]*100) / 100.0)		
	for i in value.keys():		
		table[item][i] = (int(table[item][i]*100) / 100.0)		
		if (table[item][i]*100) < 1:
			table[item][i] = 0

#Printing table
print ""
for (item, value) in table.items():
	print item, " Owes:- "
	print ""
	total = 0
	for (i,v) in value.items():
		if v != 0:
			print i, " : ", v
			total += v
	print ""
	print "Total money = ", total
	print ""
	print ""

print "START OF OPTIMIZATION"
print ""
print ""
print ""

for people in list_of_people: #A
	for peep in list_of_people: #B
		#If A owes money to B
		if table[people][peep] != 0:
			#List of people A owes money to
			for person in table[people].keys(): #C
				#Making sure C is a unique person
				if person != people and person != peep:
					#If C owes money to B
					if table[person][peep] != 0:
						#A,C owe money to B
						#A owes money to C
						diff = min(table[people][person], table[person][peep])
						#C owes less to B
						table[person][peep] -= diff
						#A owes more to B
						table[people][peep] += diff
						#Now A ownes less to C
						table[people][person] -= diff		
#Printing table
print ""
for (item, value) in table.items():
	print item, " Owes:- "
	print ""
	total = 0
	for (i,v) in value.items():
		if v != 0:
			print i, " : ", v
			total += v
	print ""
	print "Total money = ", total
	print ""
	print ""

print money_spent_each
		
	