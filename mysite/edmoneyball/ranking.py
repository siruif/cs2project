##CHICAGO PUBLIC SCHOOL - BUDGET, PERFORMANCE, AND OPTIONS##

##Team: EdMoneyBall##
##Team Members: Sirui Feng, Turab Hassan, & Vi Nguyen
##CS122 Project, University of Chicago

from . import school_info, chart 
#import school_info
#import chart


def clean_data(pref_criteria_from_ui):
    '''
    Cleans data from ui and returns a new version in the form of a simpler dictionary
    '''
    # Processing diversity component
    ethnicity = pref_criteria_from_ui['ethnicity']
    ethnicity_threshold = float(pref_criteria_from_ui['ethnicity_threshold'])
    clean_pref = {ethnicity: ethnicity_threshold}

    # Processing school type
    school_type = pref_criteria_from_ui['school_type']
    clean_pref = {'type': school_type}

    exceptions = ['ethnicity', 'school_type', 'location']

    for key in pref_criteria_from_ui.keys():
        criteria = pref_criteria_from_ui[key]
        if (criteria != '') and (criteria != None): # only pull in criteria that weren't left blank
            if key not in exceptions:
                #print(key)
                threshold = float(pref_criteria_from_ui[key])
                clean_pref[key] = threshold
            if key == 'location':
                clean_pref[key] = pref_criteria_from_ui[key]
    clean_pref['rdg_growth'] = clean_pref['performance']
    clean_pref['math_growth'] = clean_pref['performance']
    #print(clean_pref)
    return clean_pref


def school_rank(clean_pref):
    '''
    Takes in the criteria and value score from users, and a dictionary of 
    school information to calculate a ranking of recommended school based 
    on user's preferences

    Assumes pref_criteria_from_ui is in format of:
    {'Diversity': [A, B], 'Free_Reduced_Lunch': [C, D], 'English_Learners': [E, F], 'Special Ed': [G, H], 'Performance': [I, J]}


    Assumes dictionary_school_info is in format of:
    {School ID: {'Diversity': A, 'Free_Reduced_Lunch': B, 'English_Learners': C}...}


    pref_crit_from_ui = {'special_educ': 55.0, 'performance': 88.0, 'distance_threshold': 66.0, \
    'location': [41.9449905,-87.6843248], 'free_red_lunch': 56.0, 'type': 'charter','ethnicity': 'asian', \
    'ethnicity_threshold': 20.0}

    Notes:
    -Converting all criteria thresholds to numbers to ensure that the assignment of school_score makes sense
    '''

    # index that holds certain info
    threshold = 0 # for the clean_pref.keys()
    # holds a max of 5 schools
    top_matches = []
    schools_in_distance = []

    district_data = school_info.create_school_dictionary()

    # gets list of schools that fit radius parameters
    if 'location' in clean_pref.keys():
        user_location = clean_pref['location']
        user_radius = clean_pref['distance_threshold']
        neighbor_schools = school_info.find_neighbor_schools(user_location, user_radius)
        for val in neighbor_schools:
            schools_in_distance.append(val[0])  

    # go through all schools to find 2 scores, one to note whether the school met the minimum criteria, and 
    # the second to note how well they met each criteria
    for school in district_data.keys():
        school_crit_met = 1 # assume they meet it until we come across a criteria where they don't
        school_rank = 0
        school_data = district_data[school]

        if schools_in_distance != []:
            if (school not in schools_in_distance) and (district_data[school]['type'] is not 'charter'):
                school_crit_met = 0

        for key in clean_pref.keys():
            if key in school_data.keys():
                if (type(clean_pref[key])) is str:
                    if school_data[key] != clean_pref[key]:
                        school_crit_met = 0
                else:
                    school_data[key] = school_data[key].strip('%')
                    print(school_data[key])
                    if float(school_data[key]) < clean_pref[key]:
                        school_crit_met = 0
                    school_rank = school_rank + float(school_data[key])
        if len(top_matches) < 5:
            top_matches.append((school, school_crit_met, school_rank))
        else:
            for i in range(len(top_matches)):
                if (school_crit_met > top_matches[i][1]) or \
                ((school_crit_met == top_matches[i][1]) and (school_rank > top_matches[i][2])) :
                    deranked_school = top_matches[i]
                    top_matches.remove(deranked_school)
                    top_matches.append((school, school_crit_met, school_rank))
                    break

    ranked_top_matches = sorted(top_matches, key = lambda x: (x[1], x[2]), reverse = True)

    top_school_names = []
    for val in ranked_top_matches:
        top_school_names.append(val[0])

    return top_school_names




