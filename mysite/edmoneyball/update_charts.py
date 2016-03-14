# CS 122 Project: EdMoneyBall
# Passes key variables (titles, school data, etc) to the plotting functions to 
# generate needed urls
# Vi Nguyen, Sirui Feng, Turab Hassan

from . import school_info, chart, ranking, school_zone

# calling dictionaries to increase speed
data = school_info.create_school_dictionary()
data_distr_avg = chart.district_avg()


def create_charts(school):
    '''
    Given a school name, returns a list of urls where we plot the school's data 
    and the district average for:
        -Percent of students on free and reduced Lunch
        -Distribution of ethnicity groups among students
        -Math/Reading growth scores, and grade level scores
        -Expenditures
    '''
    # Income indicator
    urls = {'school': school}
    url_frl = chart.frlunch_bar(school, data, data_distr_avg)
    urls['url1'] = url_frl

    # Ethnicity
    url_eth = chart.bar(school, data, data_distr_avg, chart.ethnicity_cat,
    chart.ethnicity_cat_rename, 'Ethnicity')
    urls['url2'] = url_eth

    # Performance
    url_perf = chart.bar(school, data, data_distr_avg, chart.acad_perf_cat,
    chart.acad_perf_cat_rename, 'Academic Performance')
    urls['url3'] = url_perf

    # Expenditure chart
    labels_school, values_school = chart.expenditure_data(school, data)
    labels_distr, values_distr = chart.expenditure_data('district_avg', 
    data_distr_avg)
    url_exp = chart.expenditure_pie(data, school, labels_school, values_school,
    labels_distr, values_distr)
    urls['url4'] = url_exp

    return urls


def compare_recommend(recommend_indicator, pref_crit_from_ui = None,
list_of_schools = None):
    '''
    Plots the graphs for either the schools that the user wants to compare, 
    or the top 5 schools that we recommend to the user
    Inputs:
        recommend_indicator - True or False to indicate whether this function 
            is being called to chart the recommended schools (True) or just to
            chart the comparisons
    Outputs:
        list of urls where plotly charted the graphs
    '''

    if recommend_indicator:
        clean_data = ranking.clean_data(pref_crit_from_ui)
        list_of_schools, crit_met_indicator, crit_not_met_full_list = \
        ranking.school_rank(clean_data)

    urls = {'school': list_of_schools}

    url1 = chart.compare(list_of_schools, chart.Expenditure_Cat, \
        chart.Expenditure_Cat_Rename, 'Expenditures Per Student', data, \
        data_distr_avg)
    urls['url1'] = url1

    url2 = chart.compare(list_of_schools, chart.ethnicity_cat, \
        chart.ethnicity_cat_rename, 'Ethnicity', data, data_distr_avg)
    urls['url2'] = url2
    
    url3 = chart.compare(list_of_schools, chart.frlunch_cat, \
        chart.frlunch_cat_rename, 'Income Indicator: Free and Reduced Lunch', \
        data, data_distr_avg)
    urls['url3'] = url3

    url4 = chart.compare(list_of_schools, chart.acad_perf_cat, \
        chart.acad_perf_cat_rename, 'Academic Performance', data, data_distr_avg)
    urls['url4'] = url4

    if recommend_indicator:
        return urls, crit_met_indicator, crit_not_met_full_list
    else:
        return urls