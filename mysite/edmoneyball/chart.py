from . import school_info
#import school_info
import matplotlib.pylab as plt
import numpy as np
import plotly.plotly as py
import plotly.tools as tls 
import plotly.graph_objs as go

#from plotly.graph_objs import *

#py.sign_in('vi-tnguyen', '2j59j4yh6y')
#py.sign_in('siruif', '1xbbym8vxv')
#py.sign_in('nvi613', 'dceant1x53')
#py.sign_in('turabhassan', 'qu73c973p4')
py.sign_in('sarahfsr', 'g263mhd6au')
# Key sets and dictionaries for dealing with expenditure data
Expenditure_Cat = set(['Admin Salary & Benefits', \
                  'Operational Expenses', 'Teacher Salary & Benefits',\
                  'Pensions', 'Capital Expenses', 
                  'Instructional-Related Expenses'])
Expenditure_Cat_Unknown = set(['Unknown','#N/A'])
Expenditure_Cat_Rename = {'Operational Expenses': 'Operations', \
                          'Capital Expenses':'Capital', \
                          'Instructional-Related Expenses': 'Instructional-Related'}

# Key sets and dictionaries for dealing with ethnicity data
ethnicity_cat = set(['asian', 'white', 'african', 'hispanic', 'multi'])
ethnicity_cat_rename = {'asian': 'Asian', \
                        'white': 'Caucasian', \
                        'african': 'African American', \
                        'hispanic':' Hispanic',\
                        'multi': 'Multi-racial'}

# Key sets and dictionaries for dealing with free, reduced lunch data
frlunch_cat = set(['free_red_lunch'])
frlunch_cat_rename = {'free_red_lunch': 'Free/Reduced Lunch'}

# Key sets and dictionaries for dealing with academic performance data
acad_perf_cat = set(['rdg_growth', 'math_growth'])
acad_perf_cat_rename = {'rdg_growth': 'Growth in Reading', 'math_growth': 'Growth in Math'}


# Pulls in data dictionary of school data and creates a list of 
# variables for which we are bringing in data
district_data = school_info.create_school_dictionary()

# Pulling in 'total students' to calculate expenditure per student
students = set(['total_students'])

# Pulls in 'total_expenditures' to get district avg
total_expend = set(['total_expend'])

# Creates a list of variables for which we are bringing in data.
# Any school name would work here
variables = list(district_data['Wolfgang A Mozart Elementary School'].keys())
variables_charts = frlunch_cat | Expenditure_Cat | ethnicity_cat | \
                   Expenditure_Cat_Unknown | students | total_expend | acad_perf_cat

# List of variables that will not be a number, to be used to deal with type incongruencies
non_num_var = set(['type', 'unit', 'perf_rating' ])
#print(district_data)


# Deal with type incongruencies
for school in district_data.keys():
    for var in district_data[school]:
        if var not in non_num_var: # Exclude processing of variables for which our data is not a number
            data_point = district_data[school][var]
            if type(data_point) is str:
                #print('string loop')
                data_point = data_point.replace(',', '')
                data_point = data_point.strip('%')
                data_point = float(data_point)
                district_data[school][var] = data_point
            #print('data_point: {}, type: {}'.format(data_point, type(data_point)))
#print(district_data)

# Calculate district averages for baseline in charts
def district_avg():
    district_avg = {}
    district_dict = {}
    for var in variables:
        total = 0
        if var in variables_charts:
            for school in district_data.keys():
                if var in district_data[school].keys():
                    #if var == 'total_students':
                        #print('school:', school, 'var:', var)
                    school_value = district_data[school][var]
                    total = total + school_value
                    avg = total / len(district_data)
            district_avg[var] = avg
    district_dict['district_avg'] = district_avg
    #print(district_dict)

    #print('testing')
    return district_dict


def create_labels_values(school_name, data_dictionary, data_labels, renamed_labels = {}):
    school_data = data_dictionary[school_name]
    labels = []
    values = []

    for key in school_data.keys():
        if key in data_labels:
            if key in renamed_labels.keys():
                new_key = renamed_labels[key]
                labels.append(new_key)
            else:
                labels.append(key)

            value_string = school_data[key]
            if type(value_string) is str:
                #print(value_string,  type(value_string))
                value_string = value_string.strip("%")
            values.append(float(value_string))

    return labels, values, school_data


