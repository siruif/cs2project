import school_info
import matplotlib.pylab as plt
import numpy as np

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

# Create expenditure pie charts
def expenditure_pie(school_name):
    Expenditure_Cat = set(['Admin Salary & Benefits', \
                      'Operational Expenses', 'Teacher Salary & Benefits',\
                      'Pensions', 'Capital Expenses', 
                      'Instructional-Related Expenses'])
    Expenditure_Cat_Unknown = set(['Unknown','#N/A'])
    Expenditure_Cat_Rename = {}
    Expenditure_Cat_Rename['Operational Expenses'] = 'Operations'
    Expenditure_Cat_Rename['Capital Expenses'] = 'Capital' 
    Expenditure_Cat_Rename['Instructional-Related Expenses'] = 'Instructional-Related'

    create_data = school_info.create_school_dictionary()
    school_data = create_data
    sample_school = school_data[school_name]

    labels = []
    values = []
    unknown_sum = 0


    for key in sample_school.keys():
        if key in Expenditure_Cat:
            if key in Expenditure_Cat_Rename.keys():
                new_key = Expenditure_Cat_Rename[key]
                labels.append(new_key)
            else:
                labels.append(key)
            values.append(sample_school[key])
        elif key in Expenditure_Cat_Unknown:
            unknown_sum = unknown_sum + sample_school[key]

    # grouping all 'unknown' or '#N/A' categories together
    labels.append('Unknown')
    values.append(unknown_sum)

    colors = tableau20[0: len(labels) + 1]


    fig = plt.figure()
    ax = fig.add_axes([.15, .1, .7, .7])
    ax.pie(values, labels = labels, colors = colors, autopct = '%1.f%%',\
            shadow = True, startangle = 90)

    plt.title('Expenditures: {0} \n Total: ${1}' .format(school_name, 
        "{:,.0f}".format(school_data[school_name]['total_expend'])))

    image = plt.show()
    return image

def demographic_bar(school_name):
    ethnicity_cat = set(['asian', 'white', 'african', 'hispanic', 'multi'])
    
