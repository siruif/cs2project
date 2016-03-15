# CS 122 Project: EdMoneyBall
# Creates the Plotly charts
# Vi Nguyen, Sirui Feng, Turab Hassan
# All Original Code
# This files builds the information that needs to be passed to the html file

import urllib.parse
from . import school_info, school_zone, update_charts, geocode


def build_context_from_address(ulat, ulon):
  '''
  Given the lat lon of the address user entered return the schools in the zone.
  This function is called from the views file to render the page when
  the user gives his/her address
  Input: Lat Lon of the user as floats
  Output: Dictionary for the context.

  '''
  context = {}
  
  user_location = (ulat, ulon)

  schools_in_zone, zone, zone_cordinates = school_zone.school_in_zone(ulat, ulon, True)

  schools_data = school_info.schools_data(schools_in_zone)

  context['user'] = ['My Home', ulat, ulon]
  context['info'] = schools_data
  context['zone'] = zone_cordinates
  
  
  return context

def build_context_from_recommendation(data):
  '''
  Given the data the user entered in the recommendation form. Pass the data
  to the recommendation algorithm and return the context to render the data
  for html page
  Input: User data as a Dictionary with each key being the field as defined in
  the forms file
  Output: Dictionary of urls and school names
  '''
  
  if data['location'] != '':
    address = urllib.parse.quote_plus ( data['location'] )
    latlon = geocode.get_latlon(address)
    data['location'] = latlon
  
  data['ethnicity'] = data['ethnicity'].lower()

  urls, indicator, not_met = update_charts.compare_recommend\
  (True, pref_crit_from_ui = data)

  context = urls
  school_list = context['school']
  i = 0
  for each_school in school_list:
      if each_school != 'District Average*':
          key = "school" + str(i)
          context[key] = each_school
          i += 1

  if indicator:
    return indicator, context
  else:
    context['not_met'] = not_met
    return indicator, context

def build_context_from_comparison(data):
  '''
  Given the data the user entered to compare schools, build the context from
  the update charts file and return it.
  Input: User data as a Dictionary with each key being the field as defined in
  the forms file
  Output: Dictionary of urls and school names
  '''
  school_list = []
  for key in data.keys():
      if data[key] != '':
          school_list.append(data[key]) 
  context = update_charts.compare_recommend\
            (False, list_of_schools = school_list )            

  return context