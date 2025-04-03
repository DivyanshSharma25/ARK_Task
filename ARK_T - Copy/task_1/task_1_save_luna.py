import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def clamp(n, smallest, largest): return max(smallest, min(n, largest))

def error(img1,img2,x1,y1,x2,y2,r):
    
    err=0
    block1=img1[x1-r:x1+r+1,y1-r:y1+r+1]
    block2=img2[x2-r:x2+r+1,y2-r:y2+r+1]
    
    err=np.sum((block1-block2)**2)
    
    return err

left_img=cv2.imread('right.png',0)
right_img=cv2.imread('left.png',0)
left_img=cv2.resize(left_img,(320,180))
right_img=cv2.resize(right_img,(320,180))

x,y=left_img.shape

disparity_mtrx=np.zeros((x,y))
r=10
check_r=50
for k in range(r,x-r):
    for i in range(r,y-r):
        err=float('inf')
        shift=0
        for j in range(clamp(i-check_r,r,y-r),clamp(i+check_r,r,y-r)):
            a=error(left_img,right_img,k,j,k,i,r).astype(int)
            if(a<err):
                err=a
                shift=abs(i-j)
            print(k,i,j,a)
            
        disparity_mtrx[k,i]=shift
   
sns.heatmap(disparity_mtrx)
plt.show()


    