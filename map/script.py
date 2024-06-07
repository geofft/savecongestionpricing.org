"""
Adapted from https://developers.google.com/sheets/api/quickstart/python
"""
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import geopandas as gpd

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1xIE2aD8Nb28cV7tPdMLq-z0cavyc04aE4vfhGd5DnVo"


def update_geojson(chamber, district_key, support_column_index):
    """
    Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    Updates GeoJSON with a 'support' column with values from the provided sheet
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    gdf = gpd.read_file(f"NYS_{chamber}_Districts_4326.geojson")
    gdf["support"] = None
    print(gdf.head())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        range = f"{chamber}!A2:E"
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        for row in values:
            try:
                print(f"{row[0]}, {row[1]}, {row[support_column_index]}")
                gdf.loc[gdf[district_key] == int(row[0]), "support"] = row[
                    support_column_index
                ]
            except IndexError:
                pass
    except HttpError as err:
        print(err)

    gdf.to_file(f"updated_{chamber}.geojson")


def main():
    # CHAMBER = "Assembly"
    # DISTRICT = "District"
    chamber = "Senate"
    district = "DISTRICT"
    support_column_index = 4
    update_geojson(chamber, district, support_column_index)
    pass


if __name__ == "__main__":
    main()
