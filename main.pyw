import pygame
from random import randint
from itertools import permutations
import time
import os, psutil
import tracemalloc

class node :
    def __init__(self,attr,first='',parent='',visited = False,prev=[-1,-1]):
        self.attr = attr
        self.visited = visited
        self.prev = prev
        self.first = first #start from end point or start point
        self.parent = parent #which Char this node start from
    def __str__(self):
        return "attr: {0} visited : {1} prev : {2}".format(self.attr,self.visited,self.prev)

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def gen_new_map():

    def gen_Map(Map,target):
        #print(target)

        target_Marker = 'A'
        for i in range(0,2*targetNo,2):
            Map[target[i][0]][target[i][1]] = node(target_Marker)
            Map[target[i+1][0]][target[i+1][1]] = node(target_Marker)
            target_Marker = chr(ord(target_Marker)+1)

    def reset_Map(Map):
        for i in range(0,mapSize):
            for j in range(0,mapSize):
                if(Map[i][j].attr != Map[i][j].parent):
                    Map[i][j].attr='-'
                    Map[i][j].parent = ''
                    Map[i][j].first = ''
                    Map[i][j].prev=[-1,-1]
                    Map[i][j].visited=False

    def show_Map(Map):
        for i in range(mapSize):
            for j in range(mapSize):
                print(Map[i][j].attr,end=' ')
            print()

    def find_color(Map,reroll):
        color_list=[]
        for i in range(mapSize):
            for j in range(mapSize):
                if(Map[i][j].attr != '-'):
                    color_list.append([i,j])
        color_list=sorted(color_list,key=lambda x: Map[x[0]][x[1]].attr)
        while(reroll > 0):
            tempTarget =  color_list.pop(0)
            color_list.append(tempTarget)
            tempTarget =  color_list.pop(0)
            color_list.append(tempTarget)
            reroll-=1
        return color_list

    def resetVisited(Map):
        for i in range(mapSize):
            for j in range(mapSize):
                if Map[i][j].attr == "-":
                    Map[i][j].visited=False

    def set(Map): #reset map if current pair of point don't make line successfully 
        for i in range(10):
            for j in range(10):
                if not Map[i][j].attr.isalpha():
                    Map[i][j].attr = "-"
                Map[i][j].visited = False
                
    def reversePosition(line_path):
        for i in line_path:
            temp = i[0]
            i[0] = i[1]
            i[1] = temp
            
    def bfs(start,finish,way_pattern): #normal breath first search
        search_count = 0
        executeCount = 0
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
                    if not Map[temp[0]][temp[1]+1].attr.isalpha():
                        bfs_queue.append([temp[0],temp[1]+1])
                    elif temp[0]==finish[0] and temp[1]+1==finish[1]:
                        bfs_queue.append([temp[0],temp[1]+1])
            if temp[1]>0:
                if Map[temp[0]][temp[1]-1].visited==False:
                    Map[temp[0]][temp[1]-1].prev = [temp[0],temp[1]]
                    if not Map[temp[0]][temp[1]-1].attr.isalpha():
                        bfs_queue.append([temp[0],temp[1]-1])
                    elif temp[0]==finish[0] and temp[1]-1==finish[1]:
                        bfs_queue.append([temp[0],temp[1]-1])
            if temp[0]>0:
                if Map[temp[0]-1][temp[1]].visited==False :
                    Map[temp[0]-1][temp[1]].prev = [temp[0],temp[1]]
                    if not Map[temp[0]-1][temp[1]].attr.isalpha():
                        bfs_queue.append([temp[0]-1,temp[1]])
                    elif temp[0]-1==finish[0] and temp[1]==finish[1]:
                        bfs_queue.append([temp[0]-1,temp[1]])
            if temp[0]<9: 
                if Map[temp[0]+1][temp[1]].visited==False :
                    Map[temp[0]+1][temp[1]].prev = [temp[0],temp[1]] 
                    if not Map[temp[0]+1][temp[1]].attr.isalpha():
                        bfs_queue.append([temp[0]+1,temp[1]])
                    elif temp[0]==finish[0] and temp[1]+1==finish[1]:
                        bfs_queue.append([temp[0]+1,temp[1]])
            
            
            if temp == finish :
                #print("found")
                PreviousPoint=Map[temp[0]][temp[1]].prev
                while PreviousPoint!=start:
                    #print("prevend" + str(Map[PreviousPoint[1]][PreviousPoint[0]].prev))
                    Map[PreviousPoint[0]][PreviousPoint[1]].attr = line_pattern[way_pattern]
                    PreviousPoint=Map[PreviousPoint[0]][PreviousPoint[1]].prev 
                #print("end" + str(Map[temp[1]][temp[0]].prev))
                Map[start[0]][start[1]].visited = True
                Map[finish[0]][finish[1]].visited = True
                search_count+=executeCount
                #print("execcount = "+str(executeCount))
                return 1
        return 0

    def bidirect_bfs(Map,finished,retry,linePath,Target):
        #target_list = find_color(Map,retry)
        target_list = Target[retry]
        #print('targetlist : ',target_list)
        di_r = [0,0,-1,1]
        di_c = [1,-1,0,0]
        for i in range(0,2*targetNo,2):
            resetVisited(Map)
            q_st = []
            q_en = []
            pair_path_st=[]
            pair_path_en=[]
            q_st.append([target_list[i][0],target_list[i][1]])
            q_en.append([target_list[i+1][0],target_list[i+1][1]])
            st_point_i = q_st[0][0]
            st_point_j = q_st[0][1]
            en_point_i = q_en[0][0]
            en_point_j = q_en[0][1]
            Map[st_point_i][st_point_j].first = 'st'
            Map[st_point_i][st_point_j].visited = True
            Map[st_point_i][st_point_j].parent = Map[st_point_i][st_point_j].attr
            Map[en_point_i][en_point_j].first = 'en'
            Map[en_point_i][en_point_j].visited = True
            Map[en_point_i][en_point_j].parent = Map[en_point_i][en_point_j].attr
            while(len(q_st) > 0 or len(q_en) > 0):
                #print('bfs')
                #show_Map(Map)

                #start point
                if(len(q_st)>0):
                    cur_st_i = q_st[0][0]
                    cur_st_j = q_st[0][1]
                    q_st.pop(0)
                    #print('START Q FRONT:',cur_st_i,cur_st_j)
                    if(not(cur_st_i == st_point_i and cur_st_j  == st_point_j)):
                        #Map[cur_st_i][cur_st_j].attr = str.lower(Map[Map[cur_st_i][cur_st_j].prev[0]][Map[cur_st_i][cur_st_j].prev[1]].attr)
                        Map[cur_st_i][cur_st_j].parent = Map[Map[cur_st_i][cur_st_j].prev[0]][Map[cur_st_i][cur_st_j].prev[1]].parent
                        Map[cur_st_i][cur_st_j].first = Map[Map[cur_st_i][cur_st_j].prev[0]][Map[cur_st_i][cur_st_j].prev[1]].first
                    
                    for j in range (4):
                        nst_i = cur_st_i+di_r[j]
                        nst_j = cur_st_j+di_c[j]
                        if(nst_i < 0 or nst_i >= mapSize or nst_j < 0 or nst_j >=mapSize or Map[nst_i][nst_j].attr != '-'):
                            continue
                        if(Map[nst_i][nst_j].visited):
                            if (Map[cur_st_i][cur_st_j].parent == Map[nst_i][nst_j].parent and Map[cur_st_i][cur_st_j].first != Map[nst_i][nst_j].first):
                                #print('found')
                                #print('at :',nst_i,nst_j)
                                finished+=1
                                while(not len(q_st)<=0):
                                    q_st.pop()
                                while(not len(q_en)<=0):
                                    q_en.pop()
                                if([nst_i,nst_j] == [en_point_i,en_point_j]):
                                    break;
                                Map[nst_i][nst_j].attr = str.lower(Map[nst_i][nst_j].parent)
                                pair_path_st.append([nst_i,nst_j])
                                previ = Map[nst_i][nst_j].prev[0]
                                prevj = Map[nst_i][nst_j].prev[1]
                                while([previ,prevj] != [en_point_i,en_point_j]):
                                    pair_path_en.append([previ,prevj])
                                    if([previ,prevj] == [-1,-1] or [previ,prevj] == [en_point_i,en_point_j]):
                                        break;
                                    Map[previ][prevj].attr = str.lower(Map[nst_i][nst_j].parent)
                                    previ_temp=Map[previ][prevj].prev[0]
                                    prevj_temp=Map[previ][prevj].prev[1]
                                    previ=previ_temp
                                    prevj=prevj_temp
                                    #print('path en:',pair_path_en)
                                previ=cur_st_i
                                prevj=cur_st_j
                                while([previ,prevj] != [st_point_i,st_point_j]):
                                    pair_path_st.append([previ,prevj])
                                    if([previ,prevj] == [-1,-1] or [previ,prevj] == [en_point_i,en_point_j]):
                                        break;
                                    Map[previ][prevj].attr =  str.lower(Map[nst_i][nst_j].parent)
                                    previ_temp=Map[previ][prevj].prev[0]
                                    prevj_temp=Map[previ][prevj].prev[1]
                                    previ=previ_temp
                                    prevj=prevj_temp
                                    #print('path st:',pair_path_st)
                                pair_path_st.append([st_point_i,st_point_j])
                                pair_path_en.append([en_point_i,en_point_j])
                                pair_path_st.reverse()
                                linePath.append(pair_path_st+pair_path_en)
                                break
                            continue
                        Map[nst_i][nst_j].prev = [cur_st_i,cur_st_j] 
                        Map[nst_i][nst_j].visited = True
                        q_st.append([nst_i,nst_j])

                #end point
                if(len(q_en)>0):
                    cur_en_i = q_en[0][0]
                    cur_en_j = q_en[0][1]
                    q_en.pop(0)
                    #print('END Q FRONT:',cur_en_i,cur_en_j)
                    if(not (cur_en_i == en_point_i and cur_en_j  == en_point_j)):
                        #Map[cur_en_i][cur_en_j].attr = str.lower(Map[Map[cur_en_i][cur_en_j].prev[0]][Map[cur_en_i][cur_en_j].prev[1]].attr)
                        Map[cur_en_i][cur_en_j].parent = Map[Map[cur_en_i][cur_en_j].prev[0]][Map[cur_en_i][cur_en_j].prev[1]].parent
                        Map[cur_en_i][cur_en_j].first = Map[Map[cur_en_i][cur_en_j].prev[0]][Map[cur_en_i][cur_en_j].prev[1]].first
                    for j in range (4):
                        nst_i = cur_en_i+di_r[j]
                        nst_j = cur_en_j+di_c[j]
                        if(nst_i < 0 or nst_i >= mapSize or nst_j < 0 or nst_j >=mapSize or Map[nst_i][nst_j].attr != '-'):
                            continue
                        if(Map[nst_i][nst_j].visited):
                            if (Map[cur_en_i][cur_en_j].parent == Map[nst_i][nst_j].parent and Map[cur_en_i][cur_en_j].first != Map[nst_i][nst_j].first):
                                #print('found')
                                #print('at :',nst_i,nst_j)
                                finished+=1
                                while(not len(q_st)<=0):
                                    q_st.pop()
                                while(not len(q_en)<=0):
                                    q_en.pop()
                                if([nst_i,nst_j] == [st_point_i,st_point_j]):
                                    break;
                                Map[nst_i][nst_j].attr = str.lower(Map[nst_i][nst_j].parent)
                                pair_path_st.append([nst_i,nst_j])
                                previ = Map[nst_i][nst_j].prev[0]
                                prevj = Map[nst_i][nst_j].prev[1]
                                while([previ,prevj] != [st_point_i,st_point_j]):
                                    pair_path_st.append([previ,prevj])
                                    if([previ,prevj] == [-1,-1] or [previ,prevj] == [st_point_i,st_point_j]):
                                        break;
                                    Map[previ][prevj].attr = str.lower(Map[nst_i][nst_j].parent)
                                    previ_temp=Map[previ][prevj].prev[0]
                                    prevj_temp=Map[previ][prevj].prev[1]
                                    previ=previ_temp
                                    prevj=prevj_temp
                                    #print('path st:',pair_path_st)
                                previ=cur_en_i
                                prevj=cur_en_j
                                while([previ,prevj] != [en_point_i,en_point_j]):
                                    pair_path_en.append([previ,prevj])
                                    if([previ,prevj] == [-1,-1] or [previ,prevj] == [st_point_i,st_point_j]):
                                        break;
                                    Map[previ][prevj].attr = str.lower(Map[nst_i][nst_j].parent)
                                    previ_temp=Map[previ][prevj].prev[0]
                                    prevj_temp=Map[previ][prevj].prev[1]
                                    previ=previ_temp
                                    prevj=prevj_temp
                                    #print('path en:',pair_path_en)
                                pair_path_st.append([st_point_i,st_point_j])
                                pair_path_en.append([en_point_i,en_point_j])
                                pair_path_st.reverse()
                                linePath.append(pair_path_st+pair_path_en)
                                break
                            continue
                        Map[nst_i][nst_j].prev = [cur_en_i,cur_en_j] 
                        Map[nst_i][nst_j].visited = True
                        q_en.append([nst_i,nst_j])
        print(finished)
        if(finished!=targetNo):
            reset_Map(Map)
            #print(target_list)
            finished=0
            return False
        return True


    #allmap
    allMap = [[[7,3],[7,6] , [0,3],[6,0] , [0,5],[6,7] , [0,2],[5,5]], [[0,1],[5,2] , [4,3],[6,2] , [5,3],[6,4]  , [0,8],[9,3]], 
              [[0,9],[5,0] , [1,3],[7,2] , [3,3],[4,7] , [4,8],[8,7]], [[8,2],[9,4] , [4,0],[6,7] , [2,7],[8,5] , [2,2],[4,6]],
              [[9,1],[2,8] , [1,2],[7,5] , [2,2],[8,4] , [1,6],[7,4]], [[0,6],[9,9] , [0,7],[7,8] , [0,9],[8,8] , [7,4],[5,7]], 
              [[2,0],[7,9] , [3,0],[1,6] , [7,1],[1,5] , [2,1],[7,2]], [[3,0],[1,6] , [1,5],[7,1] , [0,8],[5,8] , [2,1],[7,3]],
              [[2,7],[6,8] , [8,0],[7,9] , [0,9],[5,4] , [3,4],[5,5]], [[0,2],[6,1] , [7,0],[1,6] , [8,1],[6,6] , [3,6],[2,3]],
              [[5,1],[6,8] , [1,6],[9,6] , [3,2],[6,7] , [8,1],[5,4]], [[0,0],[4,5] , [1,0],[2,7] , [3,2],[2,9] , [5,4],[7,7]],
              [[0,0],[4,0] , [5,1],[1,9] , [8,0],[3,8] , [6,1],[3,5]], [[5,1],[6,8] , [1,6],[9,6] , [3,2],[6,7] , [8,1],[5,4]],
              [[0,2],[6,1] , [7,0],[1,6] , [8,1],[6,4] , [2,3],[6,3]], [[6,8],[3,7] , [8,0],[7,9] , [0,9],[5,4] , [3,4],[5,5]],
              [[5,4],[0,9] , [7,9],[8,0] , [6,1],[3,5] , [3,3],[6,4]], [[2,0],[7,9] , [3,0],[1,5] , [0,9],[6,8] , [2,1],[7,2]]] 
    
    line_pattern = "|\+!%^"
    targetNo = 4
    mapSize = 10
    Target = []
    Map = [[node('-') for _ in range(mapSize)] for _ in range(mapSize)]
    mapChoose = randint(0, len(allMap)-1)
    print(mapChoose)
    x = list(allMap[mapChoose][i][1] for i in range(len(allMap[mapChoose]))) # position of point in x-axis (point x[0] is paired of poit x[1])
    y = list(allMap[mapChoose][i][0] for i in range(len(allMap[mapChoose]))) # position of point in y-axis (point y[0] is paired of poit y[1])

    pair_count = len(x)//2
    point_count = len(x)
    Map_Marker = 'A'
    for i in range(point_count): #mark "ABCDE" in map where point exist 
        position = [y[i],x[i]]
        Map[y[i]][x[i]].attr = chr(ord(Map_Marker)+(i//2))
        Target.append(position)
    way_pattern = 0 #make different line for different pair
    success = 0 #count number of pair connected successfully
    pair_set = [] #set of pair
    pair_select = 0 
    for j in range(pair_count): #add each pair to pair_set
        pair = []
        pair.append(Target[pair_select])
        pair.append(Target[pair_select+1])
        pair_select+=2
        pair_set.append(pair)
    perm = list(permutations(pair_set))
    #print(str(perm))
    #print(len(perm))


    #----------------------------------------------------------------------------two way BFS------------------------------------------------------------------------------------------------

    maximumRetry = 0
    permBi = perm[0:]
    for i in range(0,len(permBi)):
        permBi[i]=list(permBi[i])
        temp_single_target = []
        for j in range(0,len(permBi[i])):
            st,en = permBi[i][j]
            temp_single_target.append(st)
            temp_single_target.append(en)
        permBi[i]=temp_single_target.copy()
    maximumRetry=len(permBi)-1
    print("Maximum Retry :",maximumRetry)
    reset_Map(Map)
    gen_Map(Map,permBi[0])
    show_Map(Map)
    current_try = 0
    line_path = []
    start_time = int(round(time.time()*1000))
    tracemalloc.start()
    while(not bidirect_bfs(Map,0,current_try,line_path,permBi) and current_try!=maximumRetry):
        current_try+=1
        line_path=[]
        print("Line_Path :",len(line_path))
        #print("Not Possible Retrying Try #{0}".format(current_try+1))
    print('######################')
    end_time = int(round(time.time()*1000))
    memBiBFS  = list(tracemalloc .get_traced_memory())
    tracemalloc.stop()
    show_Map(Map)
    pathsort=[]
    for i in range(len(line_path)):
        start_char=Map[line_path[i][0][0]][line_path[i][0][1]].attr
        temp_sortpath=[]
        temp_sortpath.append(start_char)
        temp_sortpath.append(i)
        pathsort.append(temp_sortpath)
    realLinePath=[]
    pathsort=sorted(pathsort)
    for i in range(len(pathsort)):
        realLinePath.append(line_path[pathsort[i][1]])
        print('Path for',pathsort[i][0],':',line_path[pathsort[i][1]])
    allBiBFSPath = realLinePath
    timeBiBFS = end_time-start_time
    print("Searched time used {} milliseconds".format(timeBiBFS))
    print("Searched memory current used {:,} bytes, peak memory usage {:,} bytes".format(memBiBFS[0], memBiBFS[1])) 
    
    
    #---------------------------------------------------------------BFS---------------------------------------------------------------------------
    
    Map = [[node('-') for _ in range(mapSize)] for _ in range(mapSize)]
    line_path = []
    search_count = 0
 
    for i in range(point_count): #mark "ABCDE" in map where point exist 
        Map[y[i]][x[i]].attr = chr(ord(Map_Marker)+(i//2))
        
    start_time = int(round(time.time()*1000))
    tracemalloc.start()
    for j in range(len(perm)): #try bfs from permutation
        for k in range(len(perm[j])):
            start = perm[j][k][0]
            finish = perm[j][k][1]
            #print("bfs"+ str(start))
            success+=bfs(start,finish,way_pattern)
            way_pattern+=1
            resetVisited(Map)
        if success < pair_count and j!=len(perm)-1: #reset if all pair aren't connected
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
                        PreviousPoint = Map[PreviousPoint[0]][PreviousPoint[1]].prev
                    path_each.append(start)
                    #reversePosition(path_each)
                    line_path.append(path_each)
            break #end when all pair connected
    end_time = int(round(time.time()*1000))
    memBFS  = list(tracemalloc .get_traced_memory())
    tracemalloc.stop()
    for i in range(10): #print result
        for j in range(10):
            print(Map[i][j].attr,end=' ')
        print()
        
    allBFSPath = []
    timeBFS = end_time-start_time

    for i in range(pair_count):
        temp_linePath = line_path[i].copy()
        allBFSPath.append(temp_linePath)
        print("path "+chr(65+i)+ " : "+str(temp_linePath))
        
    print("Searched {0} time".format(search_count))
    print("Searched time used {} milliseconds".format(timeBFS))
    print("Searched memory current used {:,} bytes, peak memory usage {:,} bytes".format(memBFS[0], memBFS[1]))
    
    return [allBFSPath, allBiBFSPath, timeBFS, memBFS, timeBiBFS, memBiBFS]


#---------------------------------------------------------------------------pygame------------------------------------------------------------------------------------------

def draw_text(text, x, y, color, size):
    font = "DiloWorld.ttf"
    font = pygame.font.Font(font, size)
    
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_grid(rowcol, width, numOfGrid, recSize, heightStart, atGrid):
    gridWidthStart = ((width/(numOfGrid*2))*atGrid)-((recSize*rowcol)/2)
    for row in range(rowcol):
        for col in range(rowcol):
            pygame.draw.rect(
                screen, white, (gridWidthStart, heightStart, recSize+(row*recSize), recSize+(col*recSize)), 1)

def draw_color(coor, color, atGrid):
    gridWidthStart = ((WIDTH/(gridCount*2))*atGrid)-((gridRecSize*gridRowCol)/2)
    x, y = coor[1], coor[0]
    pygame.draw.circle(screen, color, (gridWidthStart+(gridRecSize/2)+(x*gridRecSize), gridHeightStart+(gridRecSize/2)+(y*gridRecSize)), (gridRecSize/2)-5)

def gen_map(coorColor, atGrid):
    color, coor = coorColor[1], coorColor[0]
    for count in range(len(coor)):
        draw_color(coor[count], color[count], atGrid) 
        
def go_to(color, coors, atGrid):
    gridWidthStart = ((WIDTH/(gridCount*2))*atGrid)-((gridRecSize*gridRowCol)/2)
    for count in range(len(coors)-1):
        x, y = coors[count][1], coors[count][0]
        nx, ny = coors[count + 1][1], coors[count + 1][0]
        hrect = pygame.Rect(gridWidthStart+(gridRecSize/5)+(x*gridRecSize), 0, (gridRecSize/1.6), 0)
        wrect = pygame.Rect(0, gridHeightStart+(gridRecSize/5)+(y*gridRecSize), 0, (gridRecSize/1.6))
        if x == nx:
            if ny-y >= 0:
                hrect.y = gridHeightStart+(gridRecSize/5)+(y*gridRecSize)
            else:
                hrect.y = gridHeightStart+(gridRecSize/5)+(ny*gridRecSize)
            hrect.h = abs((ny-y))*gridRecSize + (gridRecSize/1.6)
        elif y == ny:
            if nx-x >= 0:
                wrect.x = gridWidthStart+(gridRecSize/5)+(x*gridRecSize)
            else:
                wrect.x = gridWidthStart+(gridRecSize/5)+(nx*gridRecSize)
            wrect.w = abs((nx-x))*gridRecSize + (gridRecSize/1.6)
        else:
            hrect.h = 0
            wrect.w = 0
            draw_text('path not connected',220, 25, red)
        pygame.draw.rect(screen, color, hrect, 0, 10)
        pygame.draw.rect(screen, color, wrect, 0, 10)
        
    
pygame.init()
pygame.display.set_caption('COLOR LINK')
white = (255, 255, 255)
black = (65, 65, 65)
pink = (243, 168, 188)
purple = '#987284'
blue = (158, 231, 245)
red = (245, 173, 148)
green = (180, 249, 165)
yellow = (255, 241, 166)
WIDTH = 1600
HEIGHT = 900
gridCount = 2
gridRowCol = 10
gridRecSize = 60
pairCount = 4
gridHeightStart = (HEIGHT/2)-((gridRecSize*gridRowCol)/2)-10
gridRatio = list(range(1, gridCount*2, 2))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60
color = [pink, blue, green, yellow]
coorColor = [[], []]
info = gen_new_map()
allBFSPath = info[0] 
allBiBFSPath = info[1] 
timeBFS = info[2] 
memBFS = info[3] 
timeBiBFS = info[4] 
memBiBFS = info[5]  
for path in allBFSPath:
    coorColor[0].extend([path[0], path[len(path)-1]])
for c in color:
    coorColor[1].extend([c, c])

running = True

while running:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            if outrect.collidepoint(mouse):
                info = gen_new_map()
                coorColor = [[], []]
                allBFSPath = info[0] 
                allBiBFSPath = info[1] 
                timeBFS = info[2] 
                memBFS = info[3] 
                timeBiBFS = info[4] 
                memBiBFS = info[5]  
                for path in allBFSPath:
                    coorColor[0].extend([path[0], path[len(path)-1]])
                for c in color:
                    coorColor[1].extend([c, c])

    # draw_text(str(pygame.mouse.get_pos()), WIDTH-100, 25, white)
    
    draw_text('Breadth First Search', (WIDTH/(gridCount*2))*gridRatio[0], 90, white, 45)
    draw_text('Searched time :', (WIDTH/(gridCount*2))*gridRatio[0]-110, HEIGHT-120, white, 30)
    draw_text(str(timeBFS) + ' milliseconds', (WIDTH/(gridCount*2))*gridRatio[0]+120, HEIGHT-120, red, 30)
    draw_text('Searched memory used :', (WIDTH/(gridCount*2))*gridRatio[0]-90, HEIGHT-70, white, 30)
    draw_text(str(memBFS[0]) + ' bytes', (WIDTH/(gridCount*2))*gridRatio[0]+170, HEIGHT-70, red, 30)
    
    draw_text('Bidirectional Breadth First Search', (WIDTH/(gridCount*2))*gridRatio[1], 90, white, 45)
    draw_text('Searched time : ', (WIDTH/(gridCount*2))*gridRatio[1]-100, HEIGHT-120, white, 30)
    draw_text(str(timeBiBFS) + ' milliseconds', (WIDTH/(gridCount*2))*gridRatio[1]+120, HEIGHT-120, red, 30)
    draw_text('Searched memory used : ', (WIDTH/(gridCount*2))*gridRatio[1]-80, HEIGHT-70, white, 30)
    draw_text(str(memBiBFS[0]) + ' bytes', (WIDTH/(gridCount*2))*gridRatio[1]+170, HEIGHT-70, red, 30)
    
    inrect = pygame.Rect((WIDTH/2)-80, (HEIGHT/2)-40, 160, 80)
    outrect = pygame.Rect((WIDTH/2)-74, (HEIGHT/2)-34, 148, 68)
    pygame.draw.rect(screen, purple, inrect, 0, 20)
    pygame.draw.rect(screen, white, outrect, 0, 16)
    draw_text('New Map', WIDTH/2, HEIGHT/2, purple, 30)
    for ratio in gridRatio:
        draw_grid(gridRowCol, WIDTH, gridCount, gridRecSize, gridHeightStart, ratio)
        gen_map(coorColor, ratio)
        
    for i in range(pairCount):
        go_to(color[i], allBFSPath[i], gridRatio[0])
        go_to(color[i], allBiBFSPath[i], gridRatio[1])

    pygame.display.update()
    clock.tick(FPS)
