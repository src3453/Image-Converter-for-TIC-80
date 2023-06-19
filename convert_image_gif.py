import sys
import numpy as np
import cv2
from PIL import Image
from skvideo.io import vread



IMWIDTH = int( 240 // 2 ) # Output image width
IMHEIGH = int( 136 // 2 ) # Output image height

OUT_FPS = 10 # output video framerate (-1 to auto framerate)

FRAME_DECIMATION = 1 # Decimation rate of video frames (Default: 1 (No decimation)) 

K = min( 16 ,IMWIDTH)

palcode = """pals={{"""
imgcode = """img={{"""
tic_code = f"imgt=0 function SCN(y)for i=0,{K*3-1} do poke(i+0x3fc0,tonumber(string.sub((pals[imgt%#pals+1][y//{136//IMHEIGH}+1])or pals[imgt%#pals+1][1],i+1,i+1),36)*7)end for x=1,{IMWIDTH+1} do if y%{136//IMHEIGH} == 0 then rect((x-1)*{240//IMWIDTH},y,{240//IMWIDTH},{136//IMHEIGH},tonumber(string.sub((img[imgt%#img+1][y//{136//IMHEIGH}+1])or pals[imgt%#pals+1][1],x,x),16))end end end TIC=function()imgt=time()//{1000//OUT_FPS} end"

path = input("Image path?> ")
print(f"\nLoading image...")
video = vread(path)
deco = "|/-\\"

print(f"This image has {video.shape[0]} frame(s). (Decimated to {video.shape[0]//FRAME_DECIMATION} frame(s))")

RES_AUTO = False #Undeveloped

if RES_AUTO:
    est_list = []
    for w in range(16,32,2):
        for h in range(16,32,2):
            estimated = int((240//w+48)*(136//h)*video.shape[0]*1.027571851190771)
            if estimated > 524288:
                print(f"\033[31;1m{240//w}x{136//h}({w}x{h})\033[0m",estimated)
            elif estimated > 65536:
                print(f"\033[33;1m{240//w}x{136//h}({w}x{h})\033[0m",estimated)
                est_list.append([estimated,w,h])
            else:
                print(f"\033[32;1m{240//w}x{136//h}({w}x{h})\033[0m",estimated)
    #maxv = est_list.index(np.max(np.array(est_list),0))
    #print(est_list[maxv])
    np.clip(est_list,0,524289)
    

for l,image in enumerate(video[::FRAME_DECIMATION]):
    image = cv2.resize(cv2.cvtColor(image,cv2.COLOR_RGB2BGR),(IMWIDTH,IMHEIGH),interpolation=cv2.INTER_LINEAR_EXACT)
    tmp = np.zeros_like(image)
    
    colors = np.zeros((IMHEIGH,K,3))

    for i in range(image.shape[0]):
        img = image[i,:]
        Z = img.reshape((-1,3))
        Z = np.float32(Z)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)   
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        #print(center)
        paltmp = ""
        imgtmp = ""
        for j in center:    
            for k in reversed(j):
                paltmp += np.base_repr(int(k//7.11111),36)
        for j in label.flatten():
            imgtmp += format(j,"1x")
        
        palcode += f"\"{paltmp}\","
        imgcode += f"\"{imgtmp}\","
        res2 = res.reshape((img.shape))
        tmp[i,:] = res2 
        colors[i,:K,:] = center
    palcode = palcode[:-1] + "},{"
    imgcode = imgcode[:-1] + "},{"
    print(f'converting frame {l+1}/{video.shape[0]//FRAME_DECIMATION}...{deco[l%4]}',end="\r")

print('\nconverted.')
open("converted.code.lua","w").write(f"{palcode[:-2]}}}\n{imgcode[:-2]}}}\n{tic_code}")
#cv2.imwrite("converted.png",tmp)
#cv2.imwrite("converted.colors.png",colors)
