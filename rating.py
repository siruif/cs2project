import sqlite3
import math
import csv
connection = sqlite3.connect("EducationData.db")
cursor = connection.cursor()


s2 = "SELECT g.CPSUnit, p.SQRPRating, sum(e.Expenditures) as totalexpend, l.Total, g.FullName,  g.Latitude, g.longitude \
FROM general AS g JOIN expenditure AS e ON g.CPSUnit = e.CPSUnit \
JOIN lunch AS l ON l.CPSUnit = g.CPSUnit JOIN performance AS p ON p.CPSUnit = g.CPSUnit \
GROUP BY g.FullName;"
#s2 is for heat map

rating_data = cursor.execute(s2)


UNIT = 0
RATING = 1
EXPEND = 2
TOTAL = 3
NAME = 4
LAT = 5
LON = 6
rate_criteria = {"Level 1+": 90, "Level 1":70, "Level 2+": 50, "Level 2": 40, "Level 3": 20, "Inability to Rate": None}
#reference: http://cps.edu/SiteCollectionDocuments/SQRP_one_pager.pdf
#for Level 3: assign 20

rating_list = []

for each in rating_data:
	full_name = each[NAME]
	rating = each[RATING]
	score = rate_criteria[rating]

	expend = each[EXPEND]
	expend = float(expend)

	total = each[TOTAL]
	total = total.replace(",","")
	total = float(total)

	school=[]
	school.append(full_name)
	school.append(each[LON])
	school.append(each[LAT])

	if score!=None:
		if expend >0:
			score = round(math.log(score / (expend/total)),2)
	else:
		score = None
	school.append(score)
	rating_list.append(school)

for each in rating_list:
	print(each)


with open('scores.csv', 'w') as outcsv:   
    #configure writer to write standard csv file
    writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerow(['full_name', 'lon', 'lat', 'score'])
    for item in rating_list:
        #Write item to outcsv
        writer.writerow([item[0], item[1], item[2], item[3]])


connection.close()