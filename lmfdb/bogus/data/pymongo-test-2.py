import pymongo

client = pymongo.MongoClient("mongodb://127.0.0.1:40000")

db = client.bogus

query = {'animal' : 'elephant'}
cursor = db.animals.find(query)
for entry in cursor:
    print(entry)

