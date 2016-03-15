# CS122project
A group project for UChicago CS 122
Team Name: EdMoneyBall
Sirui Feng, Turab Hassan, & Vi Nguyen

##Install Packages##
Name: pyproj
 Use: Performs cartographic transformations and geodetic computations.
 Installation command: sudo pip3 install pyproj

Name: Shapely
 Use:Manipulation and analysis of geometric objects in the Cartesian plane.
 Installation command: sudo apt-get install python-shapely; sudo pip3 install shapely

Name: Plotly
 Use: create online charts
 Installation command: sudo pip3 install plotly

Name: Bootstrap Forms
 Use: format django forms
 Installation command: sudo pip3 install django-bootstrap3-form django-bootstrap-form

Name: Bootstrap
 Use: styling of site
 Installation command sudo pipe3 install django-bootstrap


##Data##
Datasets folder
    Chicago Public Schools Budget Fiscal Year 2015 Proposed - (did we use this?)
    CPS_School_Locations_SY1415.xlsx - 
    CPS_Schools_IDs_locations_13-14.xlsx -(this file has wrong geolocation information) 
    FY2015 GL Expenditure Report as of 2015-06-30 - Schools 08-04-2015.xls - 
    				    				SchoolQualityRatingPolicyResults&AccountabilityStatus_2015-6_full.xlsx


##Django implmentation##
mysite - folder that contains our Django implementation
    Edmoneyball - folder that ...
        static - folder that contains static css, js, images, and other files 
        for styling
            -all files in this folder, unless specified, were sourced from 
            http://startbootstrap.com/template-overviews/stylish-portfolio/; 
            only small modifications were made
            *img/heatmap_sample.png was created by us ...

        templates - folder that contains our html pages
            edmoneyball - folder to house our html pages
                explore.html - page where user can choose 1 school at a time to 
                    look at data, or enter their address to see school zones and
                    select the school to explore
                address.html - page to display school zones after user enters 
                    address in explore.html
                comparison.html - page to let user choose schools they want to 
                    compare; and displays the results
                recommendation.html - page to let user enter preferences for 
                    algorithm to recommend top performing schools

                individual.html - page to display charts for one school
                plot_school_comparisons.html - page to display charts for 
                    comparisons
                plot_school_recommendations.html - page to display charts for
                    recommended schools
                

                # The 4 files below were sourced from 
                http://startbootstrap.com/template-overviews/stylish-portfolio/; 
                    only small modifications were made
                index.html  - homepage
                javascript.html - brings in js components
                head.html - brings in header styling 
                navar.html - navigation bar

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
        update_charts.py - calls on various functions to update charts with 
        selected/relevant schools
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



=======
Install Packages:
sudo pip3 install pyproj
sudo apt-get install python-shapely
sudo pip3 install shapely

sudo pip3 install django-bootstrap-form
sudo pip3 install django-bootstrap3-form
sudo pip3 install plotly
sudo pip3 install django-bootstrap
