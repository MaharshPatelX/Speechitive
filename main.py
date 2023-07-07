from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import json
import requests
import pymongo
import subprocess
import os
from flask_cors import CORS, cross_origin
import time



app = Flask(__name__)
CORS(app, support_credentials=True)

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["CGC"]
vdata = mydb["video_data"]
names = mydb["N_names"]



# --------------- functions --------------------------------
def check_video_url(video_id):
	checker_url = "https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v="
	video_url = checker_url + video_id

	request = requests.get(video_url)

	return request.status_code == 200



def vid_size_duration(filename):
	result = subprocess.check_output(f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{filename}"',shell=True).decode()
	fields = json.loads(result)['streams'][0]
	duration = fields['duration']

	file_stats = os.stat(filename)
	size = file_stats.st_size / (1024 * 1024)

	return size,duration





# --------------- functions --------------------------------









# ------------------------------------------------------------------------



@app.route("/",methods=["GET","POST"])
@cross_origin(supports_credentials=True)
def main():
	
	tost = ''

	if (request.method == 'POST'):
		new_name = ''
		# vid = ''
		flg = 0
		get_names_data = names.find_one()
		if get_names_data != None:
			old_max_names = get_names_data['names']
			new_name = str(int(old_max_names)+1)
			vid = str(int(old_max_names)+1)

			myquery = { "names": old_max_names }
			newvalues = { "$set": { "names": int(new_name) } }
			flg = 1

		else:
			new_name = '0'
			vid = '0'
			names.insert_one({'names':int(new_name)})
		

		f = request.files['file']
		old_name = secure_filename(f.filename)
		


		new_name = new_name+'.'+old_name.split('.')[-1]
		
		loc = 'static/up_videos/'
		fullloc = loc + new_name
		f.save(fullloc)

		size,duration = vid_size_duration(fullloc)


		find_v_in_data = vdata.find_one({'old_name':old_name,'video_lenth':duration})
		if find_v_in_data == None:
			vdata.insert_one({'vid':int(vid),'new_name':new_name,'old_name':old_name,'store_location':loc,'video_lenth':duration,'video_size':size,'change':[0,0,0,0],'fol':0,'thum':0})
			if flg == 1: 
				names.update_one(myquery, newvalues)
				flg=0
			tost = 'New data Stored'

			return redirect('/video-process?data='+vid)
			
		else:
			print('del "'+ fullloc.replace('/','\\') +'"')
			os.system('del "'+ fullloc.replace('/','\\') +'"')
			tost = 'Data is already there'
			# first delete new added data then go and get store data
			nvid = find_v_in_data['vid']
			if find_v_in_data['change'][0] == 0 or find_v_in_data['change'][1] == 0 or find_v_in_data['change'][2] == 0 or find_v_in_data['change'][3] == 0:
				return redirect('/video-process?data='+str(nvid))
			else:
				return redirect('/demos?data='+str(nvid))

	return render_template("index.html",tost=tost)





@app.route("/video-process",methods=["GET","POST"])
def video_process():
	if (request.method == 'GET'):
		vid = request.args.get('data')
		
		data = vdata.find_one({'vid':int(vid)},{'_id':0})
		print(data)
		if data['change'][0] == 1 and data['change'][1] == 1 and data['change'][2] == 1 and data['change'][3] == 1:
			# return redirect('/video?data='+vid)
			pass


	return render_template("process.html",data=data)




@app.route("/analytics",methods=["GET","POST"])
def analytics():
	data = None
	if (request.method == 'GET'):
		vid = request.args.get('data')
		
		data = vdata.find_one({'vid':int(vid)},{'_id':0})
		
		if data['change'][0] == 1 and data['change'][1] == 1 and data['change'][2] == 1 and data['change'][3] == 1:
			f = open('static/output/'+data['new_name']+'/json/output.json')
			nlu = json.load(f)
			f.close()

	return render_template("ana.html",data=data,nlu=nlu)


@app.route("/wordcloud",methods=["GET","POST"])
def wordcloud():
	data = None
	if (request.method == 'GET'):
		vid = request.args.get('data')
		
		data = vdata.find_one({'vid':int(vid)},{'_id':0})
		
		if data['change'][0] == 1 and data['change'][1] == 1 and data['change'][2] == 1 and data['change'][3] == 1:
			data=data
		else:
			data=None

	return render_template("wordcl.html",data=data)





@app.route("/demos",methods=["GET","POST"])
def demos():
	data = []
	for x in vdata.find({},{'_id':0}):
		if x['change'][0] == 1 and x['change'][1] == 1 and x['change'][2] == 1 and x['change'][3] == 1:
			data.append(x)


	return render_template("demo.html",data=data)





@app.route("/video",methods=["GET","POST"])
def demos_video():
	data = {}
	if (request.method == 'GET'):
		vid = request.args.get('data')

		x = vdata.find_one({'vid':int(vid)},{'_id':0})
		if x['change'][0] == 1 and x['change'][1] == 1 and x['change'][2] == 1 and x['change'][3] == 1:
			data = x

	return render_template("video.html",data=data)


@app.route("/datatojson",methods=["GET","POST"])
def datatojson():
	data = {}
	if (request.method == 'GET'):
		vid = request.args.get('data')
		x = vdata.find_one({'vid':int(vid)},{'_id':0})		

	return jsonify({"message": x})






















@app.route('/process-data')
def process_data():
	if (request.method == 'GET'):
		vid = request.args.get('data')
	def all_pro_data():
		while True:
			all_list_data = vdata.find_one({'vid':int(vid)},{'_id':0})
			json_data = json.dumps(all_list_data)
			yield f"data:{json_data}\n\n"
			time.sleep(1)

	return Response(all_pro_data(), mimetype='text/event-stream')

















app.run(debug = True, threaded=True, host='0.0.0.0', port=5001)