import pandas as pd
import csv
import random
import copy
import os
import requests


# Reading the google forms response sheet
sheet_id = "1Y8XrBRt952oFlihPI8hn5KWcJ57n9zXULrlBXFn-LqI"
df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

# Printing the full list of respondents (including the date on which the forms was filled in)
print("These are the participants that signed up:")
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

# path to CSV file that stores the pairings of this round
new_pairs_csv = "Coffee Partner Lottery new pairs.csv"

# path to CSV file that stores all pairings (to avoid repetition)
all_pairs_csv = "Coffee Partner Lottery all pairs.csv"


# init set of old pairs
opairs = set()

DELIMITER = ','

# load all previous pairings (to avoid redundancies)
if os.path.exists(all_pairs_csv):
    with open(all_pairs_csv, "r") as file:
        csvreader = csv.reader(file, delimiter=DELIMITER)
        for row in csvreader:
            opairs.add(tuple(row))
            
# load participant's data
formdata = pd.read_csv(participants_csv, sep=DELIMITER)

# create duplicate-free list of participants
participants = list(set(formdata[header_email]))

# init set of new pairs
npairs = set()

# running set of participants
nparticipants = copy.deepcopy(participants)

# Boolean flag to check if new pairing has been found
new_pairs_found = False

# Ask how big the groups have to be
group_size = int(input("How big should the groups be?"))

# try creating new pairing until successful
while not new_pairs_found:
    if len(participants) % group_size != 0:
        if len(participants) % group_size == 1:
            glist = []
            for i in range(group_size + 1):
                i = random.choice(nparticipants)
                nparticipants.remove(i)
                glist.append(i)
            npairs.add(tuple(glist))
        else:
            glist = []
            for i in range(len(participants) % group_size):
                i = random.choice(nparticipants)
                nparticipants.remove(i)
                glist.append(i)
            npairs.add(tuple(glist))

    while len(nparticipants) > 0:
        plist = []
        for i in range(group_size):
            i = random.choice(nparticipants)
            nparticipants.remove(i)
            plist.append(i)
        npairs.add(tuple(plist))

    if npairs.isdisjoint(opairs):
        new_pairs_found = True
    else:
        npairs = set()
        nparticipants = copy.deepcopy(participants)
        
# assemble output for printout
output_string = "------------------------\n"
output_string += "Today's coffee groups:\n"

for pair in npairs:
    pair = list(pair)
    output_string += "------------------------\n"
    for i in range(len(pair)):
        name_email_pair = f"Member {i+1}:{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]} ({pair[i]})"
        if i < len(pair) - 1:
            output_string += name_email_pair + ", \n"
        else:
            output_string += name_email_pair + "\n"

# write output to console
print(output_string)

# write new pairs into CSV file
with open(new_pairs_csv, "w") as file:
    header = ["name1", "email1", "name2", "email2", "name3", "email3"]
    file.write(DELIMITER.join(header) + "\n")
    for pair in npairs:
        pair = list(pair)
        for i in range(len(pair)):
            name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]}{DELIMITER} {pair[i]}"
            if i < len(pair) - 1:
                file.write(name_email_pair + DELIMITER + " ")
            else:
                file.write(name_email_pair + "\n")

mode = "a" if os.path.exists(all_pairs_csv) else "w"
        
with open(all_pairs_csv, mode) as file:
    for pair in npairs:
        pair = list(pair)
        for i in range(0,len(pair)):
            if i < len(pair)-1:
                file.write(pair[i] + DELIMITER)
            else:
                file.write(pair[i] + "\n")
# Function to read conversation starters from a file
def read_conversation_starters(file_path):
    with open(file_path, "r") as file:
        conversation_starters = file.readlines()
    return conversation_starters

# Function to generate messages for all groups
def generate_messages(groups, conversation_starters):
    messages = []
    for group_index, group in enumerate(groups):
        participants = ", ".join(group)
        message = f"Hello {participants}!\n\nYou have been matched for a coffee meeting. Here's your conversation starter:\n\n"
        message += random.choice(conversation_starters)
        message += "\n\nEnjoy your coffee meeting!\n"
        messages.append(message)
    return messages

# groups
groups = npairs

# Simulated conversation starters file path
conversation_starters_file = "conversation_starters.txt"

# Read conversation starters from file
conversation_starters = read_conversation_starters(conversation_starters_file)

# Generate messages for all groups
messages = generate_messages(groups, conversation_starters)

# Save messages to text files
for index, message in enumerate(messages):
    with open(f"group_{index + 1}_message.txt", "w") as file:
        file.write(message)

        
# print finishing message
print()
print("Job done.")    
