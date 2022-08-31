import pygame
import numpy as np
import ctypes
import random
import time

#user32 = ctypes.windll.user32
#screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

WIDTH = 1080
HEIGHT = 720
#WIDTH = user32.GetSystemMetrics(0)
#HEIGHT = user32.GetSystemMetrics(1)


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
    Title = font.render("2048", True, (10, 96, 245))
    Title_rect = Title.get_rect(center = (WIDTH/2, HEIGHT/2 - 256))
    game_display.blit(Title, Title_rect)

def gameEnd():
    endScreen = True
    while endScreen:
        instructions = num_font.render("Press SPACE to restart", True, (255,255,0))
        instructions_rect = instructions.get_rect(center = (WIDTH/2, HEIGHT/2 + 100))
        game_display.blit(instructions, instructions_rect)

        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.set_alpha(15)
        pygame.draw.rect(surface, (0,0,0), (0,0,WIDTH, HEIGHT))
        game_display.blit(surface, (0,0))

        game_over = font.render("GAME OVER", True, ((255, 0, 0)))
        game_over_rect = game_over.get_rect(center = (WIDTH/2, HEIGHT/2))
        game_display.blit(game_over, game_over_rect)

        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                endScreen = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                endScreen = False
                pygame.quit()
                sys.exit()
                break
            if event.type == pygame.QUIT:
                endScreen = False
                pygame.quit()
                sys.exit()
                break

def gameWin():
    endScreen = True
    
    while endScreen:
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.set_alpha(15)
        pygame.draw.rect(surface, (0,0,0), (0,0,WIDTH, HEIGHT))
        game_display.blit(surface, (0,0))
        
        game_over = font.render("GAME WON!!", True, (2, 146, 250))
        game_over_rect = game_over.get_rect(center = (WIDTH/2, HEIGHT/2))
        game_display.blit(game_over, game_over_rect)

        instructions = num_font.render("Press SPACE to restart", True, (255,255,0))
        instructions_rect = instructions.get_rect(center = (WIDTH/2, HEIGHT/2 + 100))
        game_display.blit(instructions, instructions_rect)

        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                endScreen = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                endScreen = False
                pygame.quit()
                break
            if event.type == pygame.QUIT:
                endScreen = False
                pygame.quit()
                break

def spawnTile(gameboard):
    tileSpawned = False
    while not tileSpawned:
        rand_x = np.random.randint(0,4)
        rand_y = np.random.randint(0,4)
        if gameboard[rand_y][rand_x] == None:
            tile_chance  = random.random()
            if tile_chance < .1:
                cell_state = 4
            else: cell_state = 2
            tileSpawned = True
            return cell_state, rand_y, rand_x


def boardcheck(old_state, current_state):
    same_board = True
    for y in range(len(current_state)):
        for x in range(len(current_state[0])):
            if old_state[y][x] != current_state[y][x]:
                same_board = False
    return same_board

def boardFull(gameboard):
    fullBoard = True
    for y in range(len(gameboard)):
        if gameboard[y].count(None) != 0:
            fullBoard = False
    return fullBoard

def slideRight(gameboard):
    for row in gameboard:
        for i in range(len(row)-1,-1,-1):
            if row[i] == None:
                for x in range(i, -1, -1):
                    if row[x] != None:
                        row[i] = row[x]
                        row[x] = None
                        break
    return gameboard

def slideLeft(gameboard):
    for row in gameboard:
        for i in range(len(row)):
            if row[i] == None:
                for x in range(i,len(row)):
                    if row[x] != None:
                        row[i] = row[x]
                        row[x] = None
                        break
    return gameboard

def slideUp(gameboard):
    for col_ind in range(len(gameboard[0])):
        column = [gameboard[k][col_ind] for k in range(len(gameboard))]
        for i in range(len(column)):
                if column[i] == None:
                    for x in range(i,len(column)):
                        if column[x] != None:
                            column[i] = column[x]
                            column[x] = None
                            break
        for index in range(len(column)):
            gameboard[index][col_ind] = column[index]
    return gameboard

def slideDown(gameboard):
    for col_ind in range(len(gameboard[0])):
        column = [gameboard[k][col_ind] for k in range(len(gameboard))]
        for i in range(len(column)-1, -1, -1):
                if column[i] == None:
                    for x in range(i,-1, -1):
                        if column[x] != None:
                            column[i] = column[x]
                            column[x] = None
                            break
        for index in range(len(column)):
            gameboard[index][col_ind] = column[index]
    return gameboard

def combineLeft(gameboard):
    for row in gameboard:
        for i in range(len(row)-1):
            if row[i] == row[i+1] and row[i] != None:
                row[i] = row[i] + row[i+1]
                row[i+1] = None
    return gameboard

def combineRight(gameboard):
    for row in gameboard:
        for i in range(len(row)-1, 0, -1):
            if row[i] == row[i-1] and row[i] != None:
                row[i] = row[i] + row[i-1]
                row[i-1] = None
    return gameboard

