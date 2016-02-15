import sqlite3
import math
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
		score = rate_criteria[rating]

		expend = each[EXPEND]
		expend = expend.replace(",","")
		expend = float(expend)

		total = each[TOTAL]
		total = total.replace(",","")
		total = float(total)

		rating_dict[key]["rating"] = rate_criteria[rating]
		rating_dict[key]["expenditure"] = expend
		rating_dict[key]["total"] = total

		print("the type of score is", type(score))
		print("the type of expend is", type(expend))
		print("the type of total is", type(total))
		print("the total is", total)
		print("the expenditure is:", expend)
		if score!=None:
			if expend >0:
			
				rating_dict[key]["scoreperexpend"] = math.log(score / (expend/total))
		else:
			rating_dict[key]["scoreperexpend"] = None
print(rating_dict)

connection.close()