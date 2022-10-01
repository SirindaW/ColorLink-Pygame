from random import random, randrange
from itertools import permutations
from re import search 
import time
import os, psutil
Target = []
Map =[]
line_pattern = "|\+!%^"
search_count = 0
class node: #node structure of each point in map
    def __init__(self,attribute,visited=False,previous=[-1,-1],first = '',parent='') :
        self.attribute = attribute
        self.visited = visited
        self.prev = previous
        self.first =''
        self.parent = ''
def bfs(start,finish,way_pattern): #normal breath first search
    global search_count
    executeCount=0
    bfs_queue = []
    bfs_queue.append(start)
    Map[start[0]][start[1]].visited=True
    Map[finish[0]][finish[1]].visited=False
    Map[start[0]][start[1]].prev=[-1,-1]
    while len(bfs_queue)>0:
        executeCount+=1
        
        temp = bfs_queue.pop(0) #temp is first position in queue for search in bfs
        Map[temp[0]][temp[1]].visited=True
        #if wp==2:
            #print("node"+str(temp)+" prev "+str(Map[temp[0]][temp[1]].prev)+"finish "+str(finish) +" "+ str(Map[finish[0]][finish[1]].visited))
        if temp[1]<9:
            if Map[temp[0]][temp[1]+1].visited==False:
                Map[temp[0]][temp[1]+1].prev = [temp[0],temp[1]]
                if not Map[temp[0]][temp[1]+1].attribute.isalpha():
                    bfs_queue.append([temp[0],temp[1]+1])
                elif temp[0]==finish[0] and temp[1]+1==finish[1]:
                    bfs_queue.append([temp[0],temp[1]+1])
        if temp[1]>0:
            if Map[temp[0]][temp[1]-1].visited==False:
                Map[temp[0]][temp[1]-1].prev = [temp[0],temp[1]]
                if not Map[temp[0]][temp[1]-1].attribute.isalpha():
                    bfs_queue.append([temp[0],temp[1]-1])
                elif temp[0]==finish[0] and temp[1]-1==finish[1]:
                    bfs_queue.append([temp[0],temp[1]-1])
        if temp[0]>0:
            if Map[temp[0]-1][temp[1]].visited==False :
                Map[temp[0]-1][temp[1]].prev = [temp[0],temp[1]]
                if not Map[temp[0]-1][temp[1]].attribute.isalpha():
                    bfs_queue.append([temp[0]-1,temp[1]])
                elif temp[0]-1==finish[0] and temp[1]==finish[1]:
                    bfs_queue.append([temp[0]-1,temp[1]])
        if temp[0]<9: 
            if Map[temp[0]+1][temp[1]].visited==False :
                Map[temp[0]+1][temp[1]].prev = [temp[0],temp[1]] 
                if not Map[temp[0]+1][temp[1]].attribute.isalpha():
                    bfs_queue.append([temp[0]+1,temp[1]])
                elif temp[0]==finish[0] and temp[1]+1==finish[1]:
                    bfs_queue.append([temp[0]+1,temp[1]])
        
        
        
        
        if temp == finish :
            #print("found")
            PreviousPoint=Map[temp[0]][temp[1]].prev
            while PreviousPoint!=start:
                #print("prevend" + str(Map[PreviousPoint[1]][PreviousPoint[0]].prev))
                Map[PreviousPoint[0]][PreviousPoint[1]].attribute = line_pattern[way_pattern]
                PreviousPoint=Map[PreviousPoint[0]][PreviousPoint[1]].prev 
            #print("end" + str(Map[temp[1]][temp[0]].prev))
            Map[start[0]][start[1]].visited = True
            Map[finish[0]][finish[1]].visited = True
            search_count+=executeCount
            #print("execcount = "+str(executeCount))
            return 1
    return 0
def resetvisited(): #reset visited for next pair of point
    for i in range(10):
        for j in range(10):
            if Map[i][j].attribute=="-":
                Map[i][j].visited=False
