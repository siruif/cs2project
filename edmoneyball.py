##CHICAGO PUBLIC SCHOOL - BUDGET, PERFORMANCE, AND OPTIONS##

##Team: EdMoneyBall##
##Team Members: Sirui Feng, Turab Hassan, & Vi Nguyen
##CS122 Project, University of Chicago

def school_rank(pref_criteria_from_ui, dictionary_school_info):
'''
Takes in the criteria and value score from users, and a dictionary of 
school information to calculate a ranking of recommended school based 
on user's preferences

Assumes pref_criteria_from_ui is in format of:
{'Diversity': [A, B], 'Free_Reduced_Lunch': [C, D], 'English_Learners': [E, F], 'Special Ed': [G, H], 'Performance': [I, J]}


Assumes dictionary_school_info is in format of:
{School ID: {'Diversity': A, 'Free_Reduced_Lunch': B, 'English_Learners': C}...}

Notes:
-Converting all criteria thresholds to numbers to ensure that the assignment of school_score makes sense
'''

    denominator_score = 0

    # gets the score denominator
    for values in pref_criteria_from_ui.values():
        score_denominator = score_denominator + values[1]

    # go through all schools to find 2 scores, 1 to make sure the schools that meet all the criteria are ranked higher than those
    # that did not; and another score to rank the ones that meet all the criteria
    for school in dictionary_school_info.keys():
        school_score = 0
        school_score_second_rank = 0
        for key in pref_criteria_from_ui.keys():
            if key[1] != 0:
                school_score = school_score + min((school[key] / key[1]), key[1]) 
                school_score_second_rank =  school_score_second_rank + (school[key] * key[1])
        school['school_score'] = school_score
        school['school_score_second_rank'] = school_score_second_rank

    sorted(dictionary_school_info.items(), key = lambda x: x[1], reverse = True)






