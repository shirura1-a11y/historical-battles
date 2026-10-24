"""Original procedural soundtrack, bilingual ASS captions and FFmpeg assembly."""
import math, random, wave, struct, subprocess, argparse
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--out',default='build'); a=p.parse_args(); out=Path(a.out).resolve(); out.mkdir(parents=True,exist_ok=True)
missing=[out/'frames'/f'frame_{i:04d}.png' for i in range(1,2101) if not (out/'frames'/f'frame_{i:04d}.png').is_file()]
if missing: raise FileNotFoundError(f'Missing {len(missing)} frames; render first. First missing: {missing[0]}')
rate=24000; rng=random.Random(1600)
with wave.open(str(out/'soundtrack.wav'),'wb') as w:
 w.setparams((1,2,rate,0,'NONE','not compressed'))
 for sec in range(70):
  data=bytearray()
  for j in range(rate):
   t=sec+j/rate; beat=t%(0.6 if t<35 else .4); drum=math.sin(2*math.pi*65*beat)*math.exp(-beat*20)*.3
   chord=[110,130.8128,146.8324,164.8138][int(t/8)%4]
   music=.08*math.sin(2*math.pi*chord*t)+.04*math.sin(2*math.pi*chord*1.5*t)
   noise=rng.uniform(-1,1); march=noise*.12*math.exp(-(t%.5)*35) if 15<=t<35 else 0
   clash=noise*.3*math.exp(-(t%.7)*14) if 35<=t<55 or t<3 else 0
   turn=.16*math.sin(2*math.pi*(220+40*(t-55))*t)*math.exp(-(t-55)) if 55<=t<60 else 0
   retreat=noise*.1*math.exp(-(t%.28)*30) if 60<=t<67 else 0
   fade=min(1,t/0.3,(70-t)/3); v=(music+drum+march+clash+turn+retreat)*max(0,fade)
   data.extend(struct.pack('<h',int(max(-.95,min(.95,v))*32767)))
  w.writeframes(data)
header='''[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: JP,Noto Sans CJK JP,34,&H00FFFFFF,&H00FFFFFF,&H00101820,&H90000000,1,0,0,0,100,100,0,0,1,3,1,8,30,30,65,1
Style: EN,Noto Sans CJK JP,27,&H00FFFFFF,&H00FFFFFF,&H00101820,&H90000000,0,0,0,0,100,100,0,0,1,2,1,2,30,30,75,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
cues=[(0,3,'天下分け目の決戦','SEKIGAHARA • 1600'),(3,8,'関ヶ原の戦い・1600年','Battle of Sekigahara'),(8,15,'赤：西軍　青：東軍','RED: WESTERN / BLUE: EASTERN'),(15,25,'東軍が進軍','The Eastern Army advances'),(25,35,'西軍が迎え撃つ','The Western Army responds'),(35,45,'両軍、激突','The armies clash'),(45,55,'戦線は膠着する','The battle hangs in the balance'),(55,62,'小早川秀秋が西軍を攻撃','Kobayakawa turns against the West'),(62,67,'西軍は敗走へ','The Western Army retreats'),(67,70,'関ヶ原の戦い 1600年','Battle of Sekigahara')]
def stamp(t): return f'0:{t//60:02}:{t%60:02}.00'
text=header
for start,end,jp,en in cues:
 for style,line in [('JP',jp),('EN',en)]: text+=f'Dialogue: 0,{stamp(start)},{stamp(end)},{style},,0,0,0,,{line}\n'
text+='Dialogue: 1,0:00:03.00,0:00:15.00,EN,,0,0,145,,史実を簡略化した再現 / Simplified historical reconstruction\n'
text+='Dialogue: 1,0:01:07.00,0:01:10.00,EN,,0,0,145,,史実を簡略化した再現 / Simplified reconstruction\n'
(out/'captions.ass').write_text(text,encoding='utf-8')
# cwd avoids filter escaping problems with absolute paths.
subprocess.run(['ffmpeg','-y','-framerate','30','-start_number','1051','-t','3','-i','frames/frame_%04d.png','-framerate','30','-start_number','91','-t','67','-i','frames/frame_%04d.png','-i','soundtrack.wav','-filter_complex','[0:v]setpts=PTS-STARTPTS[h];[1:v]setpts=PTS-STARTPTS[m];[h][m]concat=n=2:v=1:a=0,ass=captions.ass[v]','-map','[v]','-map','2:a:0','-frames:v','2100','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t','70','-movflags','+faststart','sekigahara.mp4'],cwd=out,check=True)
subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height,r_frame_rate','-of','json','sekigahara.mp4'],cwd=out,check=True)