def combineUp(gameboard):
    for col_ind in range(len(gameboard[0])):
        column = [gameboard[k][col_ind] for k in range(len(gameboard))]
        for i in range(len(column)-1):
            if column[i] == column[i+1] and column[i] != None:
                column[i] = column[i] + column[i+1]
                column[i+1] = None
        for index in range(len(column)):
            gameboard[index][col_ind] = column[index]
    return gameboard

def combineDown(gameboard):
    for col_ind in range(len(gameboard[0])):
        column = [gameboard[k][col_ind] for k in range(len(gameboard))]
        for i in range(len(column)-1, 0, -1):
            if column[i] == column[i-1] and column[i] != None:
                column[i] = column[i] + column[i-1]
                column[i-1] = None
        for index in range(len(column)):
            gameboard[index][col_ind] = column[index]
    return gameboard


def checkCombines(gameboard):
    phantom_board = [[gameboard[y][x] for x in range(len(gameboard[0]))] for y in range(len(gameboard))]
    combines = False
    if not boardcheck(gameboard, combineUp(phantom_board)):
        combines = True
    elif not boardcheck(gameboard, combineDown(phantom_board)):
        combines = True
    elif not boardcheck(gameboard, combineLeft(phantom_board)):
        combines = True
    elif not boardcheck(gameboard, combineRight(phantom_board)):
        combines = True
    return combines


while True:
    Gameboard = [[None,None,None,None],
                [None,None,None,None],
                [None,None,None,None],
                [None,None,None,None]]
    spawn_cell_state, spawn_y, spawn_x = spawnTile(Gameboard)
    Gameboard[spawn_y][spawn_x] = spawn_cell_state
    spawn_cell_state, spawn_y, spawn_x = spawnTile(Gameboard)
    Gameboard[spawn_y][spawn_x] = spawn_cell_state

    old_state =  [[Gameboard[y][x] for x in range(len(Gameboard[0]))] for y in range(len(Gameboard))]

    reset = False
    tile_spawned = False
    while not reset:
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
                if event.key == ord('r'):
                    reset = True
                        
                if (event.key == ord('d')) or (event.key == pygame.K_RIGHT):
                    Gameboard = slideRight(Gameboard)
                    Gameboard = combineRight(Gameboard)
                    Gameboard = slideRight(Gameboard)

                    if not boardFull(Gameboard):
                        if not boardcheck(old_state, Gameboard):
                            spawn_cell_state, spawn_y, spawn_x = spawnTile(Gameboard)
                            Gameboard[spawn_y][spawn_x] = spawn_cell_state
                            tile_spawned = True
                    else:
                        if not checkCombines(Gameboard):
                            gameEnd()
                            reset = True

                if (event.key == ord('a')) or (event.key == pygame.K_LEFT):
                    Gameboard = slideLeft(Gameboard)
                    Gameboard = combineLeft(Gameboard)
                    Gameboard = slideLeft(Gameboard)

                    if not boardFull(Gameboard):
                        if not boardcheck(old_state, Gameboard):
                            spawn_cell_state, spawn_y, spawn_x = spawnTile(Gameboard)
                            Gameboard[spawn_y][spawn_x] = spawn_cell_state
                            tile_spawned = True
                    else:
                        if not checkCombines(Gameboard):
                            gameEnd()
                            reset = True


                if (event.key == ord('w')) or (event.key == pygame.K_UP):
                    Gameboard = slideUp(Gameboard)
                    Gameboard = combineUp(Gameboard)
                    Gameboard = slideUp(Gameboard)

                    if not boardFull(Gameboard):
                        if not boardcheck(old_state, Gameboard):
                            spawn_cell_state, spawn_y, spawn_x = spawnTile(Gameboard)
                            Gameboard[spawn_y][spawn_x] = spawn_cell_state
                            tile_spawned = True
                    else:
                        if not checkCombines(Gameboard):
                            gameEnd()
                            reset = True


                if (event.key == ord('s')) or (event.key == pygame.K_DOWN):
                    Gameboard = slideDown(Gameboard)
                    Gameboard = combineDown(Gameboard)
                    Gameboard = slideDown(Gameboard)

                    if not boardFull(Gameboard):
                        if not boardcheck(old_state, Gameboard):
                            spawn_cell_state, spawn_y, spawn_x = spawnTile(Gameboard)
                            Gameboard[spawn_y][spawn_x] = spawn_cell_state
                            tile_spawned = True
                    else:
                        if not checkCombines(Gameboard):
                            gameEnd()
                            reset = True



        old_state =  [[Gameboard[y][x] for x in range(len(Gameboard[0]))] for y in range(len(Gameboard))]
        

        drawBoard(Gameboard)
        pygame.display.update()

        for y in range(len(Gameboard)):
            for x in range(len(Gameboard[0])):
                if Gameboard[y][x] == 2048:
                    gameWin()
                    reset = True

        drawBoard(Gameboard)
        pygame.display.update()
        
        if reset:
            break
        tile_spawned = False

        clock.tick(60)

