import pymongo

client = pymongo.MongoClient("mongodb://127.0.0.1:40000")

db = client.bogus

cursor = db.animals.find()
for entry in cursor:
    print(entry)

