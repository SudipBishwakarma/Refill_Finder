from __future__ import print_function
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of the spreadsheet.
SPREADSHEET_ID = '1FnVT6qk1x2HVggmn_EkspLdnvdZbN-RoaYICoDokstY'
PRODUCTS_SHEET_RANGE_NAME = 'A2:F'
BRANDS_SHEET_RANGE_NAME = 'Brands!A2:D'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    """Shows basic usage of the Sheets API.
    Reads values from two sheets and 
    generates respective json files.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.join(BASE_DIR, 'token.pickle')):
        with open(os.path.join(BASE_DIR, 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(BASE_DIR, 'credentials.json'), SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(os.path.join(BASE_DIR, 'token.pickle'), 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    products_sheet_data = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=PRODUCTS_SHEET_RANGE_NAME).execute().get('values', [])

    brands_sheet_data = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=BRANDS_SHEET_RANGE_NAME).execute().get('values', [])

    if not (products_sheet_data and brands_sheet_data):
        print('No data found.')
    else:
        # Extracts Products sheet data to json file
        product_coll = {} # Main products collection

        # Gets unique brand names from Products sheet.
        brands = []
        for i in range(0, len(products_sheet_data)):
            brands.append(products_sheet_data[i][0].strip())
        brands = list(set(brands))
        
        #Gets types and product details
        for i in range(0, len(brands)):
            types = []
            product_coll[brands[i]] = {} # Parent collection for brands

            # Gets Types based on Brand
            for j in range(0, len(products_sheet_data)):
                if products_sheet_data[j][0] == brands[i]:
                    types.append(products_sheet_data[j][1])
            types = list(set(types))

            for k in range(0, len(types)):
                product_coll[brands[i]][types[k]] = {} # Child collection of brand for types

            for l in range(0, len(types)):
                # Gets product data based on brand and type
                product_data = []
                for m in range(0, len(products_sheet_data)):
                    if products_sheet_data[m][0] == brands[i] and products_sheet_data[m][1] == types[l]:
                        product_data.append(products_sheet_data[m][2:])

                for n in range(0, len(product_data)):
                    product_coll[brands[i]][types[l]][n] = {} # Child collection of types for product details

                for o in range(0, len(product_data)):
                    keys = ["product_name", "img_url", "product_url", "refill_length"] # Key name mapping for individual product data
                    for p in range(0, len(keys)):
                        product_coll[brands[i]][types[l]][o][keys[p]] = product_data[o][p]

        write_file(product_coll, "products.json") # Writes data to products.json file

        # Extracts Brands sheet data to a json file
        brand_coll = {} # Main brands collection

        # Gets unique brand names from Brands sheet.
        brands = []
        for i in range(0, len(brands_sheet_data)):
            brands.append(brands_sheet_data[i][0].strip())
        brands = list(set(brands))
        
        #Gets types and brand details
        for i in range(0, len(brands)):
            types = []
            brand_coll[brands[i]] = {} # Parent collection for brands based on types

            # Gets Types based on Brand
            for j in range(0, len(brands_sheet_data)):
                if brands_sheet_data[j][0] == brands[i]:
                    types.append(brands_sheet_data[j][1])

            for k in range(0, len(types)):
                brand_coll[brands[i]][types[k]] = {} # Child collection of types for storing brand data

            for l in range(0, len(types)):
                # Gets data based on brand and type
                brand_data = []
                for m in range(0, len(brands_sheet_data)):
                    if brands_sheet_data[m][0] == brands[i] and brands_sheet_data[m][1] == types[l]:
                        brand_data.append(brands_sheet_data[m][2:])

                for n in range(0, len(brand_data)):
                    keys = ["img_url", "description"] # Key name mapping for individual brand data
                    for o in range(0, len(keys)):
                        brand_coll[brands[i]][types[l]][keys[o]] = brand_data[n][o]

        write_file(brand_coll, "brands.json") # Writes data to brands.json file

def write_file(data, file_name):
    """This function converts dictionary data to json format and 
    writes json data to a file with name specified as file_name parameter.
    """
    json_data = json.dumps(data, sort_keys=True, indent=4)
    try:
        file_to_write = open(os.path.join(BASE_DIR, file_name),'w')
        print('%s generated successfully' % file_name)
    except:
        print("Failed")
    file_to_write.write(json_data)
    file_to_write.close()

if __name__ == '__main__':
    main()