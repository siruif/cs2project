import json
import pyproj
from shapely.geometry import Polygon, Point
from shapely.ops import transform
from functools import partial
import school_info

def create_zone_dict(zone_jsonfile):
    zone_dict={}
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
            
            zone_dict[zone_num] = {}
            zone_dict[zone_num]["zone_name"] = zone_name
            zone_dict[zone_num]["poly"] = zone_poly_list
    return zone_dict

def build_school_zone_dict():
    school_dict = school_info.create_school_dictionary()
    school_zone_dict = {}
    for school in school_dict:
        s_lon = school_dict[school]['lon']
        s_lat = school_dict[school]['lat']
        school_zone_dict[school] = get_zone(s_lon, s_lat)
    return school_zone_dict

def school_in_zone(ulat, ulon):
    poly_dict = create_zone_dict("network_info.geojson")
    u_zone = get_zone(ulon, ulat)
    school_in_zone=[]
    for school in school_zone_dict:
        if u_zone == school_zone_dict[school]:
            school_in_zone.append(school)
    return school_in_zone

def get_zone(lon, lat):
    #source: http://stackoverflow.com/questions/21328854/shapely-and-matplotlib-point-in-polygon-not-accurate-with-geolocation
    poly_dict = create_zone_dict("network_info.geojson")
    lon = float(lon)
    lat = float(lat)
    for zone in poly_dict:
        zone_poly = poly_dict[zone]["poly"]
        project = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'),
        pyproj.Proj('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs'))
        poly = Polygon(zone_poly)
        #print(lon, lat)
        p = Point(lon, lat)
        if poly.contains(p):
            return zone

school_zone_dict = build_school_zone_dict()

school_list = school_in_zone(41.796221, -87.581463)
print(school_list)

