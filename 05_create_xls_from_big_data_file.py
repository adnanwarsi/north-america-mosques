import sys
import os
import io
import json
import xlwt
import re

if len(sys.argv) < 2:
    print ('\n\nusage1: \n\n>>>python ' + sys.argv[0] + ' {all-data json file} \n\n')
    exit()

data_file = sys.argv[1]

# set the excel file name to be populated
excel_file_name = os.path.splitext(data_file)[0] + ".xls"

# write the palces list in a excel file
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('muslim centers')


with open(data_file) as json_data:
    place_coord_file_data = json.load(json_data)

    '''
    # logic to be completed
    # combine all the same addresses as multiple instances of teh same place
    new_dict = {}
    for placeItemData in place_coord_file_data.itervalues():
        key = placeItemData['formatted_address']
        if key not in new_dict:
            # add the record as is
            new_dict[key] = placeItemData
        else:
            # the key exists already.  merge the two
            new_dict[key]['Aliases'] =
    '''


    # put in the column titles
    sheet.write(0, 0, 'Google Place ID')
    sheet.write(0, 1, 'Latitude')
    sheet.write(0, 2, 'Longitude')
    sheet.write(0, 3, 'Name')
    sheet.write(0, 4, 'Address')
    sheet.write(0, 5, 'Rating')
    sheet.write(0, 6, 'Google ID')
    sheet.write(0, 7, 'Phone')
    sheet.write(0, 8, 'Website')
    sheet.write(0, 9, 'Postal Code')
    sheet.write(0, 10, 'Country')
    sheet.write(0, 11, 'State')
    sheet.write(0, 12, 'County')
    sheet.write(0, 13, 'City')
    sheet.write(0, 14, 'Types')
    sheet.write(0, 15, 'Sect')

    row = 1
    for placeItemData in place_coord_file_data.itervalues():
        placeInfo = placeItemData['result']
        sheet.write(row, 0, placeInfo['place_id'])
        sheet.write(row, 1, placeInfo['geometry']['location']['lat'])
        sheet.write(row, 2, placeInfo['geometry']['location']['lng'])
        sheet.write(row, 3, placeInfo['name'])
        sheet.write(row, 4, placeInfo['formatted_address'])
        if 'rating' in placeInfo:
            sheet.write(row, 5, placeInfo['rating'])
        sheet.write(row, 6, placeInfo['id'])

        if 'international_phone_number' in placeInfo:
            sheet.write(row, 7, placeInfo['international_phone_number'])

        if 'website' in placeInfo:
            sheet.write(row, 8, placeInfo['website'])

        for elems in placeInfo['address_components']:
            if 'postal_code' in elems['types']:
                sheet.write(row, 9, elems['short_name'])
            elif 'country' in elems['types']:
                sheet.write(row, 10, elems['short_name'])
            elif 'administrative_area_level_1' in elems['types']:
                sheet.write(row, 11, elems['short_name'])
            elif 'administrative_area_level_2' in elems['types']:
                sheet.write(row, 12, elems['short_name'])
            elif 'locality' in elems['types']:
                sheet.write(row, 13, elems['long_name'])

        sheet.write(row, 14, ', '.join(placeInfo['types']) )

        # filters for sects

        # nation of islam
        if re.search(r'nation |[0-9]+|muhammad mosque|muhammad\'s', placeInfo['name'], re.IGNORECASE):
            sheet.write(row, 15, "Nation Of Islam")
        elif re.search(r'shia |imam ali|bohra |hussain |husain |ahlul |jafari |islamic education', placeInfo['name'], re.IGNORECASE):
            sheet.write(row, 15, "Shia")
        elif re.search(r'ahmadiyya ', placeInfo['name'], re.IGNORECASE):
            sheet.write(row, 15, "Ahmadiyya")
        elif re.search(r'ismaili |jamat ', placeInfo['name'], re.IGNORECASE):
            sheet.write(row, 15, "Ismaili")
        elif re.search(r'ismaili |jamat |jamaat ', placeInfo['name'], re.IGNORECASE):
            sheet.write(row, 15, "Ismaili")
        elif re.search(r'sufi ', placeInfo['name'], re.IGNORECASE):
            sheet.write(row, 15, "Sufi")
        elif re.search(r'cemetery', placeInfo['name'], re.IGNORECASE):
            sheet.write(row, 15, "Cemetery")

        elif 'website' in placeInfo and re.search(r'jamat|jamaat', placeInfo['website'], re.IGNORECASE):
            sheet.write(row, 15, "Ismaili")
        elif 'website' in placeInfo and re.search(r'ahmadiyya', placeInfo['website'], re.IGNORECASE):
            sheet.write(row, 15, "Ahmadiyya")
        elif 'website' in placeInfo and re.search(r'sufi', placeInfo['website'], re.IGNORECASE):
            sheet.write(row, 15, "Sufi")
        elif 'website' in placeInfo and re.search(r'noi\.org', placeInfo['website'], re.IGNORECASE):
            sheet.write(row, 15, "Nation Of Islam")
        elif 'website' in placeInfo and re.search(r'cemetery', placeInfo['website'], re.IGNORECASE):
            sheet.write(row, 15, "Cemetery")

        else:
            sheet.write(row, 15, "Sunni") # default to Sunni

        row += 1


workbook.save(excel_file_name)
