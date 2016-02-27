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
                rv.append( [ float(row[4]), float(row[5]) ] )
    return rv    