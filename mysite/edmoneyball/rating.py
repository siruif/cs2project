# CS 122 Project: EdMoneyBall
# This file is used to fetch information from the database and transform 
# data to create a heatmap.
# Created by: Vi Nguyen, Sirui Feng, Turab Hassan

import sqlite3
import math
import csv

connection = sqlite3.connect("EducationData.db")
cursor = connection.cursor()


s1 = "SELECT g.CPSUnit, p.SQRPRating, sum(e.Expenditures) as totalexpend, \
l.Total, g.FullName,  g.Latitude, g.longitude \
FROM general AS g JOIN expenditure AS e ON g.CPSUnit = e.CPSUnit \
JOIN lunch AS l ON l.CPSUnit = g.CPSUnit \
JOIN performance AS p ON p.CPSUnit = g.CPSUnit \
GROUP BY g.FullName;"

rating_data = cursor.execute(s1)

UNIT = 0
RATING = 1
EXPEND = 2
TOTAL = 3
NAME = 4
LAT = 5
LON = 6
rate_criteria = {"Level 1+": 90, "Level 1":70, "Level 2+": 50, \
"Level 2": 40, "Level 3": 20, "Inability to Rate": None}
#reference: http://cps.edu/SiteCollectionDocuments/SQRP_one_pager.pdf
#for Level 3: assign 20

rating_list = []

for each in rating_data:
	full_name = each[NAME]
	rating = each[RATING]
	raw_score = rate_criteria[rating]

	expend = each[EXPEND]
	expend = float(expend)

	total = each[TOTAL]
	total = total.replace(",","")
	total = float(total)

	school = []
	school.append(full_name)
	school.append(each[LON])
	school.append(each[LAT])

	if raw_score != None:
		if expend > 0:
			adjusted_score = round(math.log(raw_score / (expend/total)),3)
	else:
		adjusted_score = None
	school.append(adjusted_score)
	school.append(raw_score)
	rating_list.append(school)

with open('scores.csv', 'w') as outcsv:   
    writer = csv.writer(outcsv, delimiter = ',', quotechar = '|', \
    	quoting = csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerow(['full_name', 'lon', 'lat', 'adjusted_score', \
    	'raw_score'])
    for item in rating_list:
        writer.writerow([item[0], item[1], item[2], item[3], item[4]])

connection.close()