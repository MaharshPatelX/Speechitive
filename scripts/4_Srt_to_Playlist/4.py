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
				if x['change'][3] == 0:
					name = x['new_name']
					os.system('python stp.py "'+name+'"')
					y = vdata.find_one({'vid':x['vid']})
					myquery = { "vid": x['vid'] }
					new_lst = y['change']
					new_lst[3] = 1
					newvalues = { "$set": { "change": new_lst } }
					vdata.update_one(myquery, newvalues)

	time.sleep(3)