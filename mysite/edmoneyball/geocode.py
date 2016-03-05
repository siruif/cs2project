import urllib.parse
import json

def get_latlon(address):
    '''
    Given a street address as a string, geo codes the street address
    and returns the Lat and Lon and a list of floats
    '''
    maps_api_url = "?".join(["https://maps.googleapis.com/maps/api/geocode/json",\
    urllib.parse.urlencode({"address":address, "sensor":False, 'key':'AIzaSyD3MgwYmLVdZ6FUuftS3d-Yf85HbniwypY'})])
    response = urllib.request.urlopen(maps_api_url)
    data = json.loads(response.read().decode('utf8'))
    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
    return [ float(lat) , float(lng) ]            