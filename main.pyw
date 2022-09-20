import pygame, random, itertools


def draw_text(text, x, y, color):
    font = "Starborn.ttf"
    font = pygame.font.Font(font, 30)
    
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_grid(num, atGrid):
    gridWidthStart = ((WIDTH/(gridCount*2))*atGrid)-((gridSize*gridRowCol)/2)
    for row in range(num):
        for col in range(num):
            pygame.draw.rect(
                screen, white, (gridWidthStart, gridHeightStart, gridSize+(row*gridSize), gridSize+(col*gridSize)), 1)

def draw_color(coor, color, atGrid):
    gridWidthStart = ((WIDTH/(gridCount*2))*atGrid)-((gridSize*gridRowCol)/2)
    x, y = coor[0], coor[1]
    pygame.draw.circle(screen, color, (gridWidthStart+(gridSize/2)+(x*gridSize), gridHeightStart+(gridSize/2)+(y*gridSize)), (gridSize/2)-5)
            
def rand_coor(num_list, count):
    coordinate = list(itertools.permutations(num_list, 2))
    color = [pink, pink, blue, blue, red, red, green, green, yellow, yellow]
    random.shuffle(coordinate)
    random.shuffle(color)
    return [coordinate[:count], color]

def gen_map(coorColor, atGrid):
    color, coor = coorColor[1], coorColor[0]
    for count in range(len(coor)):
        draw_color(coor[count], color[count], atGrid) 
        
def go_to(color, coors, atGrid):
    gridWidthStart = ((WIDTH/(gridCount*2))*atGrid)-((gridSize*gridRowCol)/2)
    for count in range(len(coors)-1):
        x, y = coors[count][0], coors[count][1]
        nx, ny = coors[count + 1][0], coors[count + 1][1]
        hrect = pygame.Rect(gridWidthStart+(gridSize/5)+(x*gridSize), 0, (gridSize/1.6), 0)
        wrect = pygame.Rect(0, gridHeightStart+(gridSize/5)+(y*gridSize), 0, (gridSize/1.6))
        if x == nx:
            if ny-y >= 0:
                hrect.y = gridHeightStart+(gridSize/5)+(y*gridSize)
            else:
                hrect.y = gridHeightStart+(gridSize/5)+(ny*gridSize)
            hrect.h = abs((ny-y))*(gridSize) + (gridSize/1.6)
        elif y == ny:
            if nx-x >= 0:
                wrect.x = gridWidthStart+(gridSize/5)+(x*gridSize)
            else:
                wrect.x = gridWidthStart+(gridSize/5)+(nx*gridSize)
            wrect.w = abs((nx-x))*(gridSize) + (gridSize/1.6)
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
blue = (158, 231, 245)
red = (245, 173, 148)
green = (180, 249, 165)
yellow = (255, 241, 166)
# drawing = False
# onx, ony = -1, -1
WIDTH = 800
HEIGHT = 600
gridCount = 2
gridRowCol = 5
gridSize = 50
# gridWidthStart = (WIDTH/(gridCount*2))-((gridSize*gridRowCol)/2)
gridHeightStart = (HEIGHT/2)-((gridSize*gridRowCol)/2)-10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

running = True
# genMap = True
while running:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     drawing = True
        # elif event.type == pygame.MOUSEBUTTONUP:
        #     drawing = False
        #     onx, ony = -1, -1
            
    # if drawing:
    #     mouse = pygame.mouse.get_pos()
    #     color, coor = coorColor[1], coorColor[0]
    #     for count in range(10):
    #         x, y = coor[count][0], coor[count][1]
    #         if (mouse[0] > (200 + (x*50)) and mouse[0] < (250 + (x*50)) and mouse[1] > (100 + (y*50)) and mouse[1] < (150 + (y*50))):
    #             draw_text("mouse on color", 200, 30)
    #             onx, ony, oncolor = x, y, color[count]
    #     if onx >= 0 and ony >= 0:
    #         if mouse[0] > 220 + onx*50:
    #             pygame.draw.rect(screen, oncolor, pygame.Rect(220 + onx*50, 110 + ony*50, mouse[0] - (200 + (onx*50)), 30), 0, 10)
    #         if mouse[0] < 220 + onx*50:
    #             pygame.draw.rect(screen, oncolor, pygame.Rect(220 + onx*50, 110 + ony*50, mouse[0] - (230 + (onx*50)), 30), 0, 10)
    #         if mouse[1] > 100 + ony*50:
    #             pygame.draw.rect(screen, oncolor, pygame.Rect(210 + onx*50, 120 + ony*50, 30, mouse[1] - (110 + (ony*50))), 0, 10)
    #         if mouse[1] < 100 + ony*50:
    #             pygame.draw.rect(screen, oncolor, pygame.Rect(210 + onx*50, 120 + ony*50, 30, mouse[1] - (130 + (ony*50))), 0, 10)

    draw_text(str(pygame.mouse.get_pos()), 700, 25, white)
    coorColor = [[(0,0),(4,0),(0,1),(4,1),(0,2),(4,2),(0,3),(4,3),(0,4),(4,4)],[pink, blue, blue, red, red, pink, green, green, yellow, yellow]]
    for count in range(1, gridCount*2, 2):
        draw_grid(gridRowCol, count)
        gen_map(coorColor, count)
    
    go_to(pink, [(4,2),(3,2),(3,0),(2,0),(2,2),(1,2),(1,0),(0,0)], 1)
    go_to(green, [(0,3),(4,3)], 1)
    go_to(yellow, [(4,4),(0,4)], 1)
    # if genMap:
    #     coorColor = rand_coor([0,1,2,3,4], 10)
    # genMap = False

    pygame.display.update()
    clock.tick(FPS)
