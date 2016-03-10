# CS 122 Project: EdMoneyBall
# Vi Nguyen, Sirui Feng, Turab Hassan

from . import school_info
import matplotlib.pylab as plt
import numpy as np
import plotly.plotly as py
import plotly.tools as tls 
import plotly.graph_objs as go
## commented out to align with Django
#import school_info
#from plotly.graph_objs import *


# Sign-in accounts in case hit the 50/chart daily limit on plotly
# i.e. when request is "throtteled"
#py.sign_in('vi-tnguyen', '2j59j4yh6y')
#py.sign_in('siruif', '1xbbym8vxv')
#py.sign_in('nvi613', 'dceant1x53')
#py.sign_in('turabhassan', 'qu73c973p4')
#py.sign_in('turabhassan', 'qu73c973p4')
py.sign_in('sarahfsr', 'g263mhd6au')

## Reserve for demo
py.sign_in('vnguyen31', '4x69erhlu4')
py.sign_in('vi.nguyen61388', 'w8p15c6rq4')


# Key sets and dictionaries for processing and cleaning expenditure data
Expenditure_Cat = set(['Admin Salary & Benefits', \
                  'Operational Expenses', 'Teacher Salary & Benefits',\
                  'Pensions', 'Capital Expenses', 
                  'Instructional-Related Expenses'])
Expenditure_Cat_Unknown = set(['Unknown','#N/A'])
Expenditure_Cat_Rename = {'Operational Expenses': 'Operations', \
                          'Capital Expenses':'Capital', \
                          'Instructional-Related Expenses': 'Instructional-Related'}

# Key sets and dictionaries for processing and cleaning ethnicity data
ethnicity_cat = set(['asian', 'white', 'african', 'hispanic', 'multi'])
ethnicity_cat_rename = {'asian': 'Asian', \
                        'white': 'Caucasian', \
                        'african': 'African American', \
                        'hispanic':' Hispanic',\
                        'multi': 'Multi-racial'}

# Key sets and dictionaries for processing and cleaning free, reduced lunch data
frlunch_cat = set(['free_red_lunch'])
frlunch_cat_rename = {'free_red_lunch': 'Free/Reduced Lunch'}

# Key sets and dictionaries for processing and cleaning academic performance data
acad_perf_cat = set(['rdg_growth', 'math_growth', 'rdg_attainment', 'math_attainment'])
acad_perf_cat_rename = {'rdg_growth': 'Growth in Reading', 'math_growth': \
                        'Growth in Math', 'rdg_attainment': "Reading Attainment",\
                        'math_attainment': "Math Attainment"}

# Pulls in data dictionary of school data and creates a list of 
# variables for which we are bringing in data
district_data = school_info.create_school_dictionary()

# Pulls in 'total students' to calculate expenditure per student
students = set(['total_students'])

# Pulls in 'total_expenditures' to get district avg
total_expend = set(['total_expend'])

# Creates a list of variables for which we are bringing in data.
# Any school name would work here
variables = list(district_data['Wolfgang A Mozart Elementary School'].keys())
variables_charts = frlunch_cat | Expenditure_Cat | ethnicity_cat | \
                   Expenditure_Cat_Unknown | students | total_expend | acad_perf_cat

# List of variables that will not be a number, to be used to deal with type 
# incongruencies
non_num_var = set(['type', 'unit', 'perf_rating', 'address', 'attending_grades'])

# Deal with type incongruencies
for school in district_data.keys():
    for var in district_data[school]:
        # Exclude processing of variables for which our data is not a number
        if var not in non_num_var:
            data_point = district_data[school][var]
            if type(data_point) is str:
                data_point = data_point.replace(',', '')
                data_point = float(data_point)
                district_data[school][var] = data_point

