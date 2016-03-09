import csv
from . import school_info, school_zone


def build_context_from_address(ulat, ulon, radius):
  '''
  Given the lat lon of the address user entered and the radius the user entered, return the 
  schools in the zone. This function is called from the views file to render the page when
  the user gives his/her address
  '''
  user_location = (ulat, ulon)

  schools_in_zone, zone, zone_cordinates = school_zone.school_in_zone(ulat, ulon, True)

  school_in_radius = school_info.schools_in_radius(schools_in_zone)

  #rv = school_in_radius
  
  return school_in_radius, zone, zone_cordinates

def extract_location():
    '''
    opens the cps.csv and extracts the locations and returns
    them
    '''

    rv = []
    with open( 'edmoneyball/cps.csv', newline='' ) as csvfile:
            locationreader = csv.reader(csvfile, delimiter=',')
            next(locationreader) #skipping first line
            for row in locationreader:
                rv.append( [row[2], float(row[4]), float(row[5]) ] )
    return rv    

def extract_location_network():
    '''
    open the edmoneyball/NetworkBoundaries.csv and extract the NetworkBoundaries
    locations as LatLons and returns them
    '''

    rv = []

    with open( 'NetworkBoundaries.csv', newline='' ) as csvfile:
            locationreader = csv.reader(csvfile, delimiter=',')
            print (next(locationreader)[0])
            #print (next(locationreader)) #skipping first line
            for row in locationreader:
                for value in range(len(row)):
                    print (row[value])
            #    print(row)
                #rv.append( [row[2], float(row[4]), float(row[5]) ] )
    return rv        
    