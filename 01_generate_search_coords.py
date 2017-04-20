import json
import math
import xlwt
import geopy
from geopy.distance import VincentyDistance
from geopy.geocoders import Nominatim


geolocator = Nominatim()
def geo_reverse_print(lat, lon):
    print "\n"
    print(str('%.6f' % lat) + "," + str('%.6f' % lon))
    location = geolocator.reverse(str('%.6f' % lat) + "," + str('%.6f' % lon))
    print(location.address)
    print "\n"

# given: lat1, lon1, b = bearing in degrees, d = distance in kilometers

# google API reference doc https://github.com/googlemaps/google-maps-services-python
#
# import googlemaps
# from datetime import datetime
#
# gmaps = googlemaps.Client(key='Add Your Key here')
#  oh, btw, my key =    AIzaSyC02kAGSXn6IIOw0kvgITAYdoOdEF1noK0
#
# # Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#
# # Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
#

'''
# US mainland (excluding Alaska, Hawaii, PeurtoRico) enclosing rectangle
lat_sw_corner = 25.194324
lon_sw_corner = -124.683966
lat_ne_corner = 49.431926
lon_ne_corner = -65.918096
'''

# Canada
lat_sw_corner = 41.698099
lon_sw_corner = -141.285412
lat_ne_corner = 69.921785
lon_ne_corner = -52.178718


'''
The distance between the centers of the circles in the X-direction is sqrt(3)*R  and not 2*R
because the search radius of google api allows R = 50km
'''

d = math.sqrt(3)*50  # distance in kilometers


# initialize
lat = lat_sw_corner
lon = lon_sw_corner
row = 0
coord_matrix = {}

while (lat < lat_ne_corner):
    row += 1
    col = 1
    coord_matrix[str('row%02dcol%02d' % (row, col))] = [str('%.6f' % lat) , str('%.6f' % lon)]
    row_origin = geopy.Point(lat, lon)
    while (lon < lon_ne_corner):
        col += 1
        b = 90 # bearing in degrees from north
        origin = geopy.Point(lat, lon)
        destination = VincentyDistance(kilometers=d).destination(origin, b)
        lat, lon = destination.latitude, destination.longitude
        coord_matrix[str('row%02dcol%02d' % (row, col))] = [str('%.6f' % lat) , str('%.6f' % lon)]
        print str('%s,%s'%(lat,lon))

    # coord_matrix.append(row_array)
    b = 30*math.pow((-1),(row % 2))  # bearing in degrees from north
    destination = VincentyDistance(kilometers=d).destination(row_origin, b)
    lat, lon = destination.latitude, destination.longitude

# print json.dumps(coord_matrix,indent=2,sort_keys=True)


# write the coordinates in an excel file
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('srch_coords')

# put in the column titles
sheet.write(0, 0, 'title')
sheet.write(0, 1, 'latitude')
sheet.write(0, 2, 'longitude')

row = 1
for elem in sorted(coord_matrix):
    sheet.write(row,0,elem)
    sheet.write(row,1,coord_matrix[elem][0])
    sheet.write(row,2,coord_matrix[elem][1])
    row += 1

workbook.save('canada_search_coords.xls')

# geo_reverse_print(lat2,lon2)

