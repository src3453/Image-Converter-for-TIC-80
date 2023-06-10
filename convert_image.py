import sys
import numpy as np
import cv2
from PIL import Image

if sys.argv[1]:
    print("using args")
    path = sys.argv[1]
else:
    path = input("Image path?> ")

image = cv2.resize(cv2.cvtColor(np.array(Image.open(path)),cv2.COLOR_RGB2BGR),(240,136),interpolation=cv2.INTER_CUBIC)
tmp = np.zeros_like(image)
palcode = """pals={"""
imgcode = """img={"""
tic_code = "function SCN(y)for i=0,47 do poke(i+0x3fc0,tonumber(string.sub(pals[y+1],i*2+1,i*2+2),16))end for x=1,241 do pix(x-1,y,tonumber(string.sub(img[y+1],x,x),16))end end TIC=function()end"
colors = np.zeros((136,16,3))

for i in range(image.shape[0]):
    img = image[i,:]
    Z = img.reshape((-1,3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 16
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    #print(center)
    paltmp = ""
    imgtmp = ""
    for j in center:    
        for k in reversed(j):
            paltmp += format(k,'02x')
    for j in label.ravel():
        imgtmp += format(j,"1x")
    
    palcode += f"\"{paltmp}\","
    imgcode += f"\"{imgtmp}\","
    res2 = res.reshape((img.shape))
    tmp[i,:] = res2 
    colors[i,:K,:] = center
palcode = palcode[:-1] + "}"
imgcode = imgcode[:-1] + "}"

print('converted.')
open("converted.code.lua","w").write(f"{palcode}\n{imgcode}\n{tic_code}")
cv2.imwrite("converted.png",tmp)
cv2.imwrite("converted.colors.png",colors)
