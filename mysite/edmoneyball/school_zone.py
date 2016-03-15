# CS 122 Project: EdMoneyBall
# Imports the geolocation information regarding school zones, 
# and do related computations.
# Created by: Vi Nguyen, Sirui Feng, Turab Hassan

from . import school_info
import json
import pyproj
from shapely.geometry import Polygon, Point
from shapely.ops import transform
from functools import partial


zone_jsonfile = "edmoneyball/network_info.geojson"
school_dict = school_info.create_school_dictionary()

def create_poly_dict(zone_jsonfile):
    '''
    Constructs a dictionary, which the keys are the zone number in the form of
    string, and the value is a list of lists in the form of [lon, lat] taht
    defines a polygon of the school zone.
    The input is the json file that contains information of the polygon.
    '''
    poly_dict={}
    with open(zone_jsonfile) as f:
        network_info = json.load(f)
        zone_info = list((network_info["features"]))
        for zone in zone_info:
            zone_num = zone["properties"]["networknum"]
            zone_name = zone["properties"]["planningzo"]

            if len(zone["geometry"]["coordinates"]) == 1:
                zone_poly_list = zone["geometry"]["coordinates"][0][0]
            else:
                zone_poly_list = []
                for each in zone["geometry"]["coordinates"]:
                    for x in each:
                        zone_poly_list += x
            
            poly_dict[zone_num] = {}
            poly_dict[zone_num]["zone_name"] = zone_name
            poly_dict[zone_num]["poly"] = zone_poly_list
    return poly_dict

poly_dict=create_poly_dict(zone_jsonfile)

def build_school_zone_dict(poly_dict, school_dict):
    '''
    Constructs a school zone dictionary, the key is the school name,
    the value is the zone number.
    '''
    school_zone_dict = {}
    for school in school_dict:
        s_lon = school_dict[school]['lon']
        s_lat = school_dict[school]['lat']
        school_zone_dict[school] = get_zone(s_lon, s_lat, poly_dict)
    return school_zone_dict

def school_in_zone(ulat, ulon, show_u_zone = False):
    '''
    Constructs a list of schools that is in the user's school zone, 
    only the names.
    The input is the user's (lat, lon)
    ''' 
    u_zone = get_zone(ulon, ulat, poly_dict)
    school_in_zone=[]
    for school in school_zone_dict:
        if school_dict[school]['type'] == 'Charter' or \
        u_zone == school_zone_dict[school]:
            school_in_zone.append(school)
    
    if not show_u_zone:
        return school_in_zone
    return school_in_zone, u_zone, poly_dict[u_zone]['poly']

def get_zone(lon, lat, poly_dict):
    '''
    Returns a zone number which the location being passed along belongs to.
    This function is direct copy of the following source:
    Source: 'http://stackoverflow.com/questions/21328854/shapely-and
    -matplotlib-point-in-polygon-not-accurate-with-geolocation'
    '''
    lon = float(lon)
    lat = float(lat)
    for zone in poly_dict:
        zone_poly = poly_dict[zone]["poly"]
        project = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'),
        pyproj.Proj('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 \
            +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m \
            +nadgrids=@null +no_defs'))
        poly = Polygon(zone_poly)
        p = Point(lon, lat)
        if poly.contains(p):
            return zone
            
school_zone_dict=build_school_zone_dict(poly_dict, school_dict)