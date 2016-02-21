import sqlite3
from math import *
import operator

def create_school_dictionary():
	'''
	Constructs a dictionary that stores information of the school. The key is the school name.
	'''
	connection = sqlite3.connect("EducationData.db")
	cursor = connection.cursor()

	s1 = "SELECT g.CPSUnit, g.FullName, g.SchoolType, g.Latitude, g.longitude, \
	SUM(e.Expenditures) AS expend, e.CategoriesName, \
	p.SQRPRating, p.SQRPTotalPointsEarned, \
	l.Total, l.FreeReducedPercent, l.SpEdPercent, \
	r.WhitePercentage, r.AfricanAmericanPercentage, r.HispanicPercentage, r.MultiRacialPercentage, r.AsianPercentage \
	FROM 'general' AS g JOIN 'expenditure' AS e ON g.CPSUnit = e.CPSUnit \
	JOIN performance AS p ON p.CPSUnit = e.CPSUnit \
	JOIN lunch AS l ON l.CPSUnit = p.CPSUnit \
	JOIN race AS r ON r.CPSUnit = l.CPSUnit \
	GROUP by g.FullName, e.CategoriesName;"
	#s1 is for building a dictionary for the comparison


	school_information = cursor.execute(s1)

	UNIT = 0
	NAME = 1
	TYPE = 2
	LAT = 3
	LON = 4
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
			school_dictionary[key]['unit'] = each[UNIT]
			school_dictionary[key]['type'] = each[TYPE]
			school_dictionary[key]['lat'] = each[LAT]
			school_dictionary[key]['lon'] = each[LON]
			category = each[CATEG]
			school_dictionary[key][category] = each[EXPEND]
			school_dictionary[key]['total_expend'] = each[EXPEND]
			school_dictionary[key]['perf_rating'] = each[RATING]
			school_dictionary[key]['perf_points'] = each[POINTS]
			school_dictionary[key]['total_students'] = each[TOTAL]
			school_dictionary[key]['free_red_lunch'] = each[LUNCH]
			school_dictionary[key]['special_educ'] = each[SPED]
			school_dictionary[key]['white'] = each[WHITE]
			school_dictionary[key]['african'] = each[AFRICAN]
			school_dictionary[key]['hispanic'] = each[HISPANIC]
			school_dictionary[key]['multi'] = each[MULTI]
			school_dictionary[key]['asian'] = each[ASIAN]
		else:
			category = each[CATEG]
			school_dictionary[key][category] = each[EXPEND]
			school_dictionary[key]['total_expend'] += each[EXPEND]


	connection.close()

	return school_dictionary

def get_radius(lon1, lat1):
	'''
	Constructs a dictionary, key is the school name and value is the distance to long1 lat1
	'''
	distance_dict = {}
	school_dictionary = create_school_dictionary()
	for school in school_dictionary:
		#print(school_dictionary[school])
		lon2 = float(school_dictionary[school]['lon'])
		#print(long2)
		lat2 = float(school_dictionary[school]['lat'])
		#print(lat2)
		distance = find_radius_helper(lon1, lat1, lon2, lat2)
		distance_dict[school] = distance
	#print(distance_dict)

	return distance_dict



def find_radius_helper(lon1, lat1, lon2, lat2):
	'''
	calculates the miles distance between two points, assuming the radius of earth is 3959 miles.
	http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
	'''
	#print(long1, lat1, long2, lat2)
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	# haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 
	mile = 3959 * c

	return mile

get_radius(-87.6297982, 41.8781136)