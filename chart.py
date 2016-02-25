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

def create_labels_values(school_name, data_labels, renamed_labels = {}):
    
    school_data = school_info.create_school_dictionary()
    sample_school = school_data[school_name]
    labels = []
    values = []

    for key in sample_school.keys():
        if key in data_labels:
            if key in renamed_labels.keys():
                new_key = renamed_labels[key]
                labels.append(new_key)
            else:
                labels.append(key)
            values.append(sample_school[key])

    return labels, values, sample_school


# Create expenditure pie charts
def expenditure_pie(school_name):
    Expenditure_Cat = set(['Admin Salary & Benefits', \
                      'Operational Expenses', 'Teacher Salary & Benefits',\
                      'Pensions', 'Capital Expenses', 
                      'Instructional-Related Expenses'])
    Expenditure_Cat_Unknown = set(['Unknown','#N/A'])
    Expenditure_Cat_Rename = {'Operational Expenses': 'Operations', \
                              'Capital Expenses':'Capital', \
                              'Instructional-Related Expenses': 'Instructional-Related'}

    labels, values, sample_school = create_labels_values(school_name, Expenditure_Cat, \
                     renamed_labels = Expenditure_Cat_Rename)
    
    # Grouping all 'unknown' or '#N/A' categories together
    unknown_sum = 0
    for key in sample_school.keys():
        if key in Expenditure_Cat_Unknown:
            unknown_sum = unknown_sum + sample_school[key]
    labels.append('Unknown')
    values.append(unknown_sum)

    # Creating chart
    title = 'Expenditures: {0} \n Total: ${1}' .format(school_name, 
        "{:,.0f}".format(sample_school['total_expend']))
    
    fig = {
    'data': [{'labels': labels, 'values': values, 'type': 'pie'}],
    'layout': {'title': title}}

    url = py.plot(fig, filename='Pie Chart Example')


def demographic_bar(school_name):
    ethnicity_cat = set(['asian', 'white', 'african', 'hispanic', 'multi'])
    ethnicity_cat_rename = {'asian': 'Asian', \
                            'white': 'Caucasian', \
                            'african': 'African American', \
                            'hispanic':' Hispanic',\
                            'multi': 'Multi-racial'}
    labels, values, sample_school = create_labels_values(school_name, ethnicity_cat,\
                                    renamed_labels = ethnicity_cat_rename)

    trace1 = [go.Bar(x = labels,y = values)]

    layout = go.Layout(yaxis = dict(title = 'Percentage (%)'))

    fig = go.Figure(data = trace1, layout = layout)

    url = py.plot(fig, filename='Bar Chart Example')
