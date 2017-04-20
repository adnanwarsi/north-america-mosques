import sys
import os
import io
import json
import xlwt

if len(sys.argv) < 2:
    print ('\n\nusage1: \n\n>>>python ' + sys.argv[0] + '  {dir with data files} \n\n')
    exit()

places_search_dir_path = sys.argv[1]
if not os.path.isdir(places_search_dir_path):
    print places_search_dir_path + ' is not a directory'

composite_data_file_name = 'composite_data_file.json'
dict = {}

for filename in os.listdir(places_search_dir_path):
    if filename.endswith(".json"):
        print filename
        with open(str(places_search_dir_path) + str(filename)) as json_data:
            place_coord_file_data = json.load(json_data)
            # print json.dumps(coord_places_data, indent=2)
            for key in place_coord_file_data:
                dict[key] = place_coord_file_data[key]

# write the data into a json file
with io.open(composite_data_file_name, 'w', encoding='utf8') as json_file:
    data = json.dumps(dict, indent=4, ensure_ascii=False)
    json_file.write(unicode(data))

