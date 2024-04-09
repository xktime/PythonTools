import pymongo
import bson

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["mixture"]
collection = db["mixture"]

with open("mixture.bson", "rb") as file:
    data = file.read()

documents = bson.decode_all(data)

collection.insert_many(documents)

print("完成")