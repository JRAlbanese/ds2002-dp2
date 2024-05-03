#!/bin/bash python3

from pymongo import MongoClient, errors
from bson.json_util import dumps
import os
import json

#note that MONGOPASS is now changed to be MY OWN mongo passowrd
MONGOPASSn = os.getenv('MONGOPASSn')

uri = "mongodb+srv://cluster0.pnxzwgz.mongodb.net/"
client = MongoClient(uri, username='nmagee', password=MONGOPASSn, connectTimeoutMS=200, retryWrites=True)
# specify a database
db = client.pwg2gq
# specify a collection
collection = db.dp2stuff

#print(str(db))
#print(str(collection))

#both of the above things printed out, so I think the connection is working



#now, we need to import the 50 files within data, one of the directories given inside of this repo
directory = "data"


good_imports = 0
imports_failed = 0
imports_corrupted = 0

for filename in os.listdir(directory):
    full_file_path = os.path.join(directory, filename)
    try:
        with open(full_file_path) as file:
            file_data = json.load(file)  # This will also check for JSON integrity

        #now we can insert our data into mongo finally!
        if isinstance(file_data, list):
            collection.insert_many(file_data)
            good_imports += 1
                #update the number
            print("Successfully inserted multiple documents")
        else: #for if the json is not in a list
            collection.insert_one(file_data)
            good_imports += 1
            print(f"Inserted one document from {filename}")
    except json.JSONDecodeError: #found this error suggestion online for corruption
        imports_corrupted += 1
        print("Corrupted JSON file")
    except Exception: #we'll just do this for all other kinds of exceptions
        imports_failed += 1
        print("Failed to import")


#lets just print up some fstrings
print(f"Aggregate uccessful imports: {good_imports}")

print(f"total good imports: {imports_failed}")
print(f"Aggregate JSON files: {imports_corrupted}")



"""


# 2) Inserting the loaded data in the collection
#if JSON contains data more than one entry,
#insert_many is used, or else insert_one is used

if isinstance(file_data, list):
    try:
        collection.insert_many(file_data)
    except Exception as e:
        print(e, "when importing into Mongo")
else:
    try:
        collection.insert_one(file_data)
    except Exception as e:
        print(e)

        """