def set(Map): #reset map if current pair of point don't make line successfully 
    '''for i in range(point_count): #mark "x" in map where point exist 
        Map[y[i]][x[i]].attribute = 'x'
        Map[y[i]][x[i]].visited = False'''
    for i in range(10):
        for j in range(10):
            if not Map[i][j].attribute.isalpha():
                Map[i][j].attribute = "-"
            Map[i][j].visited = False
def reversePosition(line_path):
    for i in line_path:
        temp = i[0]
        i[0] = i[1]
        i[1] = temp
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss
for i in range(10): #set first map
    temp = []
    for j in range(10):
        temp.append(node("-"))
    Map.append(temp)
x= [3,6,3,0,5,7,2,5] # position of point in x-axis (point x[0] is paired of poit x[1])
y= [7,7,0,6,0,6,0,5] # position of point in y-axis (point y[0] is paired of poit y[1])

pair_count = len(x)//2
point_count = len(x)
Map_Marker = 'A'
for i in range(point_count): #mark "ABCDE" in map where point exist 
    position = [y[i],x[i]]
    Map[y[i]][x[i]].attribute = chr(ord(Map_Marker)+(i//2))
    Target.append(position)
start_time = int(round(time.time()*1000))
start_mem = process_memory()
print('target :',Target)
way_pattern = 0 #make different line for different pair
success=0 #count number of pair connected successfully
pair_set = [] #set of pair
pair_select = 0 
for j in range(pair_count): #add each pair to pair_set
    pair = []
    pair.append(Target[pair_select])
    pair.append(Target[pair_select+1])
    pair_select+=2
    pair_set.append(pair)
perm =permutations(pair_set)
perm = list(perm)
#print(str(perm))
#print(len(perm))
line_path = []
for j in range(len(perm)): #try bfs from permutation
    for k in range(len(perm[j])):
        start = perm[j][k][0]
        finish = perm[j][k][1]
        #print("bfs"+ str(start))
        success+=bfs(start,finish,way_pattern)
        way_pattern+=1
        resetvisited()
    if success<pair_count and j!=len(perm)-1: #reset if all pair aren't connected
        temp = Target.pop(0)
        Target.append(temp)
        temp = Target.pop(0)
        Target.append(temp)
        set(Map)
        way_pattern = 0
        success=0
    else :
        for n in range(len(perm[0])):
                path_each = []
                end = perm[0][n][1]
                start = perm[0][n][0]
                path_each.append(end)
                PreviousPoint=Map[perm[0][n][1][0]][perm[0][n][1][1]].prev
                while PreviousPoint!=start:
                    path_each.append(PreviousPoint)
                    PreviousPoint=Map[PreviousPoint[0]][PreviousPoint[1]].prev
                path_each.append(start)
                #reversePosition(path_each)
                line_path.append(path_each)
        break #end when all pair connected
end_time = int(round(time.time()*1000))
end_mem = process_memory()
'''for j in range(pair_count): #bfs for all pair
    for i in range(pair_count): #bfs for each pair
        start = Target.pop(0)
        Target.append(start)
        finish = Target.pop(0) 
        Target.append(finish)
        #print("bfs"+ str(start))
        success+=bfs(start,finish,way_pattern)
        way_pattern+=1
        resetvisited()
    #print(success)
    if success<pair_count and j!=pair_count-1: #reset if all pair aren't connected
        temp = Target.pop(0)
        Target.append(temp)
        temp = Target.pop(0)
        Target.append(temp)
        set(Map)
        way_pattern = 0
        success=0
    else :
        break #end when all pair connected'''
for i in range(10): #print result
    for j in range(10):
        print(Map[i][j].attribute,end=' ')
    print()
for i in range(pair_count):
    print("path "+chr(65+i)+ " : "+str(line_path[i]))
print("Searched {0} time".format(search_count))
print("Searched time used {} millisecond".format(end_time-start_time))
print("Searched memory used {:,} byte".format(end_mem-start_mem))