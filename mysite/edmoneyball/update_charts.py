'''
import school_info
import chart


school =  'Jane A Neil Elementary School'
data = school_info.create_school_dictionary()
data_distr_avg = chart.district_avg()
#print(data[school]['total_expend'])
#print(data_distr_avg['district_avg']['total_expend'])
schools = list(data.keys())
list_of_schools1 = schools[0:5]

#print(chart.expenditure_compare(list_of_schools1))

#print(chart.compare(list_of_schools1, chart.Expenditure_Cat, chart.Expenditure_Cat_Rename,\
#                     'Expenditures Per Student', data, data_distr_avg))
#print(chart.compare(list_of_schools1, chart.ethnicity_cat, chart.ethnicity_cat_rename,\
#                     'Ethnicity', data, data_distr_avg))
#print(chart.compare(list_of_schools1, chart.frlunch_cat, chart.frlunch_cat_rename,\
#                     'Income Indicator: Free and Reduced Lunch', data, data_distr_avg))
print(chart.compare(list_of_schools1, chart.acad_perf_cat, chart.acad_perf_cat_rename,\
                     'Academic Performance', data, data_distr_avg))


#print(chart.frlunch_bar(school, data, data_distr_avg))

print(chart.bar(school, data, data_distr_avg, chart.ethnicity_cat, chart.ethnicity_cat_rename,\
                            'Ethnicity'))

#print(chart.bar(school, data, data_distr_avg, chart.acad_perf_cat, chart.acad_perf_cat_rename,\
#                            'Academic Performance'))

#labels_school, values_school = chart.expenditure_data(school, data)
#print('school; label, values:', labels_school, values_school)
#labels_distr, values_distr = chart.expenditure_data('district_avg', data_distr_avg)
#print('school: label, values:', labels_distr, values_distr)
#print(chart.expenditure_pie(data, school, labels_school, values_school, labels_distr, values_distr))
#print(chart.district_avg())

'''
## Text for Sirui in Django

import school_info
import chart

#school =  'Woodlawn Community Elementary School'


def create_charts(school):
    data = school_info.create_school_dictionary()
    data_distr_avg = chart.district_avg()

    # Run charts with specified school
    urls = {'school': school}
    url_frl = chart.frlunch_bar(school, data, data_distr_avg)
    urls['url1'] = url_frl
    url_eth = chart.bar(school, data, data_distr_avg, chart.ethnicity_cat, chart.ethnicity_cat_rename,\
                                'Ethnicity')
    urls['url2'] = url_eth
    url_perf = chart.bar(school, data, data_distr_avg, chart.acad_perf_cat, chart.acad_perf_cat_rename,\
                                'Academic Performance')
    urls['url3'] = url_perf
    # Expenditure chart
    labels_school, values_school = chart.expenditure_data(school, data)
    labels_distr, values_distr = chart.expenditure_data('district_avg', data_distr_avg)
    url_exp = chart.expenditure_pie(data, school, labels_school, values_school, labels_distr, values_distr)
    urls['url4'] = url_exp

    print(urls)
    return urls