# Calculate district averages for baseline in charts
def district_avg():
    '''
    Calcultates the district average for the expenditure, performance, and
    diversity measures based on the data dictionary of district data for the
    elementary schools that we called and processed above. 

    Returns a dictionary with 'district_avg' as the key and corresponding values 
    for each measure of expenditure category, performance growth levels for math 
    and reading, the number of students on free-and-reduced lunch, and the 
    average per ethnicity
    '''
    district_avg = {}
    district_dict = {}
    for var in variables:
        total = 0
        if var in variables_charts:
            for school in district_data.keys():
                if var in district_data[school].keys():
                    school_value = district_data[school][var]
                    total = total + school_value
                    avg = total / len(district_data)
            district_avg[var] = avg
    district_dict['district_avg'] = district_avg

    return district_dict


def create_labels_values(school_name, data_dictionary, data_labels, \
    renamed_labels):
    '''
    Creates a list of labels, and a corresponding list of values for plotting

    Inputs: 
        -school_name - school name, 
        -data_dictionary - dictionary of key data elements for elementary 
            schools in Chicago
        -data_labels - list of data elements we want to bring in
        -renamed_labels - dictionary of how we want the data elements to be \
            renamed for displaying (renamed_labels)--
    Outputs:
        labels - a list of labels, 
        values - a list of values for the charts, 
        school_data - dictionary with the school name as the key and dictionaries \
        for each data element we're bringing in.
    '''
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
            values.append(float(value_string))

    return labels, values, school_data


def expenditure_pie(school_data, school_name, labels_school, values_school, \
    labels_distr, values_distr):
    '''
    Charts the expenditure donut charts 
    Inputs:
        school_data - a data dictionary with a as the key and dictionaries for 
            each data element we're bringing
        school_name - name of a school
        labels_school - list of labels that go with the school data
        values_school - corresponding list of values that go with the school data
        labels_distr - list of labels that go with the district average data
        values_distr - corresponding list of values that go with the district 
            average data
    Outputs:
        a url where plotly is charting the donot charts of expenditure for the
            school, and district average (for comparison purposes)
    '''
    total_expend_per_stud = (school_data[school]['total_expend'] / \
        float(school_data[school]['total_students']))
    title = 'Total Expenditures Per Student: \n ${0}'.format("{:,.0f}".\
        format(total_expend_per_stud))
    fig = {"data": [{"values": values_school, "labels": labels_school, "domain":\
        {"x": [0, .48]},"name": school_name, "hoverinfo":"label+percent", "hole":\
        .4, "type": "pie"}, {"values": values_distr, "labels": labels_distr,\
        "textposition":"inside", "domain": {"x": [.52, 1]},"name": "District Average",\
        "hole": .4, "type": "pie"}], "layout": {"title": title, "annotations":\
         [{"font": {"size": 10}, "showarrow": False, 'text': 'School', "x": 0.20,\
         "y": 0.5}, {"font": {"size": 10}, "showarrow": False, "text": 'District',\
         "x": 0.8, "y": 0.5}]}}

    url = py.plot(fig, filename = 'Pie Chart: Expenditure', auto_open = False)

    return url


def expenditure_data(school_name, data_dictionary):
    '''
    Special function to process expenditure data so we can show it as 
    expenditure per student
    Inputs:
        school_name - name of the school that we're processing
        data_dictionary - dictionary of data for all elementary schools in the
            Chicago Public Schools
    Outputs:
        labels - labels to use for plotting
        values - values to use for plotting
    '''
    labels, values, school_data = create_labels_values(school_name, data_dictionary,\
        Expenditure_Cat, renamed_labels = Expenditure_Cat_Rename)

    # converting values to numpy arrays to get spend per student
    values = np.array(values)
    students = school_data['total_students']
    if type(students) is str:
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


