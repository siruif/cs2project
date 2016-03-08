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

	s1 = "SELECT g.CPSUnit, g.FullName, g.SchoolType, g.Latitude, g.longitude, g.AttendingGrades, g.StreetNumber, g.StreetDirection, g.StreetName, \
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
	ATTENDGRADES = 5
	STNUM = 6
	STDIR = 7
	STNAME = 8
	EXPEND = 9
	CATEG = 10
	RATING = 11
	POINTS = 12
	MATH_GROWTH = 13
	RDG_GROWTH = 14
	TOTALNO = 15
	LUNCH = 16
	SPED = 17
	WHITE = 18
	AFRICAN = 19
	HISPANIC = 20
	MULTI = 21
	ASIAN = 22

	school_dictionary = {}

	for each in school_information:
		
		key = each[NAME]
		
		if key not in school_dictionary:
			school_dictionary[key] = {}
			school_dictionary[key]['unit'] = each[UNIT]
			school_dictionary[key]['type'] = each[TYPE]
			school_dictionary[key]['lat'] = each[LAT]
			school_dictionary[key]['lon'] = each[LON]
			school_dictionary[key]['attending_grades'] = each[ATTENDGRADES]
			if each[STNUM] == "" and each[STDIR] == "" and each[STNAME] == "":
				school_dictionary[key]['address'] = "Not Available"
			else:
				school_dictionary[key]['address'] = str(each[STNUM]) + " " + each[STDIR] + " " + each[STNAME]
			category = each[CATEG]
			school_dictionary[key][category] = each[EXPEND]
			school_dictionary[key]['total_expend'] = each[EXPEND]
			school_dictionary[key]['perf_rating'] = each[RATING]
			school_dictionary[key]['perf_points'] = each[POINTS]
			totalno_mod = each[TOTALNO].replace(",","")
			school_dictionary[key]['total_students'] = totalno_mod
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

#Inserted by Turab, creating the school dictionary as a global so that we dont have
#to create it again and again indifferent functions
SCHOOLS_DATA = create_school_dictionary()



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
		distance = find_radius_helper(lat1, lon1, lat2, lon2)
		distance_dict[school]['distance'] = distance
		distance_dict[school]['lat'] = lat2
		distance_dict[school]['lon'] = lon2
	
	return distance_dict

def find_radius_helper(lat1, lon1, lat2, lon2):
	'''
	Calculates the miles distance between two points, assuming the radius of earth is 3959 miles.
	http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
	'''
	lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2]) 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 
	mile = 3959 * c
	return mile

def find_neighbor_schools(location, radius):
	'''
	for a given (lat, lon) and a radius in miles, returns a list of school that is in the radius
	'''
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

def in_range(ulocation, slocation, radius):
	'''
	For a given user's location (ulat, ulon), the schools's location (slat, slon),
	returns True of the distance between the school and the user's location is less
	than or equal to the radius.
	'''
	(ulat, ulon) = ulocation
	(slat, slon) = slocation
	distance = find_radius_helper(ulat, ulon, slat, slon)
	return distance <= radius

#inserted by Turab
def build_context_explore():
	'''
	Given the school dictionary, returns information about the school to be displayed
	in the explore page. This function is called in the view.py file when the explore
	page is being redered
	'''
	rv = []

	for key in SCHOOLS_DATA.keys():
		rv.append ( [key, SCHOOLS_DATA[key]['address'], SCHOOLS_DATA[key]['attending_grades'],\
		SCHOOLS_DATA[key]['type'], SCHOOLS_DATA[key]['total_students'],SCHOOLS_DATA[key]['lat'],\
		SCHOOLS_DATA[key]['lon'] ] )
	
	return rv

def school_names():
	'''
	Return all the schoold names in the data. This function is called from the forms.py file
	to populate the choice fields
	'''

	return sorted(SCHOOLS_DATA.keys())





