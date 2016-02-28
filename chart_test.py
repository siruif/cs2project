import school_info
import chart

school = 'Wolfgang A Mozart Elementary School'
data = school_info.create_school_dictionary()
schools = list(data.keys())

list_of_schools1 = schools[0:5]

print(chart.expenditure_compare(list_of_schools1))
#chart.frlunch_pie(school)
#chart.demographic_bar(school)
#chart.expenditure_pie(school)