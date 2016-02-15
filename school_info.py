import sqlite3
connection = sqlite3.connect("EducationData.db")
cursor = connection.cursor()

s1 = "SELECT g.CPSUnit, g.SchoolName, g.SchoolType, g.Latitude, g.longitude, \
e.Expenditures, e.CategoriesName, \
p.SQRPRating, p.SQRPTotalPointsEarned, \
l.Total, l.FreeReducedPercent, l.SpEdPercent, \
r.WhitePercentage, r.AfricanAmericanPercentage, r.HispanicPercentage, r.MultiRacialPercentage, r.AsianPercentage \
FROM 'general' AS g JOIN 'expenditure' AS e ON g.CPSUnit = e.CPSUnit \
JOIN performance AS p ON p.CPSUnit = e.CPSUnit \
JOIN lunch AS l ON l.CPSUnit = p.CPSUnit \
JOIN race AS r ON r.CPSUnit = l.CPSUnit;"
#s1 is for building a dictionary for the comparison


school_information = cursor.execute(s1)

UNIT = 0
NAME = 1
TYPE = 2
LAT = 3
LONG = 4
EXPEND = 5
CATEG = 6
RATING = 7
POINTS = 8
TOTAL = 9
LUNCH = 10
SPED = 11
WHITE = 12
AFRICAN = 13
HISPANIC = 14
MULTI = 15
ASIAN = 16

school_dictionary = {}

for each in school_information:
	
	key = each[NAME]
	
	if key not in school_dictionary:
		school_dictionary[key] = {}
		school_dictionary[key]["unit"] = each[UNIT]
		school_dictionary[key]["type"] = each[TYPE]
		school_dictionary[key]["lat"] = each[LAT]
		school_dictionary[key]['long'] = each[LONG]
		school_dictionary[key]['expenditure'] = each[EXPEND]
		school_dictionary[key]['category'] = each[CATEG]
		#print(school_dictionary)
		school_dictionary[key]['rating'] = each[RATING]
		school_dictionary[key]['points'] = each[POINTS]
		school_dictionary[key]['total'] = each[TOTAL]
		school_dictionary[key]['lunch'] = each[LUNCH]
		school_dictionary[key]['special_educ'] = each[SPED]
		school_dictionary[key]['white'] = each[WHITE]
		school_dictionary[key]['african'] = each[AFRICAN]
		school_dictionary[key]['hispanic'] = each[HISPANIC]
		school_dictionary[key]['multi'] = each[MULTI]
		school_dictionary[key]['asian'] = each[ASIAN]



connection.close()