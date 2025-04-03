import cv2
import random
import math
import time
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
def random_pos(pos_bounds_x,pos_bounds_y):
    
    x=random.randrange(pos_bounds_x[0],pos_bounds_x[1])
    y=random.randrange(pos_bounds_y[0],pos_bounds_y[1])
    return (x,y)

class Node():
    def __init__(self,pos):
        self.pos=pos
        self.connections=[]
        self.h=float('inf')
        self.g=float('inf')
        self.f=float('inf')
        self.parent=None
        
        self.min_t=float('inf')
    
    def distance(self,node):
        return math.dist(self.pos,node.pos)

    def connect(self,node):
        self.connections.append(node)
        
        
    

class PRM():
    n_nodes=0
    def __init__(self,c_space,obstacle=0,node_color=120,node_thicknes=3,node_radius=1,conn_color=100,conn_thickness=1):
        self.c_space=c_space
        self.c_space_copy=deepcopy(c_space)
        self.obstacle=obstacle
        
        self.nodes=[]
        
        
        self.node_color=node_color
        self.node_thickness=node_thicknes
        self.node_radius=node_radius
        
        self.conn_color=conn_color
        self.conn_thickness=conn_thickness
        
        
    
    def sample_c_space(self,n_samples,x_bounds,y_bounds):
        for i in range(n_samples):
            while(1):
                point=random_pos(x_bounds,y_bounds)
                if(self.is_free(point)):
                    break
            node=Node(point)
            self.nodes.append(node)
        #self.nodes.sort(key=lambda x:x.pos[0]+x.pos[1])
        
    
    def is_free(self,pos):
        return self.c_space[pos[1]][pos[0]]!=self.obstacle
        
    def draw_nodes(self,image=None):
        if image==None:
            image=self.c_space
        for i in self.nodes:
            cv2.circle(image,i.pos,self.node_radius,self.node_color,self.node_thickness)
    
    def draw_connection(self,nodeA,noedB,image=None):
        if(image==None):
            image=self.c_space
        cv2.line(image,nodeA.pos,noedB.pos,self.conn_color,self.conn_thickness)
        cv2.line(self.c_space_copy,nodeA.pos,noedB.pos,self.conn_color,self.conn_thickness+1)
    
    def make_connections(self,n_nearest):
        for i in  self.nodes:
            
            sorted_nodes=sorted(self.nodes,key=lambda x:i.distance(x))
            sorted_nodes.pop(0)
            
            while (len(i.connections)!=n_nearest and len(sorted_nodes)!=0):
                print(self.nodes.index(i),len(sorted_nodes))
                if(self.can_connect(i,sorted_nodes[0])):
                    i.connect(sorted_nodes[0])
                    sorted_nodes[0].connect(i)
                    self.draw_connection(i,sorted_nodes[0])
                sorted_nodes.pop(0)
            print(self.nodes.index(i),len(i.connections),n_nearest)
            cv2.imshow("conn",self.c_space)
            cv2.waitKey(1)

                    
    
    def can_connect(self,nodeA,nodeB):
        theta = math.atan2(nodeB.pos[1] - nodeA.pos[1], nodeB.pos[0] - nodeA.pos[0])
        i=0
        new_point=(0,0)
        new_points=[]
        while(nodeB.distance(Node(new_point))>1):
            print(i)
            new_point = (int(nodeA.pos[0] + (i+1) * math.cos(theta)), 
                     int(nodeA.pos[1] + (i+1) * math.sin(theta)))
            new_points.append(new_point)  
            
            i=i+1      
            if(self.c_space_copy[new_point[1]][new_point[0]]<110 and(nodeA.distance(Node(new_point))>2 and nodeB.distance(Node(new_point))>2)):
                # for new_point in new_points:
                #     cv2.circle(self.c_space,new_point,1,200,1)
                return 0
        
        
        return 1
    
    def a_star(self,start,end):
        start.g=0
        start.h=start.distance(end)
        start.f=start.h
        open=[start]
        closed=[]
        
        while open:
            lowest_f=sorted(open,key=lambda x:x.f)[0]
            cv2.circle(self.c_space,lowest_f.pos,self.node_radius,20,self.node_thickness)
            if(lowest_f==end):
                
                return 1
            closed.append(open.pop(open.index(lowest_f)))
            for i in lowest_f.connections:
                if(i not in closed):
                    new_h=i.distance(end)
                    if(i not in open or new_h<i.h):
                        i.h=new_h
                        i.g=lowest_f.g+i.distance(lowest_f)
                        i.f=i.g+i.h
                    i.parent=lowest_f
                    
                    if(i not in open):
                        open.append(i)
        
        return 0
    
    def dijkstra(self,start,end,image):
        explored=[]
        
        start.min_t=0
        c_node=start
        while c_node!=end:
            print(len(explored))
            if c_node==end:
                return 1
            for i in c_node.connections:
                
                time=c_node.min_t+i.distance(c_node)
                
                if(i.min_t>time):
                    i.parent=c_node
                    i.min_t=time
            
            arr=[conn for conn in c_node.connections if conn not in explored]
            explored.append(c_node)
            cv2.circle(image,np.array(c_node.pos)*2,self.node_radius,self.node_color,self.node_thickness)
            if arr:
                new_node=sorted(arr,key=lambda x:x.min_t,)[0]   
                cv2.line(image,np.array(new_node.pos)*2,np.array(c_node.pos)*2,self.conn_color,self.conn_thickness)     
                new_node.parent=c_node
                c_node=new_node
            else:
                new_node=0
                while not new_node:
                    c_node=c_node.parent
                    print(c_node)
                    arr=[conn for conn in c_node.connections if conn not in explored]
                    if(arr):
                        new_node=min(arr,key=lambda x:x.min_t)
                        break
                cv2.circle(image,np.array(c_node.pos)*2,self.node_radius,self.node_color,self.node_thickness)
                cv2.line(image,np.array(new_node.pos)*2,np.array(c_node.pos)*2,self.conn_color,self.conn_thickness)     
                
                c_node=new_node 
            cv2.imshow("wnn",image)
            cv2.waitKey(500)  
                            
        return 0
    
    def draw_path(self,end_node,color,image=None):
        if(len(image)==0):
            image=self.c_space
        
        cv2.circle(image,end_node.pos,self.node_radius,color,self.node_thickness)
        parent=end_node.parent
        child=end_node
        while parent:
           
            
            cv2.line(image,child.pos,parent.pos,color,self.conn_thickness)
            cv2.circle(image,parent.pos,self.node_radius,self.node_thickness)
            child=parent
            parent=child.parent
            

    
                
if __name__=="__main__":
    maze=cv2.imread("task_3/maze.png",0)
    
    new_img=deepcopy(maze)
    prm=PRM(maze)
    prm.sample_c_space(200,[20,maze.shape[1]-30],[30,maze.shape[0]-30])
    start_node=Node((40,320))
    end_node=Node((100,320))
    # start_node=Node((160,40))
    # end_node=Node((430,300))
    prm.nodes.append(start_node)
    prm.nodes.append(end_node)
    prm.draw_nodes()
    cv2.waitKey(0)
    prm.make_connections(5)
    
    img=cv2.imread("task_3/maze.png",0)
    print((img.shape[0]*2,img.shape[1]*2))
    img=cv2.resize(img,(img.shape[1]*2,img.shape[0]*2))
    
    
    #print(prm.dijkstra(start_node,end_node,img))
    print(prm.a_star(start_node,end_node))
    
    prm.draw_path(end_node,20,image=new_img)
    
    cv2.imshow("win2",new_img)
    cv2.waitKey(0)
    


    