import sys
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db=myclient["codetrans"]
mydb=db[sys.argv[1]][sys.argv[2]]
for i in mydb.find():
	if i["ve"] > sys.argv[3]:
		print("Ask for labeling: ", i["file"])