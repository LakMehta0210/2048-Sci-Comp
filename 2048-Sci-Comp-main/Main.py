import pygame
import numpy as np
import ctypes

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


WIDTH = user32.GetSystemMetrics(0)
HEIGHT = user32.GetSystemMetrics(1)
#WIDTH = 640
#HEIGHT = 640

GRAY = (60, 60, 60)

scale = 100
border = 6
x_offset = WIDTH/2 - 2*scale
y_offset = HEIGHT/2 - 2*scale

pygame.init()
game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 100)
num_font = pygame.font.Font('freesansbold.ttf', 32)


color_dict = {"None": GRAY,
				"2": (130, 140, 255),
				"4": (97, 110, 255),
				"8": (60, 76, 255),
				"16": (47, 59, 189),
				"32": (59, 111, 179),
				"64": (17, 94, 194),
				"128": (91, 157, 245),
				"256": (155, 210, 250),
				"512": (102, 191, 255),
				"1024": (59, 173, 255),
				"2048": (2, 146, 250)}


Gameboard = [[None,2,4,8],
			[16,32,64,128],
			[256,512,1024,2048],
			[None,None,None,None]]

def drawBoard(gameboard):
    game_display.fill((0,0,0))
    for y in range(len(gameboard)):
        for x in range(len(gameboard[0])):
            #if gameboard[y][x] == 0:
            pygame.draw.rect(game_display, color_dict[str(gameboard[y][x])], (x_offset + scale*x+border, y_offset + scale*y+border, scale-border, scale-border), border_radius = border)
            if str(gameboard[y][x]) != "None":
                num = num_font.render(str(gameboard[y][x]), True, (0,0,0))
                num_rect = num.get_rect(center = (x_offset + scale*x+border + (scale-border)/2, y_offset + scale*y+border + (scale-border)/2))
                game_display.blit(num, num_rect)


           
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
                sys.exit()
    drawBoard(Gameboard)
    Title = font.render("2048", True, (10, 96, 245))
    Title_rect = Title.get_rect(center = (WIDTH/2, HEIGHT/2 - 256))
    game_display.blit(Title, Title_rect)
    pygame.display.update()
    clock.tick(60)