# Create expenditure pie charts
def expenditure_pie(school_data, school_name, labels_school, values_school, labels_distr, values_distr):
    # Creating chart
    title = 'Total Expenditures Per Student: \n ${0}' .format("{:,.0f}".\
        format(school_data[school]['total_expend']))
    #fig = {'data': [{'labels': labels, 'values': values, 'type': 'pie', 'domain': {'x': [0, .48]}, \
    #'hole': .4}], 'layout': {'title': title}}

    fig = {"data": [{"values": values_school, "labels": labels_school, "domain": {"x": [0, .48]},\
            "name": school_name, "hoverinfo":"label+percent", "hole": .4, "type": "pie"}, \
            {"values": values_distr, "labels": labels_distr, "textposition":"inside",\
            "domain": {"x": [.52, 1]},"name": "District Average", "hole": .4, "type": "pie"}],\
            "layout": {"title": title, \
            "annotations": [{"font": {"size": 10}, "showarrow": False, 'text': 'School', "x": 0.20, \
            "y": 0.5}, {"font": {"size": 10}, "showarrow": False, "text": 'District', "x": 0.8, "y": 0.5}]}}

    url = py.plot(fig, filename='Pie Chart: Expenditure', auto_open = False)
    #py.image.save_as(fig, 'charts/expenditure_pie.png')

    return url


def expenditure_data(school_name, data_dictionary):

    labels, values, school_data = create_labels_values(school_name, data_dictionary, Expenditure_Cat, \
                     renamed_labels = Expenditure_Cat_Rename)

    # converting values to numpy arrays to get spend per student
    values = np.array(values)
    #print(values)
    students = school_data['total_students']
    #print(type(students))
    if students is str:
        students = students.replace(',', '')
    values = values / float(students)
    values = values.tolist()
    
    # Grouping all 'Unknown' or '#N/A' categories together
    unknown_sum = 0
    for key in school_data.keys():
        if key in Expenditure_Cat_Unknown:
            unknown_sum = unknown_sum + school_data[key]
        unknown_per_student = unknown_sum / float(students)
    labels.append('Unknown')
    values.append(unknown_per_student)

    return labels, values


def bar(school_name, data_dictionary, data_distr_avg, cat_dict, cat_dict_rename, chart_title):
    labels_school, values_school, school_data = create_labels_values(school_name, data_dictionary, cat_dict,\
                                    renamed_labels = cat_dict_rename)

    labels_distr, values_distr, district_data = create_labels_values('district_avg', data_distr_avg, \
                                                cat_dict, renamed_labels = cat_dict_rename)
    #print(labels_school, values_school)
    trace1 = go.Bar(x = labels_school, y = values_school, name = 'School')

    trace2 = go.Bar(x = labels_distr, y = values_distr, name = 'District Average')

    students = school_data['total_students']

    title = '{0}: {1} \n Total Students: {2}' .format(chart_title, school_name, 
        "{:,.0f}".format(float(students)))
    layout = go.Layout(yaxis = dict(title = 'Percentage (%)'), \
             title = title, barmode = 'group')

    data = [trace1, trace2]
    fig = go.Figure(data = data, layout = layout)

    url = py.plot(fig, filename = 'Bar Chart: {}'.format(chart_title), auto_open = False)
    #py.image.save_as(fig, 'charts/demographic_bar.png')

    return url


def frlunch_bar(school_name, data_dictionary, data_distr_avg):
    labels, values, school_data = create_labels_values(school_name, data_dictionary, \
        frlunch_cat, frlunch_cat_rename)
    on_frlunch = values[0]        
    labels = ['School']
    value_not_frlunch = data_distr_avg['district_avg']['free_red_lunch']
    labels.append('District Average')
    values.append(value_not_frlunch)

    title = 'Income Indicator: Percent on Free and Reduced Lunch'
    data = [go.Bar(x = labels, y = values)]
    layout = go.Layout(title = title)

    fig = go.Figure(data = data, layout = layout)
    url = py.plot(fig, filename = 'Bar Chart: Income Indicator', auto_open = False)
    #py.image.save_as(fig, filename = 'charts/frlunch_pie.png')

    return url

def bar_compare(school, cat_dict, cat_dict_rename, chart_title, data_dictionary, data_distr_avg):
    data_dictionary['District Average*'] = data_distr_avg['district_avg']
    if chart_title == 'Expenditures Per Student':
        labels, values = expenditure_data(school, data_dictionary)
        print(labels, values)
    else:
        labels, values, school_data = create_labels_values(school, data_dictionary, \
                                      cat_dict, cat_dict_rename)
    data = go.Bar(x = labels, y = values, name = school)
    return data

def compare(list_of_schools, cat_dict, cat_dict_rename, chart_title, data_dictionary, data_distr_avg):
    list_traces = []
    #print(list_of_schools)
    if 'District Average*' not in list_of_schools:
        list_of_schools.append('District Average*')
    for school in list_of_schools:
        #print(school)
        trace1 = bar_compare(school, cat_dict, cat_dict_rename,chart_title, data_dictionary, \
                            data_distr_avg)
        list_traces.append(trace1)
        #print(list_traces)

    data = list_traces
    layout = go.Layout(barmode = 'group', title = chart_title)
    
    fig = go.Figure(data = data, layout = layout)
    url = py.plot(fig, filename = 'grouped-bar {}'.format(chart_title), auto_open = False)
    
    return url
    #py.image.save_as(fig, filename = 'charts/compare2.png')


