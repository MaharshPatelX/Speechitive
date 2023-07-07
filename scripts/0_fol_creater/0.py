import os
import pymongo
import json
import time

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["CGC"]
vdata = mydb["video_data"]

while True:
	for x in vdata.find():
		if x['fol'] == 0:
			name = x['new_name']
			loc = '../../'+(x['store_location']).replace('up_videos','output')
			full = loc+name
			os.system('mkdir "'+full+'"')
			os.system('mkdir "'+full+'/img"')
			os.system('mkdir "'+full+'/json"')
			os.system('mkdir "'+full+'/srt"')
			os.system('mkdir "'+full+'/txt"')
			os.system('mkdir "'+full+'/wav"')
			os.system('mkdir "'+full+'/vtt"')
			os.system('mkdir "'+full+'/thum"')
	
			myquery = { "vid": x['vid'] }
			newvalues = { "$set": { "fol": 1 } }
			vdata.update_one(myquery, newvalues)

	time.sleep(0.5)