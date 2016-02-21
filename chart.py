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

plt.figure(figsize = (12, 9))

# Remove the plot frame lines. They are unnecessary chartjunk.    
ax = plt.subplot(111)    
ax.spines["top"].set_visible(False)    
ax.spines["bottom"].set_visible(False)    
ax.spines["right"].set_visible(False)    
ax.spines["left"].set_visible(False)  

# Ensure that the axis ticks only show up on the bottom and left of 
# the plot. Ticks on the right and top of the plot are generally 
# unnecessary chartjunk.    
ax.get_xaxis().tick_bottom()    
ax.get_yaxis().tick_left()    
  
# Limit the range of the plot to only where the data is.    
# Avoid unnecessary whitespace.    
plt.ylim(0, 90)    
plt.xlim(1968, 2014)

# Make sure your axis ticks are large enough to be easily read.    
# You don't want your viewers squinting to read your plot.    
plt.yticks(range(0, 91, 10), [str(x) + "%" for x in range(0, 91, 10)],\
    fontsize=14)    
plt.xticks(fontsize=14)


# Create expenditure pie charts

Expenditure_Cat = set(['Admin Salary & Benefits', 'Unknown', '#N/A', \
                   'Operational Expenses', 'Teacher Salary & Benefits', \
                    'Pensions', 'Capital Expenses', 'Instructional-Related Expenses'])


create_data = school_info.create_school_dictionary()
school_data = create_data
sample_school = school_data['Edward K Ellington Elementary School']

labels = []
values = []


for key in sample_school.keys():
    if key in Expenditure_Cat:
        labels.append(key)
        values.append(sample_school[key])

colors = tableau20[0: len(labels) + 1]

plt.pie(values, labels = labels, colors = colors, autopct = '%1.1f%%',\
        shadow = True, startangle = 90)

plt.axis('equal')

plt.legend(title = "Expenditure Categories", loc = 'best')

plt.tight_layout()
plt.show()