def bar(school_name, data_dictionary, data_distr_avg, cat_dict, cat_dict_rename, \
    chart_title):
    '''
    Create bar charts for each school that is passed through, and 
    a chart of the district average for comparison purposes
    Inputs:
        school_name - name of school
        data_dictionary - dictionary of data for all elementary schools in the
            Chicago Public Schools
        data_distr_avg - data dictionary with 'district_avg' as key and average
            values for key data elements for the district
        cat_dict - dictionary of data elements we're using to build the bar plot
        cat_dict_rename - dictionary with each category as the keys and the renamed
            values 
        chart_title - title we want for the chart
    Outputs:
        -url of where plotly charted the graph
    '''
    
    labels_school, values_school, school_data = create_labels_values(school_name, \
        data_dictionary, cat_dict, renamed_labels = cat_dict_rename)
    trace1 = go.Bar(x = labels_school, y = values_school, name = 'School')

    labels_distr, values_distr, district_data = create_labels_values('district_avg', \
        data_distr_avg, cat_dict, renamed_labels = cat_dict_rename)
    trace2 = go.Bar(x = labels_distr, y = values_distr, name = 'District Average')

    students = school_data['total_students']
    title = '{0} \n Total Students: {2}' .format(chart_title, 
        "{:,.0f}".format(float(students)))
    layout = go.Layout(yaxis = dict(title = 'Percentage (%)'), \
             title = title, barmode = 'group')

    data = [trace1, trace2]
    fig = go.Figure(data = data, layout = layout)
    url = py.plot(fig, filename = 'Bar Chart: {}'.format(chart_title), \
        auto_open = False)

    return url


def frlunch_bar(school_name, data_dictionary, data_distr_avg):
    '''
    Create bar charts free_lunch data for each school that is passed through, and 
    a chart of the district average for comparison purposes
    Inputs:
        school_name - name of school
        data_dictionary - dictionary of data for all elementary schools in the
            Chicago Public Schools
        data_distr_avg - data dictionary with 'district_avg' as key and average
            values for key data elements for the district
    Outputs:
        -url of where plotly charted the graph    
    '''
    labels, values, school_data = create_labels_values(school_name, data_dictionary,\
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

    return url


def bar_compare(school_name, cat_dict, cat_dict_rename, chart_title, data_dictionary,\
    data_distr_avg):
    '''
    Create bar chart data for each school that we're comparing to in the compare
    function
    Inputs:
        school_name - name of school
        cat_dict - dictionary of data elements we're using to build the bar plot
        cat_dict_rename - dictionary with each category as the keys and the renamed
            values 
        chart_title - title we want for the chart
        data_dictionary - dictionary of data for all elementary schools in the
            Chicago Public Schools
        data_distr_avg - data dictionary with 'district_avg' as key and average
            values for key data elements for the district
    Outputs:
        -bar chart data that plotly can call on to chart    
    '''
    data_dictionary['District Average*'] = data_distr_avg['district_avg']
    if chart_title == 'Expenditures Per Student':
        labels, values = expenditure_data(school_name, data_dictionary)
    else:
        labels, values, school_data = create_labels_values(school_name, data_dictionary,\
                                      cat_dict, cat_dict_rename)
    data = go.Bar(x = labels, y = values, name = school_name)

    return data


def compare(list_of_schools, cat_dict, cat_dict_rename, chart_title, data_dictionary,\
     data_distr_avg):
    '''
    Generates charts based on user input to compare schools that are passed through
    Inputs:
        list_of_schools - names of school passed to us through user interface
        cat_dict - dictionary of data elements we're using to build the bar plot
        cat_dict_rename - dictionary with each category as the keys and the renamed
            values 
        chart_title - title we want for the chart
        data_dictionary - dictionary of data for all elementary schools in the
            Chicago Public Schools
        data_distr_avg - data dictionary with 'district_avg' as key and average
            values for key data elements for the district
    Outputs:
        -url where plotly charted the graph
    '''
    list_traces = []
    if 'District Average*' not in list_of_schools:
        list_of_schools.append('District Average*')
    for school in list_of_schools:
        trace1 = bar_compare(school, cat_dict, cat_dict_rename, chart_title, \
            data_dictionary, data_distr_avg)
        list_traces.append(trace1)

    data = list_traces
    layout = go.Layout(barmode = 'group', title = chart_title)
    
    fig = go.Figure(data = data, layout = layout)
    url = py.plot(fig, filename = 'grouped-bar {}'.format(chart_title), \
        auto_open = False)
    
    return url


