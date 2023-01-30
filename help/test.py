import csv
import os

CSV_FILE = "daimonds.csv"


import csv

# insert row[ID]:
# df.insert(0, 'ID', range(1, 1 + len(df)))

def save_csv(data): # data is a list of dictionaries
    with open(CSV_FILE, 'w', newline='') as file:
        # set the headers of the csv file
        fieldnames = data[0].keys() # make the keys of the first dictionary in the list "data"
        writer = csv.DictWriter(file, fieldnames=fieldnames) #  module that allows to write dictionaries to a CSV file
        writer.writeheader() #  writes the headers csv file - the keys of the first dictionary in the list.
        for row in data:
            writer.writerow(row) # Each row - dictionary will be written csv file with the keys as the headers.



def load_csv():
    data = []
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data