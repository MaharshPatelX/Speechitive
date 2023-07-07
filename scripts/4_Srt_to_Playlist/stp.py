import os
import json
import sys
import time


start = time.time()
tmp_fil = sys.argv[1:]
if tmp_fil == []:
	exit()

m3u8_cont = '#EXTM3U\n#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="stereo",LANGUAGE="en",NAME="English",DEFAULT=YES,AUTOSELECT=YES,URI="audio/index.m3u8"\n#EXT-X-MEDIA:TYPE=SUBTITLES,GROUP-ID="subs",LANGUAGE="en",NAME="English",DEFAULT=YES,AUTOSELECT=YES,FORCED=NO,URI="sub/index_sub.m3u8"\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=258157,AUDIO="stereo",SUBTITLES="subs"\nvideo/index.m3u8'
f = open('../../static/hls/'+tmp_fil[0]+'/playlist.m3u8', "a")
f.write(m3u8_cont)
f.close()



end = time.time()
print((end - start)/60)