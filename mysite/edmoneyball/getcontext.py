import csv


def extract_location():
    '''
    opens the cps.csv and extracts the locations and returns
    them
    '''

    rv={'lat':[],'lon':[]}
    with open('cps.csv', newline='') as csvfile:
            locationreader = csv.reader(csvfile, delimiter=',')
            next(locationreader) #skipping first line
            for row in locationreader:
                rv['lat'].append([row[4],row[5]])
        
    #print(rv)
    return rv    