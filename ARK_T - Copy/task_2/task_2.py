import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import rrt_connect
pi_img=cv2.imread('task_2\pi_image.png',0)
x,y=pi_img.shape
print(x,y)
pi_str=""

pi=open('task_2\pi.txt','r').read()
pi=pi.replace(" ",'')
for i in range(x):
    for j in range(y): 
        pi_str+=str(int(pi_img[i][j]/10))
        
        
print(len(pi_str)) 
c=0
b=False
missing=[]
for i in range(len(pi_str)-1):
    try:
        if(pi[i]!=pi_str[i+c] and pi_str[i+c+1]=="5"):
            print(i,pi[i],pi_str[i+c])
            missing.append(int(pi[i]))
            c+=1
    except:
        break
  
print(missing)

missing=[math.floor(k*10*math.pi) for k in missing]
missing.sort(reverse=True)
print(missing)
filter2x2=np.reshape(missing,(2,2))

print(filter2x2)

art_img=cv2.imread('task_2/artwork_picasso.png',0)
x,y=art_img.shape
o_image=art_img.copy()

for i in range(0,x-2,2):
    for j in range(0,y-2,2):
        o_image[i:i+2,j:j+2]=o_image[i:i+2,j:j+2]^filter2x2&filter2x2

o_image.resize((100,100))
collage=cv2.imread("task_2\collage.png",0)
min_error=float("inf")
cords=[]
x,y=collage.shape
for i in range(0,x-100,100):
    for j in range(0,y-100,100):
        block=collage[i:i+100,j:j+100]
        error=np.sum((block-o_image)**2)
        if(error<min_error):
            min_error=error
            cords=[i,j]
        

print("password",math.floor(np.sum(cords)*np.pi))



cv2.namedWindow("o_image", cv2.WINDOW_NORMAL) 
 
cv2.resizeWindow("o_image", o_image.shape[0]*5,o_image.shape[1]*5) 

cv2.imshow("o_image", o_image) 

rrt_connect.start_connet()

cv2.waitKey(0)