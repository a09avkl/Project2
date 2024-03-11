# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 13:36:11 2024

@author: stefa
"""

import requests

# Reading the google forms response sheet
sheet_id ="1Y8XrBRt952oFlihPI8hn5KWcJ57n9zXULrlBXFn-LqI"
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

# Printing the full list of respondents (including the date on which the forms was filled in)
print(df)

# Path to the CSV file
participants_csv = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

# Making a temporary file
temp_csv_path = "temp_participants.csv"

# Download participant data from response spreadsheet of the Google Forms
response = requests.get(participants_csv)

# The list of participants is read from the soucre again every time
# At the end the temporary file gets deleted
if response.status_code == 200:
    
    with open(temp_csv_path, "wb") as file:
        file.write(response.content)
        
    formdata = pd.read_csv(temp_csv_path)
    
    os.remove(temp_csv_path)
else:
    print("Failed to retrieve participant data from Google Sheets.")
    exit()
    
# header names in the CSV file (name and e-mail of participants)
header_name = "What is your name?"
header_email = "What is your e-mail?"
