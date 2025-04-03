import cv2
import matplotlib.pyplot as plt
import random
import math
from copy import deepcopy



class node():
    def __init__(self,pos,image,parent=None):
        self.pos=pos
        self.x=pos[0]
        self.y=pos[1]
        self.parent=parent
        self.image=image
    def distance(self,point):
        return math.dist((self.x,self.y),point)
    
    def extend(self,point,step):
        theta = math.atan2(point[1] - self.pos[1], point[0] - self.pos[0])
        
        for i in range(step):
           
            new_point = (int(self.pos[0] + (i+1) * math.cos(theta)), 
                     int(self.pos[1] + (i+1) * math.sin(theta)))
           
            
            if(self.image[new_point[1]][new_point[0]]==0):
                return None
            
        new_point = (int(self.pos[0] + step * math.cos(theta)), 
                     int(self.pos[1] + step * math.sin(theta)))
        
        
        if(self.image[new_point[1]][new_point[0]]==0):
            return None
        else:
            cv2.line(self.image,self.pos,new_point,50,1)
            cv2.circle(self.image,self.pos,1,50,3)
            cv2.circle(self.image,new_point,1,50,3)
            return new_point
def nearest_node(tree,point):
    min_d=tree[0].distance(point)
    nearest=tree[0]
    for n in tree:
        d=n.distance(point)
        if d<min_d:
            nearest=n
            min_d=d
    return nearest
    
        
def init_random(img):
    return (random.randrange(10,img.shape[1]-20),random.randrange(20,img.shape[0]-20))

def try_connect(start_tree,end_tree,step):
    for i in start_tree:
        for j in end_tree:
            if(i.distance(j.pos)<=step):
                if(j.extend(i.pos,step)):
                    return i,j
            
    return 0,0

def draw_path(img,nodeA,nodeB):
    color_img=cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    cv2.line(color_img,nodeA.pos,nodeB.pos,(0,255,0))
    cv2.circle(color_img,nodeA.pos,2,(255,0,0),3)
    cv2.circle(color_img,nodeB.pos,2,(255,0,0),3)
    
    draw_path_side(color_img,nodeA)
    draw_path_side(color_img,nodeB)
    
    return color_img
def draw_path_side(color_img,node):
    child=node
    parent=child.parent
    while parent:
        cv2.line(color_img,child.pos,parent.pos,(0,255,0),1)
        cv2.circle(color_img,parent.pos,2,(255,0,0),3)
        
        child=parent
        parent=child.parent
        
    
def rrt_connect(start,end,step,img,max_iter):
    start_tree=[]
    end_tree=[]
    start_tree.append(node(start,img))
    end_tree.append(node(end,img))
    
    for _ in range(max_iter):
        cv2.imshow("win",img)
        cv2.waitKey(1)
        
        rand=init_random(img)
        n_start_node=nearest_node(start_tree,rand)
        n_end_node=nearest_node(end_tree,rand)
        
        new_point=n_start_node.extend(rand,step)
        if(new_point):
            start_tree.append(node(new_point,img,n_start_node))
        
        new_point=n_end_node.extend(rand,step)
        if(new_point):
            end_tree.append(node(new_point,img,n_end_node))
        
        a,b=try_connect(start_tree,end_tree,step)
        if(a and b):
            return draw_path(img,a,b)
    return 0
            
        
def start_connet():

    start_easy=(40,320)
    start_hard=(160,10)
    end_easy=(100,320)
    end_hard=(450,300)

    step_size=25
    max_iter=500

    maze=cv2.imread("task_2/maze.png",0)


    res1=rrt_connect(start_easy,end_easy,step_size,deepcopy(maze),max_iter)
    res2=rrt_connect(start_hard,end_hard,step_size,deepcopy(maze),max_iter)


    # cv2.imwrite("maze_easy_result.png",res1)
    # cv2.imwrite("maze_hard_result.png",res2)
    cv2.imshow('win',res1)
    cv2.imshow('win2',res2)
    cv2.waitKey(0)
    
if(__name__=="__main__"):
    start_connet()
