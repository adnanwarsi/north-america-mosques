import sys
import os
import io
import json
import googlemaps

import openpyxl
import time

start_time = time.time()

if len(sys.argv) < 3:
    print ('\n\nusage1: \n\n>>>python ' + sys.argv[0] + '  {excel file with US coordinates} {search term} \n\n')
    exit()

coord_data_file = sys.argv[1]
search_term = sys.argv[2]


''' make a directory if not already, to save individual receipe files as json '''
places_search_dir_path = "./places_search_data/"
try:
    os.makedirs(places_search_dir_path)
except OSError:
    if not os.path.isdir(places_search_dir_path):
        raise

# google API reference doc https://github.com/googlemaps/google-maps-services-python
#
gmaps = googlemaps.Client(key='AIzaSyC02kAGSXn6IIOw0kvgITAYdoOdEF1noK0')
# old key AIzaSyCyJFr8K4_tNRx0ATeNOh6gDd02VCToVxA should work only for 1000 free queries in 24 hrs
# new key AIzaSyC02kAGSXn6IIOw0kvgITAYdoOdEF1noK0 should work for 15000 free queries in 24 hrs

wb = openpyxl.load_workbook(coord_data_file)
sheet = wb.get_sheet_by_name('coords')

for rowNum in range(2, sheet.max_row):  # skip the first row
    title = sheet.cell(row=rowNum, column=1).value
    lat = sheet.cell(row=rowNum, column=2).value
    lon = sheet.cell(row=rowNum, column=3).value
    print str('Places query for %s at lat %s, lon %s ' % (title, lat, lon))

    results_log_file_name = places_search_dir_path \
                            + 'radial_search_lat' \
                            + str(lat) \
                            + '_lon' \
                            + str(lon) \
                            + search_term \
                            + '.json'

    if not os.path.isfile(results_log_file_name):


        # the search has not been done yet.
        places_result = gmaps.places_radar((str(lat), str(lon)), 50000, keyword=search_term)

        if 'OK' in places_result['status']:
            place_dict = {}  # intialize
            for place_data in places_result['results']:
                try:
                    place_detail_result = gmaps.place(place_data['place_id'], language='en-US')

                    if 'OK' == place_detail_result['status']:
                        print '>>>' + place_detail_result['result']['name'],
                        if 'mosque' in place_detail_result['result']['types']:
                            # add to dictionary
                            print ' *********************** is a masjid'
                            place_dict[place_detail_result['result']['place_id']] = place_detail_result
                        elif any(substring in place_detail_result['result']['name'] for substring in ['Muslim', 'Islam', 'Muhammad', 'Mosque', 'Masjid', 'Tawheed', 'Hijra', 'Imam ', 'Quran', 'An-Noor', '-Uloom', 'Ahmadiyya', 'Bani Hashim', 'Ismaili', 'Jamatkhana', 'Hussain', 'Al-iman', 'Alhidayat', 'Madinah']):
                            # add to dictionary
                            print ' *********************** is a masjid'
                            place_dict[place_detail_result['result']['place_id']] = place_detail_result
                        else:
                            print 'IGNORE ::: not a masjid'
                    else:
                        print 'IGNORE : Did not get data back for ' + place_data['place_id']

                except:
                    print 'ERROR in processing ' + place_data['place_id']

            # write the data into a json file
            with io.open(results_log_file_name, 'w', encoding='utf8') as json_file:
                data = json.dumps(place_dict, indent=4, ensure_ascii=False)
                # unicode(data) auto-decodes data to unicode if str
                json_file.write(unicode(data))

    else:
        print str('IGNORE : %s already exists' % (results_log_file_name))


print("--- %s seconds ---" % (time.time() - start_time))