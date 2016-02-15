import sqlite3
connection = sqlite3.connect("EducationData.db")
cursor = connection.cursor()


s2 = "SELECT g.CPSUnit, p.SQRPRating, e.Expenditures, l.Total \
FROM general AS g JOIN expenditure AS e ON g.CPSUnit = e.CPSUnit \
JOIN lunch AS l ON l.CPSUnit = g.CPSUnit JOIN performance AS p ON p.CPSUnit = g.CPSUnit;"
#s2 is for heat map

rating_data = cursor.execute(s2)

UNIT = 0
RATING = 1
EXPEND = 2
TOTAL = 3
rate_criteria={"Level 1+": 4.0, "Level 1":3.5, "Level 2+": 3.0, "Level 2": 2.0, "Level 3": 1.0, "Inability to Rate": None}
#reference: http://cps.edu/SiteCollectionDocuments/SQRP_one_pager.pdf
#for Level 3: assign 1

rating_dict = {}
for each in rating_data:
	key = each[UNIT]
	if key not in rating_dict:
		rating_dict[key]={}
		rating = each[RATING]
		rating_dict[key]["rating"] = rate_criteria[rating]
		rating_dict[key]["expenditure"] = each[EXPEND]
		rating_dict[key]["total"] = each[TOTAL]

connection.close()