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
			if x['change'][0] == 0:
				name = x['new_name']
				os.system('python vtm.py "'+name+'"')
				y = vdata.find_one({'vid':x['vid']})
				myquery = { "vid": x['vid'] }
				new_lst = y['change']
				new_lst[0] = 1
				newvalues = { "$set": { "change": new_lst } }
				vdata.update_one(myquery, newvalues)

	time.sleep(3)