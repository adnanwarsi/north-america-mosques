from bs4 import BeautifulSoup
import re
import json
import sys
import requests
import openpyxl


if len(sys.argv) < 2:
    print ('\n\nusage1: \n\n>>>python ' + sys.argv[0] + '  {excel file} \n\n')
    exit()

excel_db_file = sys.argv[1]

wb = openpyxl.load_workbook(excel_db_file)
sheet = wb.get_sheet_by_name('Sheet1')


# init for the URL scans
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}



for rowNum in range(2, sheet.max_row):  # skip the first row
    url = sheet.cell(row=rowNum, column=6).value
    # print url
    if url:
        print str("%d>>>>    will scan the website %s" % (rowNum, url))
        try:
            r = requests.get(url, headers=headers)
            page = r.text
            bsObj = BeautifulSoup(page, "html.parser")

            emails = [a["href"] for a in bsObj.select('a[href^=mailto:]')]
            if len(emails) > 0:
                print json.dumps(emails)
        except:
            print 'no url'

