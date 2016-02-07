##CHICAGO PUBLIC SCHOOL - BUDGET, PERFORMANCE, AND OPTIONS##

##Team: EdMoneyBall##
##Team Members: Sirui Feng, Turab Hassan, & Vi Nguyen
##CS122 Project, University of Chicago

def school_rank(criteria_from_ui, dictionary_school_info):
'''
Takes in the criteria and value score from users, and a dictionary of 
school information to calculate a ranking of recommended school based 
on user's preferences

Assumes criteria_from_ui is in format of:
{'Diversity': [A, B], 'Free_Reduced_Lunch': [C, D], 'English_Learners': [E, F], 'Special Ed': [G, H], 'Performance': [I, J]}

Assumes dictionary_school_info is in format of:
{School ID: {'Diversity': A, 'Free_Reduced_Lunch': B, 'English_Learners': C}...}
'''
total_score = 0
max_score = 0

for values in criteria_from_ui.values():
    total_score = total_score + values[1]

for values in criteria_from_ui.values():
    #max proportional score
    max_score = (values[1] / total_score)

    for school in dictionary_school_info.keys():
        if values[1] != 0:
            if school[values] = key:
                if school[key] >= criteria_from_ui[key][0] dict.setdefault(key, default=None)
                    school['score'] = school.setdefault('score', default = 0) + max_score
                else:
                    school['score'] = school.setdefault('score', default = 0) + (max_score * (key[1] / criteria_from_ui[key][0]))






