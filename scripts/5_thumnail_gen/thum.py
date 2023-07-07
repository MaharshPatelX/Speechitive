# ffmpeg -ss 00:00:01.000 -i input.mp4 -vframes 1 output.png
import os
import sys
import time
import random




def convert_sec_to_hrs(sec):
	hour, sec = divmod(sec, 3600)
	minute, sec = divmod(sec, 60)
	second, sec = divmod(sec, 1)
	millisecond = int(sec * 1000.)
	dt_time = '%.2d:%.2d:%.2d.%.3d' % (hour, minute, second, millisecond)

	return dt_time


start = time.time()
tmp_fil = sys.argv[1:]
if tmp_fil == []:
	exit()


name = tmp_fil[0]
time1 = float(tmp_fil[1])

thum_1_tm = convert_sec_to_hrs(random.uniform(0, time1))
thum_2_tm = convert_sec_to_hrs(random.uniform(0, time1))

scr1 = 'ffmpeg -ss  00:00:10.000 -i ../../static/up_videos/'+name+' -vframes 1 ../../static/output/'+name+'/thum/1.png'
scr2 = 'ffmpeg -ss '+thum_2_tm+' -i ../../static/up_videos/'+name+' -vframes 1 ../../static/output/'+name+'/thum/2.png'

os.system(scr1)
os.system(scr2)

end = time.time()
print((end - start)/60)