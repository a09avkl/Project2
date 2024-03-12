# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 12:57:40 2024

@author: annaa
"""

import pandas as pd
import csv
import random
import copy
import os

# path to the CSV files with participant data
participants_csv = "Coffee Partner Lottery participants.csv"

# header names in the CSV file (name and e-mail of participants)
header_name = "Your name:"
header_email = "Your e-mail:"

# path to TXT file that stores the pairings of this round
new_pairs_txt = "Coffee Partner Lottery new pairs.txt"

# path to CSV file that stores the pairings of this round
new_pairs_csv = "Coffee Partner Lottery new pairs.csv"

# path to CSV file that stores all pairings (to avoid repetition)
all_pairs_csv = "Coffee Partner Lottery all pairs.csv"
        
# init set of old pairs
opairs = set()

DELIMITER=','

# load all previous pairings (to avoid redundancies)
if os.path.exists(all_pairs_csv):
    with open(all_pairs_csv, "r") as file:
        csvreader = csv.reader(file, delimiter=DELIMITER)
        for row in csvreader:
            group = []
            for i in range(0,len(row)):
                group.append(row[i])                        
            opairs.add(tuple(group))

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

# try creating new pairing until successful
group_size = int( input("How big should the groups be?")) # to determine the group size
while not new_pairs_found:   # to do: add a maximum number of tries
  
    # if number of participants not multiple of group size
    if len(participants)%group_size != 0:
        if len(participants)%group_size ==1: #if just one participant without group, make one group that is one person bigger
            glist=[] #this is a list with the groupmembers
            for i in range(group_size+1):
                i=random.choice(nparticipants) #choosing random participants until group size is reached
                nparticipants.remove(i) #remove chosen partciipants from list to not sort tthem double
                glist.append(i) #add chosen participants to group
            npairs.add(tuple(glist))
        else: #if there is more than one participant without griup just put them together in a group
            glist=[] #this is a list with the groupmembers
            for i in range(len(participants)%group_size):
                i=random.choice(nparticipants) #choosing random participants until group size is reached
                nparticipants.remove(i) #remove chosen partciipants from list to not sort tthem double
                glist.append(i)  #add chosen participants to group
            npairs.add(tuple(glist))
                
                

    # while still participants left to group...
    while len(nparticipants) > 0: # divide the rest into the chosen group size
         plist=[]
        for i in range(group_size): # code works same as above
            i=random.choice(nparticipants)
            nparticipants.remove(i)
            plist.append(i)
        npairs.add(tuple(plist))


 
    # check if all new pairs are indeed new, else reset
    if npairs.isdisjoint(opairs):
        new_pairs_found = True
    else:
        npairs = set()
        nparticipants = copy.deepcopy(participants)


# assemble output for printout
output_string = ""

output_string += "------------------------\n"
output_string += "Today's coffee partners:\n"
output_string += "------------------------\n"

for pair in npairs:
    pair = list(pair)
    output_string += "* "
    for i in range(0,len(pair)):
        name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]} ({pair[i]})"
        if i < len(pair)-1:
            output_string += name_email_pair + ", "
        else:
            output_string += name_email_pair + "\n"
    
# write output to console
print(output_string)

# write output into text file for later use
with open(new_pairs_txt, "wb") as file:
    file.write(output_string.encode("utf8"))

# write new pairs into CSV file (for e.g. use in MailMerge)
with open(new_pairs_csv, "w") as file:
    header = ["name1", "email1", "name2", "email2", "name3", "email3"]
    file.write(DELIMITER.join(header) + "\n")
    for pair in npairs:
        pair = list(pair)
        for i in range(0,len(pair)):
            name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]}{DELIMITER} {pair[i]}"
            if i < len(pair)-1:
                file.write(name_email_pair + DELIMITER + " ")
            else:
                file.write(name_email_pair + "\n")
                
# append pairs to history file
if os.path.exists(all_pairs_csv):
    mode = "a"
else:
    mode = "w"

with open(all_pairs_csv, mode) as file:
    for pair in npairs:
        pair = list(pair)
        for i in range(0,len(pair)):
            if i < len(pair)-1:
                file.write(pair[i] + DELIMITER)
            else:
                file.write(pair[i] + "\n")


             
# print finishing message
print()
print("Job done.")
