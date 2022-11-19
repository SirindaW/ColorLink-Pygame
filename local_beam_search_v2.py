from random import randint
from itertools import permutations
from re import search
import time
import os
import psutil
import tracemalloc

import pygame
Target = []
Map = []
line_pattern = "|\+!%^"
search_count = 0


class node:  # node structure of each point in map
    def __init__(self, attribute, visited=False, previous=[-1, -1], first='', parent=''):
        self.attribute = attribute
        self.visited = visited
        self.prev = previous
        self.first = ''
        self.parent = ''

    def __str__(self):
        return str(self.attribute)


def bfs(start, finish, way_pattern):  # normal breath first search
    global search_count
    executeCount = 0
    bfs_queue = []
    bfs_queue.append(start)
    Map[start[0]][start[1]].visited = True
    Map[finish[0]][finish[1]].visited = False
    Map[start[0]][start[1]].prev = [-1, -1]
    while len(bfs_queue) > 0:
        executeCount += 1

        # temp is first position in queue for search in bfs
        temp = bfs_queue.pop(0)
        Map[temp[0]][temp[1]].visited = True
        # if wp==2:
        # print("node"+str(temp)+" prev "+str(Map[temp[0]][temp[1]].prev)+"finish "+str(finish) +" "+ str(Map[finish[0]][finish[1]].visited))
        if temp[1] < 9:
            if Map[temp[0]][temp[1]+1].visited == False:
                Map[temp[0]][temp[1]+1].prev = [temp[0], temp[1]]
                if not Map[temp[0]][temp[1]+1].attribute.isalpha():
                    if finish[1] >= temp[1]:
                        bfs_queue.append([temp[0], temp[1]+1])
                elif temp[0] == finish[0] and temp[1]+1 == finish[1]:
                    if finish[1] >= temp[1]:
                        bfs_queue.append([temp[0], temp[1]+1])
        if temp[1] > 0:
            if Map[temp[0]][temp[1]-1].visited == False:
                Map[temp[0]][temp[1]-1].prev = [temp[0], temp[1]]
                if not Map[temp[0]][temp[1]-1].attribute.isalpha():
                    if finish[1] <= temp[1]:
                        bfs_queue.append([temp[0], temp[1]-1])
                elif temp[0] == finish[0] and temp[1]-1 == finish[1]:
                    if finish[1] <= temp[1]:
                        bfs_queue.append([temp[0], temp[1]-1])
        if temp[0] > 0:
            if Map[temp[0]-1][temp[1]].visited == False:
                Map[temp[0]-1][temp[1]].prev = [temp[0], temp[1]]
                if not Map[temp[0]-1][temp[1]].attribute.isalpha():
                    if finish[0] <= temp[0]:
                        bfs_queue.append([temp[0]-1, temp[1]])
                elif temp[0]-1 == finish[0] and temp[1] == finish[1]:
                    if finish[0] <= temp[0]:
                        bfs_queue.append([temp[0]-1, temp[1]])
        if temp[0] < 9:
            if Map[temp[0]+1][temp[1]].visited == False:
                Map[temp[0]+1][temp[1]].prev = [temp[0], temp[1]]
                if not Map[temp[0]+1][temp[1]].attribute.isalpha():
                    if finish[0] >= temp[0]:
                        bfs_queue.append([temp[0]+1, temp[1]])
                elif temp[0]+1 == finish[0] and temp[1] == finish[1]:
                    if finish[0] >= temp[0]:
                        bfs_queue.append([temp[0]+1, temp[1]])

        if temp == finish:
            # print("found")
            PreviousPoint = Map[temp[0]][temp[1]].prev
            while PreviousPoint != start:
                # print("prevend" + str(Map[PreviousPoint[1]][PreviousPoint[0]].prev))
                Map[PreviousPoint[0]][PreviousPoint[1]
                                      ].attribute = line_pattern[way_pattern]
                PreviousPoint = Map[PreviousPoint[0]][PreviousPoint[1]].prev
            # print("end" + str(Map[temp[1]][temp[0]].prev))
            Map[start[0]][start[1]].visited = True
            Map[finish[0]][finish[1]].visited = True
            search_count += executeCount
            # print("execcount = "+str(executeCount))
            return 1
    return 0


