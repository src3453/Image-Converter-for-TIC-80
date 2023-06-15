import sys
import numpy as np
import cv2
from PIL import Image
from skvideo.io import vread


IMWIDTH = 240 // 2 # 60
IMHEIGH = 136 // 2 # 34

palcode = """pals={{"""
imgcode = """img={{"""
tic_code = f"imgt=0 function SCN(y)for i=0,47 do poke(i+0x3fc0,tonumber(string.sub(pals[imgt%#pals+1][y//{136//IMHEIGH}+1],i+1,i+1),16)*16)end for x=1,{IMWIDTH+1} do rect((x-1)*{240//IMWIDTH},y,{240//IMWIDTH},{136//IMHEIGH},tonumber(string.sub(img[imgt%#img+1][y//{136//IMHEIGH}+1],x,x),16))end end TIC=function()imgt=time()//100 end"

path = input("Image path?> ")
video = vread(path)

print(f"This image has {video.shape[0]} frame(s).")
for l,image in enumerate(video):
    image = cv2.resize(cv2.cvtColor(image,cv2.COLOR_RGB2BGR),(IMWIDTH,IMHEIGH),interpolation=cv2.INTER_LINEAR_EXACT)
    tmp = np.zeros_like(image)
    K = 16
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
                paltmp += format(k//16,'01x')
        for j in label.ravel():
            imgtmp += format(j,"1x")
        
        palcode += f"\"{paltmp}\","
        imgcode += f"\"{imgtmp}\","
        res2 = res.reshape((img.shape))
        tmp[i,:] = res2 
        colors[i,:K,:] = center
    palcode = palcode[:-1] + "},{"
    imgcode = imgcode[:-1] + "},{"
    print(f'converting frame {l}...')

print('converted.')
open("converted.code.lua","w").write(f"{palcode[:-2]}}}\n{imgcode[:-2]}}}\n{tic_code}")
cv2.imwrite("converted.png",tmp)
cv2.imwrite("converted.colors.png",colors)
