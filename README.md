# CS122project
A group project for UChicago CS 122
Team Name: EdMoneyBall
Sirui Feng, Turab Hassan, & Vi Nguyen

##Install Packages##
Name: 
 Use: 
 Installation command: sudo pip3 install pyproj
Name:
 Use:
 Installation command: sudo apt-get install python-shapely
Name: Shapely
 Use:
 Installation command: sudo pip3 install shapely

##Data##
Datasets folder 
    FOIA Request #826 - (did we use this?)
    Chicago Public Schools Budget Fiscal Year 2015 Proposed - (did we use this?)
    CPS_School_Locations_SY1415.xlsx - 
    CPS_Schools_IDs_locations_13-14.xlsx - 
    FY2015 GL Expenditure Report as of 2015-06-30 - Schools 08-04-2015.xls - 
    SchoolQualityRatingPolicyResults&AccountabilityStatus_2015-6_full.xlsx -


##Django implmentation##
mysite - folder that contains our Django implementation
    Edmoneyball - folder that ...
        static - folder that contains static css, js, images, and other files for styling
            all files in this folder, unless specified, were sourced from 
            http://startbootstrap.com/template-overviews/stylish-portfolio/; only small modifications were made
            *img/heatmap_sample.png was created by us ...

        templates - folder that contains our html pages
            edmoneyball
                address.html - 
                comparison.html - page to let user choose schools they want to compare; and displays the results
                explore.html - page where user can choose 1 school at a time to look at data for
                heatmap.html - 
                individual.html - 
                recommendation.html

                # The 4 files below were sourced from http://startbootstrap.com/template-overviews/stylish-portfolio/; only small modifications were made
                index.html  - homepage
                javascript.html - brings in js components
                head.html - brings in 
                navar.html - navigation bar

                plot_school_comparisons.html
                plot_school_recommendations.html

        ##Python programs##
        urls.py
        views.py
        admin.py
        apps.py
        forms.py
        models.py
        geocode.py
        getcontext.py
        chart.py - contains algorithms that clean the data and plot charts
        ranking.py - algorithm that processes user inputs and generates recommendation
        update_charts.py - calls on various functions to update charts with selected/relevant schools
        rating.py - 
        school_info.py - 
        school_zone.py -
        tests.py (currently blank)

        scores.csv
        UpdatedLocations.csv
        cps.csv
        cta.kml
        EducationData.db
        network_info.geojson

        

  

 mysite - folder that ...
  settings.py -
  urls.py -
  wsgi.py -
 db.sqlite3 -
 EducationData.db -
 manage.py -



##Other##
readme.txt - this file
Proposal - folder with our initial proposal and presentation
Trash - backup of files that we had referred to and/or could use in the future



