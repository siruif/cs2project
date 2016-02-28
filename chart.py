import school_info
import matplotlib.pylab as plt
import numpy as np
import plotly.plotly as py
import plotly.tools as tls 
from plotly.graph_objs import *
import plotly.graph_objs as go
py.sign_in('vi-tnguyen', '2j59j4yh6y')

# These are the "Tableau 20" colors as RGB.    
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), 
             (255, 187, 120), (44, 160, 44), (152, 223, 138), 
             (214, 39, 40), (255, 152, 150), (148, 103, 189), 
             (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), 
             (199, 199, 199), (188, 189, 34), (219, 219, 141), 
             (23, 190, 207), (158, 218, 229)] 

# Scale the RGB values to the [0, 1] range, which is the format 
# matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)

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

# Pulls in data dictionary of school data and creates a list of 
# variables for which we are bringing in data
district_data = school_info.create_school_dictionary()

# Creates a list of variables for which we are bringing in data.
# Any school name would work here
variables = list(district_data['Wolfgang A Mozart Elementary School'].keys())
variables_charts = frlunch_cat | Expenditure_Cat | ethnicity_cat | \
                   Expenditure_Cat_Unknown


# Calculate district averages for baseline in charts
def district_avg():
    district_avg = []
    for var in variables:
        total = 0
        if var in variables_charts:
            for school in district_data.keys():
                #print('school:', school, 'var:', var)
                if var in district_data[school].keys():
                    school_value = district_data[school][var]
                    if type(school_value) is str:
                        school_value = school_value.strip('%')
                    total = total + float(school_value)
                    avg = total / len(district_data)
            district_avg.append((var, avg))

    return district_avg


def create_labels_values(school_name, data_labels, renamed_labels = {}):
    school_data = district_data[school_name]
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
def expenditure_pie(school_name):

    labels, values, school_data = create_labels_values(school_name, Expenditure_Cat, \
                     renamed_labels = Expenditure_Cat_Rename)

    # converting values to numpy arrays to get spend per student
    values = np.array(values)
    students = school_data['total_students']
    students = students.strip(',')
    students = int(students)
    values = values / students
    values = values.tolist()
    
    # Grouping all 'Unknown' or '#N/A' categories together
    unknown_sum = 0
    for key in school_data.keys():
        if key in Expenditure_Cat_Unknown:
            unknown_sum = unknown_sum + school_data[key]
    labels.append('Unknown')
    values.append(unknown_sum)

    # Creating chart
    title = 'Expenditures : {0} \n Total: ${1}' .format(school_name, 
        "{:,.0f}".format(school_data['total_expend']))
    fig = {
    'data': [{'labels': labels, 'values': values, 'type': 'pie'}],
    'layout': {'title': title}}

    url = py.plot(fig, filename='Pie Chart: Expenditure', auto_open = False)
    #py.image.save_as(fig, 'charts/expenditure_pie.png')

    return url, labels, values


def demographic_bar(school_name):
    labels, values, school_data = create_labels_values(school_name, ethnicity_cat,\
                                    renamed_labels = ethnicity_cat_rename)

    trace1 = [go.Bar(x = labels, y = values)]
    title = 'Ethnicity: {0} \n Total Students: {1}' .format(school_name, 
        "{:,.0f}".format(int(school_data['total_students'])))
    layout = go.Layout(yaxis = dict(title = 'Percentage (%)'), \
             title = title)
    fig = go.Figure(data = trace1, layout = layout)

    url = py.plot(fig, filename='Bar Chart: Demographics', auto_open = False)
    #py.image.save_as(fig, 'charts/demographic_bar.png')

    return url, labels, values


def frlunch_pie(school_name):
    labels, values, school_data = create_labels_values(school_name,\
        frlunch_cat, frlunch_cat_rename)
    on_frlunch = values[0]        

    value_not_frlunch = 100.00 - on_frlunch
    labels.append('Not on Free/Reduced Lunch')
    values.append(value_not_frlunch)

    title = 'Income Indicator: {0}'.format(school_name)
    
    fig = {'data': [{'labels': labels, 'values': values, 'type': 'pie'}],
    'layout': {'title': title}}

    url = py.plot(fig, filename='Pie Chart: Income Indicator', auto_open = False)
    #py.image.save_as(fig, filename = 'charts/frlunch_pie.png')

    return url, labels, values

def compare(list_of_schools, function):
    # max number of schools to compare is 5
    list_traces = []
    print(list_of_schools)
    if len(list_of_schools) > 0:
        school_name = list_of_schools[0]
        url, labels, values = function(school_name)
        trace1 = go.Bar(x = labels, y = values, name = school_name)
        list_of_schools.remove(school_name)
        list_traces.append(trace1)
    
    if len(list_of_schools) > 0:
        school_name = list_of_schools[0]
        url, labels, values = function(school_name)
        trace2 = go.Bar(x = labels, y = values, name = school_name)
        list_of_schools.remove(school_name)
        list_traces.append(trace2)

    if len(list_of_schools) > 0:
        school_name = list_of_schools[0]
        url, labels, values = function(school_name)
        trace3 = go.Bar(x = labels, y = values, name = school_name)
        list_of_schools.remove(school_name)
        list_traces.append(trace3)

    if len(list_of_schools) > 0:
        school_name = list_of_schools[0]
        url, labels, values = function(school_name)
        trace4 = go.Bar(x = labels, y = values, name = school_name)
        list_of_schools.remove(school_name)
        list_traces.append(trace4)

    if len(list_of_schools) > 0:
        school_name = list_of_schools[0]
        url, labels, values = function(school_name)
        trace5 = go.Bar(x = labels, y = values, name = school_name)
        list_of_schools.remove(school_name)
        list_traces.append(trace5)

    data = list_traces
    layout = go.Layout(barmode='group')
    
    fig = go.Figure(data=data, layout=layout)
    url = py.plot(fig, filename='grouped-bar')


def expenditure_compare(list_of_schools):
    # max number of schools to compare is 5
    list_traces = []
    print(list_of_schools)
    if len(list_of_schools) > 0:
        school_name = list_of_schools[0]
        url, labels, values = expenditure_pie(school_name)
        trace1 = go.Bar(x = labels, y = values, name = school_name)
        list_of_schools.remove(school_name)
        list_traces.append(trace1)
    
    if len(list_of_schools) > 0:
        school_name = list_of_schools[0]
        url, labels, values = expenditure_pie(school_name)
        trace2 = go.Bar(x = labels, y = values, name = school_name)
        list_of_schools.remove(school_name)
        list_traces.append(trace2)

    if len(list_of_schools) > 0:
        school_name = list_of_schools[0]
        url, labels, values = expenditure_pie(school_name)
        trace3 = go.Bar(x = labels, y = values, name = school_name)
        list_of_schools.remove(school_name)
        list_traces.append(trace3)

    if len(list_of_schools) > 0:
        school_name = list_of_schools[0]
        url, labels, values = expenditure_pie(school_name)
        trace4 = go.Bar(x = labels, y = values, name = school_name)
        list_of_schools.remove(school_name)
        list_traces.append(trace4)

    if len(list_of_schools) > 0:
        school_name = list_of_schools[0]
        url, labels, values = expenditure_pie(school_name)
        trace5 = go.Bar(x = labels, y = values, name = school_name)
        list_of_schools.remove(school_name)
        list_traces.append(trace5)

    data = list_traces
    layout = go.Layout(barmode='group')
    
    fig = go.Figure(data=data, layout=layout)
    url = py.plot(fig, filename='grouped-bar')
    
