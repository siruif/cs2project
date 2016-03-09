##CHICAGO PUBLIC SCHOOL - BUDGET, PERFORMANCE, AND OPTIONS##

##Team: EdMoneyBall##
##Team Members: Sirui Feng, Turab Hassan, & Vi Nguyen
##CS122 Project, University of Chicago

from . import school_info, chart, school_zone

## commented out to align with Django
#import school_info
#import chart


def clean_data(pref_criteria_from_ui):
    '''
    Cleans data from user interface and returns a new version in the form of a 
    simpler dictionary
    '''
    # Processing diversity component
    ethnicity = pref_criteria_from_ui['ethnicity']
    ethnicity_threshold = float(pref_criteria_from_ui['ethnicity_threshold'])
    clean_pref = {ethnicity: ethnicity_threshold}
    print(ethnicity, ethnicity_threshold)

    # Processing school type
    school_type = pref_criteria_from_ui['school_type']
    clean_pref = {'type': school_type}

    exceptions = ['ethnicity', 'school_type', 'location']

    for key in pref_criteria_from_ui.keys():
        criteria = pref_criteria_from_ui[key]
        # only pull in criteria that weren't left blank
        if (criteria != '') and (criteria != None): 
            # process items that are supposed to be floats
            if key not in exceptions:
                threshold = float(pref_criteria_from_ui[key])
                clean_pref[key] = threshold
            if key == 'location':
                clean_pref[key] = pref_criteria_from_ui[key]

    # sets the threshold for growth scores to be what the user set as the 
    # performance threshold
    clean_pref['rdg_growth'] = clean_pref['performance']
    clean_pref['math_growth'] = clean_pref['performance']

    return clean_pref


def school_rank(clean_pref):
    '''
    Takes in the cleaned preferences of the users from the user interface 
    and returns: 
        top_school_names - list of school names that meet the user's thresholds
            and/or is the best performing
        crit_met_indicator - boolean (True or False) to indicate whether the 
            schools we are recommending meet all the user's thresholds
        crit_not_met - list of the user's thresholds that were not met; will
            be blank if we are able to find matches

    Schools are recommended first by whether checking if they meet all the 
    user's specified thresholds; and then by how well the school is performing
    based on an average of reading and math scores
    '''

    # index that holds certain info
    threshold = 0 # for the clean_pref.keys()
    
    # holds a max of 5 schools
    top_matches = []
    
    schools_in_distance = []
    schools_in_network = []

    district_data = school_info.create_school_dictionary()

    # gets list of schools that fit radius parameters
    if 'location' in clean_pref.keys():
        lat, lon = clean_pref['location']
        user_radius = clean_pref['distance_threshold']
        neighbor_schools = school_info.find_neighbor_schools((lat, lon), user_radius)
        for val in neighbor_schools:
            schools_in_distance.append(val[0])  

        #generates schoos in zone of location
        schools_in_network = school_zone.school_in_zone(lat, lon)

    # go through all schools to find 2 scores, one to note whether the school met the minimum criteria, and 
    # the second to note how well they perform academically
    for school in district_data.keys():
        school_crit_met = 1 # assume they meet it until we come across a criteria where they don't
        school_rank = 0
        school_data = district_data[school]
        crit_not_met_list = []

        if schools_in_distance != []:
            if school not in schools_in_distance:
                school_crit_met = 0
                crit_not_met.append('distance')

        if schools_in_network != []:
            if (school not in schools_in_network) and (district_data[school]['type'] is not 'charter'):
                school_crit_met = 0
                crit_not_met.append('school network')

        for key in clean_pref.keys():
            if key in school_data.keys():
                if (type(clean_pref[key])) is str:
                    if school_data[key] != clean_pref[key]:
                        school_crit_met = 0
                        crit_not_met.append(key)
                else:
                    school_data[key] = school_data[key].strip('%')
                    if float(school_data[key]) < clean_pref[key]:
                        school_crit_met = 0
                        crit_not_met.append(key)
                school_rank = (float(school_data['rdg_growth']) + \
                    float(school_data['math_growth']))/2
        if len(top_matches) < 5:
            top_matches.append((school, school_crit_met, crit_not_met, \
                school_rank))
        else:
            for i in range(len(top_matches)):
                if (school_crit_met > top_matches[i][1]) or \
                    ((school_crit_met == top_matches[i][1]) and \
                    (school_rank > top_matches[i][2])) :
                    deranked_school = top_matches[i]
                    top_matches.remove(deranked_school)
                    top_matches.append((school, school_crit_met, crit_not_met, \
                        school_rank))
                    break
    
    # indicator that the returned schools met all the criteria
    if len(range(crit_not_met)) < 1:
                crit_met_indicator = False

    # rank the schools by best matches
    ranked_top_matches = sorted(top_matches, key = lambda x: (x[1], x[2]), \
        reverse = True)

    top_school_names = []
    for val in ranked_top_matches:
        top_school_names.append(val[0])
        # collects full list of criteria that were not met per school
        if val[2] != []:
            crit_not_met_full_list.append(val[2])

    print(top_school_names, crit_met_indicator, crit_not_met_full_list)
    return top_school_names, crit_met_indicator, crit_not_met_full_list




