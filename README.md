# CS122project
A group project for UChicago CS 122
Team Name: EdMoneyBall
Created by: Sirui Feng, Turab Hassan, & Vi Nguyen

##NOTES ON SOURCES##
In each file, if we have sourced the code from somewhere else, 
we've included a note about the extent to which we modified it. In cases 
where no notes were written about sourcing, the file was original work.


##Install Packages##
Name: pyproj
 Use: performs cartographic transformations and geodetic computations.
 Installation command: sudo pip3 install pyproj

Name: Shapely
 Use: manipulation and analysis of geometric objects in the Cartesian plane.
 Installation command: sudo apt-get install python-shapely; sudo pip3 install shapely

Name: Plotly
 Use: create online charts
 Installation command: sudo pip3 install plotly

Name: Bootstrap Forms
 Use: format django forms
 Installation command: sudo pip3 install django-bootstrap3-form django-bootstrap-form

Name: Bootstrap
 Use: styling of site
 Installation command: sudo pipe3 install django-bootstrap


##Data##
Datasets folder
    -CPS_School_Locations_SY1415.xlsx: we used this file to update the geolocation 
    information
    -CPS_Schools_IDs_locations_13-14.xlsx: this file had incorrect geolocation 
    information
    -FOIA#826: folder that contain results from Lingwei Cheng's FOIA request
    -FY2015 GL Expenditure Report as of 2015-06-30: source of expenditure 
    data that we used, from FOIA#826
    -SchoolQualityRatingPolicyResults&AccountabilityStatus_2015-6_full.xlsx:
    source of academic performance information for each school
    -Chicago_Public_Schools_Budget_-_Fiscal_Year_2015_-_Proposed.csv: data
    on planned budget spending, we didn't use it.


##Django implementation##
-mysite: folder that contains our Django implementation
    -Edmoneyball: folder that contains our edmoneyball implementation
        -static: folder that contains static css, js, images, and other files 
        for styling
            -all files in this folder, unless specified, were sourced from 
            http://startbootstrap.com/template-overviews/stylish-portfolio/; 
            only small modifications were made
            -img/heatmap_sample.png was created by us using rating.py

        -templates: folder that contains our html pages
            -edmoneyball: folder to house our html pages
                -explore.html: page where user can choose 1 school at a time to 
                look at data, or enter their address to see school zones and
                select the school to explore
                -address.html: page to display school zones after user enters 
                address in explore.html
                -comparison.html: page to let user choose schools they want to 
                compare; and displays the results
                -recommendation.html: page to let user enter preferences for 
                algorithm to recommend top performing schools

                -individual.html: page to display charts for one school
                -plot_school_comparisons.html: page to display charts for 
                comparisons
                -plot_school_recommendations.html: page to display charts for
                recommended schools
                

                # The 4 files below were sourced from 
                http://startbootstrap.com/template-overviews/stylish-portfolio/; 
                    only small modifications were made
                -index.html: homepage
                -javascript.html: brings in js components
                -head.html: brings in header styling 
                -navar.html: navigation bar

        ##Python programs##
        -urls.py: a file which tells us which page the user is on to call the 
        correct function from views.py
        -views.py: processes the Http request and redirects to the correct page 
        based on the request
        -forms.py: forms that the user see on the webpage get created here.
        -geocode.py: turns a user entered address into lat, lon location
        -getcontext.py: Based on the user input, builds the context for the 
        html page
        
        -chart.py: contains algorithms that clean the data and plot charts
        -ranking.py: algorithm that processes user inputs and generates 
        recommendation
        -update_charts.py: calls on various functions to update charts with 
        selected/relevant schools
        
        -school_info.py: contains algorithms that fetch data from the dabase 
        and do related computations
        -school_zone.py: contains algorithms that clean up the zone geolocation 
        information

        -rating.py: contains algorithms that fetch data from the database to 
        generate heatmap
        -scores.csv: generated by rating.py to draw heatmap
        
        ##Data files##
        -UpdatedLocations.csv: correct geolocation of the CPS schools
        -EducationData1.db: school information database
        -network_info.geojson: school zone geolocations
        

##Other##
readme.txt - this file
Proposal - folder with our initial proposal and presentation
Trash - backup of files that we had referred to and/or could use in the future



##Run site locally##
python3 cs2project/mysite/manage.py runserver


=======
Install Packages:
sudo pip3 install pyproj
sudo apt-get install python-shapely
sudo pip3 install shapely

sudo pip3 install django-bootstrap-form
sudo pip3 install django-bootstrap3-form
sudo pip3 install plotly
sudo pip3 install django-bootstrap
