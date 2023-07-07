import os
import pymongo
import json
import time


myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["CGC"]
vdata = mydb["video_data"]

while True:
	for x in vdata.find():
		if x['fol'] == 1:
			if x['change'][2] == 1:
				if x['thum'] == 0:
					name = x['new_name']
					time1 = x['video_lenth']
					send = 'python thum.py "'+name+'" '+'"'+time1+'"'
					os.system(send)

					myquery = { "vid": x['vid'] }
					newvalues = { "$set": { 'thum' : 1 } }
					vdata.update_one(myquery, newvalues)

	time.sleep(10)