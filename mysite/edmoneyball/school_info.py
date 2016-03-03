import sqlite3
from math import *
import operator
import csv

def create_school_dictionary():
	'''
	Constructs a dictionary that stores information of the school. The key is the school name.
	'''
	db_path = 'edmoneyball/EducationData.db'
	csv_path = 'edmoneyball/UpdatedLocations.csv'
	connection = sqlite3.connect(db_path)
	cursor = connection.cursor()

	s1 = "SELECT g.CPSUnit, g.FullName, g.SchoolType, g.Latitude, g.longitude, \
	SUM(e.Expenditures) AS expend, e.CategoriesName, \
	p.SQRPRating, p.SQRPTotalPointsEarned, p.`NationalSchoolGrowthPercentile-Maths-Score`, p.`NationalSchoolGrowthPercentile-Reading-Score`, \
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
	MATH_GROWTH = 9
	RDG_GROWTH = 10
	TOTALNO = 11
	LUNCH = 12
	SPED = 13
	WHITE = 14
	AFRICAN = 15
	HISPANIC = 16
	MULTI = 17
	ASIAN = 18

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
			school_dictionary[key]['total_students'] = each[TOTALNO]
			school_dictionary[key]['free_red_lunch'] = each[LUNCH]
			school_dictionary[key]['special_educ'] = each[SPED]
			school_dictionary[key]['white'] = each[WHITE]
			school_dictionary[key]['african'] = each[AFRICAN]
			school_dictionary[key]['hispanic'] = each[HISPANIC]
			school_dictionary[key]['multi'] = each[MULTI]
			school_dictionary[key]['asian'] = each[ASIAN]
			school_dictionary[key]['math_growth'] = each[MATH_GROWTH]
			school_dictionary[key]['rdg_growth'] = each[RDG_GROWTH]
		else:
			category = each[CATEG]
			school_dictionary[key][category] = each[EXPEND]
			school_dictionary[key]['total_expend'] += each[EXPEND]


	connection.close()
	with open(csv_path) as csvfile:
		locationreader = csv.reader(csvfile, delimiter = ',')
		next(locationreader)
		for row in locationreader:
			school_name = row[0]
			if school_name in school_dictionary:
				updated_lat = row[2]
				updated_lon = row[3]
				school_dictionary[school_name]['lat'] = updated_lat
				school_dictionary[school_name]['lon'] = updated_lon

	return school_dictionary

def get_radius(lat1, lon1):
	'''
	Constructs a dictionary of dictionaries, key is the school name and value is a dictionary
	 with distance lat1 lon1; the key names are distance, lat and lon respectively
	'''
	distance_dict = {}
	school_dictionary = create_school_dictionary()
	for school in school_dictionary:
		distance_dict[school] = {}
		lon2 = float(school_dictionary[school]['lon'])
		lat2 = float(school_dictionary[school]['lat'])
		distance = find_radius_helper(lon1, lat1, lon2, lat2)
		distance_dict[school]['distance'] = distance
		distance_dict[school]['lat'] = lat2
		distance_dict[school]['lon'] = lon2
	
	return distance_dict


def find_radius_helper(lon1, lat1, lon2, lat2):
	'''
	calculates the miles distance between two points, assuming the radius of earth is 3959 miles.
	http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
	'''
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 
	mile = 3959 * c

	return mile

def find_neighbor_schools(location, radius):
	(ulat, ulon) = location
	distance_dict = get_radius(ulat, ulon)
	schools_in_range = []
	for key in distance_dict:
		if distance_dict[key]['distance'] <= radius:
			school=[]
			school.append(key)
			school.append(float(distance_dict[key]['lat']))
			school.append(float(distance_dict[key]['lon']))
			schools_in_range.append(school)
	return schools_in_range

#inserted by Turab
def school_names():
	'''
	Given the school dictionary, just returns the school names
	'''
	school_dictionary = create_school_dictionary()

	return sorted(school_dictionary.keys())

find_neighbor_schools((41.9449905,-87.6843248),1)