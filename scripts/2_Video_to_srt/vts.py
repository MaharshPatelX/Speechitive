import os
from pydub import AudioSegment
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from fpdf import FPDF
import json
import sys
import time
import sys







def convert_sec_to_hrs(sec):
	hour, sec = divmod(sec, 3600)
	minute, sec = divmod(sec, 60)
	second, sec = divmod(sec, 1)
	millisecond = int(sec * 1000.)
	dt_time = '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)

	return dt_time


def wavConversion(targetFile):
	targetFile = AudioSegment.from_file(targetFile)
	targetFile = targetFile.set_channels(1)
	targetFile.export(path_store+"/wav/audioFile.wav", format="wav")
	
	return targetFile


def SpeechToText_API():
	apikey = 'Hq9jyX1bxjpQoUccv2ukbMQ5aAZCUO0F5QEQdw1DUs-9'
	url = 'https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/ed949167-86b1-4f74-8280-f9c625390985'

	# SpeechToText
	authenticator = IAMAuthenticator(apikey)
	stt = SpeechToTextV1(authenticator=authenticator)
	stt.set_service_url(url)

	with open(path_store+'/wav/audioFile.wav', 'rb') as aud_file:
		res = stt.recognize(audio=aud_file, 
			content_type='audio/wav', 
			model='en-US_NarrowbandModel',
			speaker_labels=True,
			smart_formatting=True,
			timestamps=True).get_result()
	word_time = res['results']

	text = [result['alternatives'][0]['transcript'].rstrip() + '.\n' for result in res['results']]
	text = [para[0].title() + para[1:] for para in text]
	transcript = ''.join(text)
	with open(path_store+'/txt/output.txt', 'w') as out:
		out.writelines(transcript)

	return word_time



def convert_sub_formate(word_time,name):
	i=1
	full_text = []
	tmpp=[]
	tmp_data = []

	for x in word_time:
		for y in x['alternatives']:
			for z in y['timestamps']:
				sub_tmp = [str(i) , str(convert_sec_to_hrs(float(z[1]))) , str(convert_sec_to_hrs(float(z[2]))) , str(z[0])]
				tmp_data.append( sub_tmp )
				i=i+1

	ij=1
	for x in tmp_data:
		text_one = str(ij)+'\n'+x[1]+' --> '+x[2]+'\n'+x[3]+'\n\n'
		full_text.append(text_one)
		ij=ij+1

	new_string = ''
	for x in full_text:
		new_string = new_string + str(x)
	with open(path_store+'/srt/tmp.srt', 'w') as out:
		out.writelines(new_string)



	

start = time.time()
tmp_fil = sys.argv[1:]
if tmp_fil == []:
	exit()
fil_path='../../'+tmp_fil[0]
global path_store
path_store = fil_path.replace('up_videos','output')
wavConversion(fil_path)
convert_sub_formate(SpeechToText_API(),fil_path)





# if len(sys.argv) is not 3:
# 	print( 'wrong argv: %d' % len(sys.argv))
# 	sys.exit(0)
'''$ python srt2vtt.py ./in/mySubtitle.srt ./out/vttFolder/'''

in_file_path = path_store + '/srt/tmp.srt'
out_folder_path = path_store + '/vtt'
in_file_name = os.path.basename(in_file_path)
out_file_name = os.path.splitext(in_file_name)[0] + '.vtt'
print(out_file_name)
with open(in_file_path) as in_file:
	frames = in_file.read().split('\n\n')
	for rowid in range(len(frames)):
		frames[rowid] = frames[rowid].split('\n', 2)
	frames = [frame for frame in frames if len(frame) == 3]
	for index in range(len(frames)):
		frames[index][0] = index + 1
	out_file = open(os.path.join(out_folder_path, out_file_name), "w")
	oldstdout = sys.stdout
	sys.stdout = out_file
	print( 'WEBVTT\n' )
	for frame in frames:
		print(frame[0])
		print(frame[1].replace(',', '.'))
		print(frame[2] + '\n')
		sys.stdout.flush()
	out_file.close()
	sys.stdout = oldstdout;
print('done: %s' % (out_folder_path + '/' + out_file_name) )


end = time.time()
print((end - start)/60)