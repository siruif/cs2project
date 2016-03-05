import csv


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
    