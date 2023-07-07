import os
import json
import time
import sys



def mp4_video_ext(output_loc,input_loc_file,fname):
	mp4_video_qr1 = 'ffmpeg -i "'+ input_loc_file +'" -c:v copy -an "'+output_loc+'\\tmp.mp4"'
	mp4_video_qr2 = 'ffmpeg -i "'+ output_loc+'\\tmp.mp4" -c:v copy -sn "'+output_loc+'\\'+ fname +'"'
	os.system(mp4_video_qr1)
	os.system(mp4_video_qr2)
	delete_tmp_file = output_loc+'\\tmp.mp4'
	os.system('del "'+delete_tmp_file+'"')

def mkv_video_ext(filename,input_path,output_path):
	new_filename = ''.join(filename.split('.')[:-1])

	mkv_video_qr1 = 'ffmpeg -i "'+input_path+'\\'+filename+'" -c:v libx264 -c:a aac -map 0 -map -0:s -c copy "'+output_path+'\\tmp.mp4"'
	mkv_video_qr2 = 'ffmpeg -i "'+output_path+'\\tmp.mp4" -c:v copy -an "'+output_path+'\\tmp1.mp4"'
	mkv_video_qr3 =	'ffmpeg -i "'+output_path+'\\tmp1.mp4" -c:v copy -sn "'+output_path+'\\'+new_filename+'.mp4"'

	os.system(mkv_video_qr1)
	os.system(mkv_video_qr2)
	os.system(mkv_video_qr3)

	os.system('del '+'"'+output_path+'\\tmp.mp4"')
	os.system('del '+'"'+output_path+'\\tmp1.mp4"')




def get_metadata(inp,out):
	qry = 'ffprobe -hide_banner -v error -show_streams -of json "'+ inp +'" > "'+out+'"'
	os.system(qry)
	f = open(out)
	data = json.load(f)
	return data

def get_tot_num_name_audio(data):
	data = data['streams']
	cnt = 0
	lst_name = []
	for d in data:
		if d['codec_type'] == 'audio':
			l=''
			t=''
			if 'language' in d['tags'].keys():
				l=d['tags']['language']
			if 'title' in d['tags'].keys():
				t=d['tags']['title']
			full_name = t+' - ['+l+']'
			lst_name.append(full_name)
			cnt=cnt+1
	
	return cnt,lst_name

def del_json(op):
	os.system('del "'+op+'"')




def mp4_audio_ext(input_location,output_location,fol_name,file_name):
	input_full_loc = input_location + '\\' + file_name
	output_json_path = input_location + '\\a.json'

	meta_data = get_metadata(input_full_loc,output_json_path)
	tot_num,lst_name = get_tot_num_name_audio(meta_data)
	del_json(output_json_path)

	op_loc = output_location + '\\' + fol_name + '\\audio\\'
	new_op_fname1 = ''
	for x in range(tot_num):
		new_op_fname = '"'+op_loc+lst_name[x]+str(x)+'.mp4"'
		print(input_full_loc,'\n',new_op_fname)
		qry='ffmpeg -i "'+input_full_loc+'" -map 0:a:'+str(x)+' -acodec libmp3lame '+new_op_fname
		os.system(qry)
		new_op_fname1= lst_name[x]+str(x)+'.mp4'
	return new_op_fname1





def mkv_audio_ext(input_location,output_location,fol_name,file_name):
	input_full_loc = input_location + '\\' + file_name
	output_json_path = input_location + '\\a.json'

	meta_data = get_metadata(input_full_loc,output_json_path)
	tot_num,lst_name = get_tot_num_name_audio(meta_data)
	del_json(output_json_path)

	op_loc = output_location + '\\' + fol_name + '\\audio\\'
	new_op_fname1 = ''
	for x in range(tot_num):
		new_op_fname = '"'+op_loc+lst_name[x]+str(x)+'.mp4"'
		print(input_full_loc,'\n',new_op_fname)
		qry='ffmpeg -i "'+input_full_loc+'" -map 0:a:'+str(x)+' -acodec libmp3lame '+new_op_fname
		os.system(qry)
		new_op_fname1= lst_name[x]+str(x)+'.mp4'

	return new_op_fname1



def video_m3u8(input_loc , output_loc , fname):
	qry = "ffmpeg -i " + input_loc+"/"+fname+"/video/"+fname  + " -codec: copy -start_number 0 -hls_time 5 -hls_list_size 0 -f hls " + output_loc+"/"+fname+"/video/index.m3u8"
	os.system(qry)
	os.system('del "' + input_loc+'/'+fname+'/video\\'+fname+'"')


def audio_m3u8(input_loc , output_loc , afname , fname):
	qry = 'ffmpeg -i "' + input_loc+'/'+fname+'/audio/'+afname  + '" -codec: copy -start_number 0 -hls_time 5 -hls_list_size 0 -f hls "' + output_loc+'/'+fname+'/audio/index.m3u8"'
	os.system(qry)
	os.system('del "' + input_loc+'/'+fname+'/audio\\'+afname+'"')






start = time.time()
tmp_fil = sys.argv[1:]
if tmp_fil == []:
	exit()
x=tmp_fil[0]

folder_location = '../../static/up_videos'
store_location = '../../static/hls'

aud_f_name = ''


full_folder_loc = folder_location+"\\"+x
loc_creat_op_fol = store_location+'\\'+x
print('mkdir "'+loc_creat_op_fol+'"')
os.system('mkdir "'+loc_creat_op_fol+'"')
file_ext = (x.split('.'))[-1]
if file_ext == 'mkv' or file_ext == 'mp4':
	file_name_wise_fol_name = loc_creat_op_fol
	os.system('mkdir "'+file_name_wise_fol_name+'\\video"')
	os.system('mkdir "'+file_name_wise_fol_name+'\\audio"')
	# Extract video only
	if file_ext == 'mp4':
		filename = x
		input_location_filename = folder_location+'\\'+x
		file_name_wise_fol_name1 = store_location+'\\'+x+'\\video'
		mp4_video_ext(file_name_wise_fol_name1 , input_location_filename , filename)
	elif file_ext == 'mkv':
		filename = x
		input_path = folder_location + '\\' + x
		output_path = store_location + '\\' + x + '\\video'
		mkv_video_ext(filename,input_path,output_path)
	# Extract video only
	# Extract audio only
	if file_ext == 'mp4':
		input_location = folder_location
		output_location = store_location
		file_name = x
		fol_name = x
		aud_f_name = mp4_audio_ext(input_location,output_location,fol_name,file_name)
	elif file_ext == 'mkv':
		input_location = folder_location
		output_location = store_location
		file_name = x
		fol_name = x
		aud_f_name = mkv_audio_ext(input_location,output_location,fol_name,file_name)
	# Extract audio only
os.system('del "'+folder_location+'/a.json"')


# M3U8 for video file
video_m3u8(store_location , store_location , x)
# M3U8 for video file

print('\n\n\n\n\n',aud_f_name,'\n\n\n\n\n')
# M3U8 for audio file
audio_m3u8(store_location , store_location , aud_f_name , x)
# M3U8 for audio file





end = time.time()
print((end - start)/60)