def resetvisited():  # reset visited for next pair of point
    for i in range(10):
        for j in range(10):
            if Map[i][j].attribute == "-":
                Map[i][j].visited = False


def set(Map):  # reset map if current pair of point don't make line successfully
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


# allmap
allMap = [[[0, 9], [5, 0], [1, 3], [7, 2], [3, 3], [4, 7], [4, 8], [8, 7]],
          [[3, 0], [1, 6], [1, 5], [7, 1], [0, 8], [5, 8], [2, 1], [7, 3]],
          [[2, 7], [6, 8], [8, 0], [7, 9], [0, 9], [5, 4], [3, 4], [5, 5]],
          [[0, 2], [6, 1], [7, 0], [1, 6], [8, 1], [6, 6], [3, 6], [2, 3]],
          [[0, 0], [4, 0], [5, 1], [1, 9], [8, 0], [3, 8], [6, 1], [3, 5]],
          [[6, 8], [3, 7], [8, 0], [7, 9], [0, 9], [5, 4], [3, 4], [5, 5]],
          [[5, 4], [0, 9], [7, 9], [8, 0], [6, 1], [3, 5], [3, 3], [6, 4]]]

Map_Marker = 'A'
mapSize = 10
pair_count = 4
point_count = 8


def gen_new_map():
    way_pattern = 0  # make different line for different pair
    success = 0  # count number of pair connected successfully
    line_path = []
    for i in range(10):  # set first map
        temp = []
        for j in range(10):
            temp.append(node("-"))
        Map.append(temp)
    print(str(Map))
    mapChoose = randint(0, len(allMap)-1)
    Target = allMap[mapChoose]
    print(Target)

    for i in range(point_count):  # mark "ABCDE" in map where point exist
        Map[Target[i][0]][Target[i][1]].attribute = chr(ord(Map_Marker)+(i//2))

    start_time = int(round(time.time()*1000))
    tracemalloc.start()
    pair_set = []  # set of pair
    for i in range(0, point_count, 2):  # add each pair to pair_set
        pair_set.append([Target[i], Target[i + 1]])

    perm = list(permutations(pair_set))

    for j in range(len(perm)):  # try bfs from permutation
        for k in range(len(perm[j])):
            start = perm[j][k][0]
            finish = perm[j][k][1]
            # print("bfs"+ str(start))
            success += bfs(start, finish, way_pattern)
            way_pattern += 1
            resetvisited()
        # reset if all pair aren't connected
        if success < pair_count and j != len(perm)-1:
            temp = Target.pop(0)
            Target.append(temp)
            temp = Target.pop(0)
            Target.append(temp)
            set(Map)
            way_pattern = 0
            success = 0
        else:
            for n in range(len(perm[0])):
                path_each = []
                end = perm[0][n][1]
                start = perm[0][n][0]

                path_each.append(end)
                PreviousPoint = Map[perm[0][n][1][0]][perm[0][n][1][1]].prev
                while PreviousPoint != start:
                    path_each.append(PreviousPoint)
                    PreviousPoint = Map[PreviousPoint[0]
                                        ][PreviousPoint[1]].prev
                path_each.append(start)
                # reversePosition(path_each)
                line_path.append(path_each)
            break  # end when all pair connected
    end_time = int(round(time.time()*1000))
    end_mem = process_memory()
    '''for j in range(pair_count): #bfs for all pair
        for i in range(pair_count): #bfs for each pair
            start = Target.pop(0)
            Target.append(start)
            finish = Target.pop(0) 
            Target.append(finish)
            # print("bfs"+ str(start))
            success+=bfs(start,finish,way_pattern)
            way_pattern+=1
            resetvisited()
        # print(success)
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
    for i in range(10):  # print result
        for j in range(10):
            print(Map[i][j].attribute, end=' ')
        print()
    for i in range(pair_count):
        print("path "+chr(65+i) + " : "+str(line_path[i]))
    print("Searched {0} time".format(search_count))
    timeUse = end_time-start_time
    print("Searched time used {} millisecond".format(timeUse))
    memUsed = list(tracemalloc .get_traced_memory())

    print("Searched memory current used {:,} byte, peak memory usage {:,} byte".format(
        memUsed[0], memUsed[1]))
    tracemalloc.stop()

    return [line_path, timeUse, memUsed[1]]

# ---------------------------------------------------------------------------pygame------------------------------------------------------------------------------------------


def draw_text(text, x, y, color, size):
    font = "DiloWorld.ttf"
    font = pygame.font.Font(font, size)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def draw_grid(rowcol, width, numOfGrid, recSize, heightStart):
    gridWidthStart = ((width/(numOfGrid*2)))-((recSize*rowcol)/2)
    for row in range(rowcol):
        for col in range(rowcol):
            pygame.draw.rect(
                screen, white, (gridWidthStart, heightStart, recSize+(row*recSize), recSize+(col*recSize)), 1)


def draw_color(coor, color):
    gridWidthStart = ((WIDTH/(gridCount*2))) - \
        ((gridRecSize*gridRowCol)/2)
    x, y = coor[1], coor[0]
    pygame.draw.circle(screen, color, (gridWidthStart+(gridRecSize/2)+(x*gridRecSize),
                       gridHeightStart+(gridRecSize/2)+(y*gridRecSize)), (gridRecSize/2)-5)


def gen_map(coorColor):
    color, coor = coorColor[1], coorColor[0]
    for count in range(len(coor)):
        draw_color(coor[count], color[count])


def go_to(color, coors):
    gridWidthStart = ((WIDTH/(gridCount*2))) - \
        ((gridRecSize*gridRowCol)/2)
    for count in range(len(coors)-1):
        x, y = coors[count][1], coors[count][0]
        nx, ny = coors[count + 1][1], coors[count + 1][0]
        hrect = pygame.Rect(gridWidthStart+(gridRecSize/5) +
                            (x*gridRecSize), 0, (gridRecSize/1.6), 0)
        wrect = pygame.Rect(0, gridHeightStart+(gridRecSize/5) +
                            (y*gridRecSize), 0, (gridRecSize/1.6))
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
            draw_text('path not connected', 220, 25, red)
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
gridCount = 1
gridRowCol = 10
gridRecSize = 60
gridHeightStart = (HEIGHT/2)-((gridRecSize*gridRowCol)/2)-10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60
color = [pink, blue, green, yellow]
coorColor = [[], []]
info = gen_new_map()
line_path = info[0]
timeUsed = info[1]
memUsed = info[2]
for path in line_path:
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
                coorColor = [[], []]
                Map = []
                info = gen_new_map()
                line_path = info[0]
                timeUsed = info[1]
                memUsed = info[2]
                for path in line_path:
                    coorColor[0].extend([path[0], path[len(path)-1]])
                for c in color:
                    coorColor[1].extend([c, c])

    draw_text('Heuristic Search', (WIDTH/(gridCount*2)), 90, white, 45)
    draw_text('Searched time :', (WIDTH/(gridCount*2))
              - 110, HEIGHT-120, white, 30)
    draw_text(str(timeUsed) + ' milliseconds', (WIDTH/(gridCount*2))
              + 120, HEIGHT-120, red, 30)
    draw_text('Searched memory used :', (WIDTH/(gridCount*2))
              - 90, HEIGHT-70, white, 30)
    draw_text(str(memUsed) + ' bytes', (WIDTH/(gridCount*2))
              + 170, HEIGHT-70, red, 30)

    inrect = pygame.Rect(200, (HEIGHT/2)-40, 160, 80)
    outrect = pygame.Rect(206, (HEIGHT/2)-34, 148, 68)
    pygame.draw.rect(screen, purple, inrect, 0, 20)
    pygame.draw.rect(screen, white, outrect, 0, 16)
    draw_text('New Map', 280, HEIGHT/2, purple, 30)
    draw_grid(gridRowCol, WIDTH, gridCount,
              gridRecSize, gridHeightStart)
    gen_map(coorColor)

    for i in range(pair_count):
        go_to(color[i], line_path[i])

    pygame.display.update()
    clock.tick(FPS)
