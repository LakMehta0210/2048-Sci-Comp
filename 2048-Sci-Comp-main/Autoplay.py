import pygame
import numpy as np
import ctypes
import random
import time
import sys

#user32 = ctypes.windll.user32
#screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

WIDTH = 1080
HEIGHT = 720
#WIDTH = user32.GetSystemMetrics(0)
#HEIGHT = user32.GetSystemMetrics(1)
#This code sets the Width and Height of our screen

GRAY = (60, 60, 60)
#Defines a color we use

#some display constants, including the size of a tile, the space between, and offsets to center the board
scale = 100
border = 6
x_offset = WIDTH/2 - 2*scale
y_offset = HEIGHT/2 - 2*scale

#basic pygame setup, including creating a screen, labeling the window, 
pygame.init()
game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()
#fonts
font = pygame.font.Font('freesansbold.ttf', 100)
num_font = pygame.font.Font('freesansbold.ttf', 32)
#This code designs the title 2048 above our game board.


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
				"2048": (2, 146, 250),
                "Over": (0, 255, 183)}
#This color dictionary allows you to pull colors for each of the twelve tile values from 2 to 2048. This makes the code more efficient later on. Since we coded our game to go over 2048, the "Over" allows us to have colors for higher value tiles.


def drawBoard(gameboard, score):
    #Makes the screen black
    game_display.fill((0,0,0))

    for y in range(len(gameboard)):
        for x in range(len(gameboard[0])):

            #sets color values based on the number in the tile
            if gameboard[y][x] == None:
                color = color_dict[str(gameboard[y][x])]
            elif gameboard[y][x] <= 2048: color = color_dict[str(gameboard[y][x])]
            else: color = color_dict["Over"]

            #draws tiles
            pygame.draw.rect(game_display, color, (x_offset + scale*x+border, y_offset + scale*y+border, scale-border, scale-border), border_radius = border)
            
            #draws numbers in the tiles
            if str(gameboard[y][x]) != "None":
                num = num_font.render(str(gameboard[y][x]), True, (0,0,0))
                num_rect = num.get_rect(center = (x_offset + scale*x+border + (scale-border)/2, y_offset + scale*y+border + (scale-border)/2))
                game_display.blit(num, num_rect)
    #draws title
    Title = font.render("2048", True, (10, 96, 245))
    Title_rect = Title.get_rect(center = (WIDTH/2, HEIGHT/2 - 256))
    game_display.blit(Title, Title_rect)

    Score = num_font.render(f'Score: {score}', True, (10, 96, 245))
    Score_rect = Score.get_rect(topright = (WIDTH/2 + 2*scale, HEIGHT/2 + 2*scale + 16))
    #game_display.blit(Score, (WIDTH/2 + 2*scale - 132, HEIGHT/2 + 2*scale + 16))
    game_display.blit(Score, Score_rect)

    Reset_R = num_font.render("Press R to Restart", True, (255, 255, 255))
    Reset_R_rect = Reset_R.get_rect(topright = (WIDTH/2 + 2*scale, HEIGHT/2 + 2*scale + 64))
    game_display.blit(Reset_R, Reset_R_rect)


def gameEnd(score):
    #creates a secondary gameloop holding the player until the player presses space
    endScreen = True
    while endScreen:
        #writes instructions
        instructions = num_font.render("Press SPACE to restart", True, (255,255,0))
        instructions_rect = instructions.get_rect(center = (WIDTH/2, HEIGHT/2 + 100))
        game_display.blit(instructions, instructions_rect)

        #creates translucent surface to create a dimming effect and the fade to black
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.set_alpha(15)
        pygame.draw.rect(surface, (0,0,0), (0,0,WIDTH, HEIGHT))
        game_display.blit(surface, (0,0))

        #writes GAME OVER
        game_over = font.render("GAME OVER", True, ((255, 0, 0)))
        game_over_rect = game_over.get_rect(center = (WIDTH/2, HEIGHT/2))
        game_display.blit(game_over, game_over_rect)

        Score = num_font.render(f"Score: {score}", True, (3, 252, 198))
        Score_rect = Score.get_rect(center = (WIDTH/2, HEIGHT/2 + 160))
        game_display.blit(Score, Score_rect)

        pygame.display.flip()
        clock.tick(60)

        #takes in user input: SPACE to restart, and ESC to exit.
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

#Structurally similar to GameEnd, but added the variables of continuing and reset, writing different instructions as well.
def gameWin(score):
    endScreen = True

    #defaults for the continuing and reset variables which help decide whether or not to continue playing
    continuing = False
    reset = True

    #creates translucent surface to create a dimming effect and the fade to black
    while endScreen:
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.set_alpha(15)
        pygame.draw.rect(surface, (0,0,0), (0,0,WIDTH, HEIGHT))
        game_display.blit(surface, (0,0))
        
        #Writes Game Won
        game_over = font.render("GAME WON!!", True, (2, 146, 250))
        game_over_rect = game_over.get_rect(center = (WIDTH/2, HEIGHT/2))
        game_display.blit(game_over, game_over_rect)

        #Writes Instructions
        instructions = num_font.render("Press SPACE to restart", True, (255,255,0))
        instructions_rect = instructions.get_rect(center = (WIDTH/2, HEIGHT/2 + 100))
        game_display.blit(instructions, instructions_rect)

        instructions = num_font.render("Press ENTER to keep playing", True, (255,255,0))
        instructions_rect = instructions.get_rect(center = (WIDTH/2, HEIGHT/2 + 150))
        game_display.blit(instructions, instructions_rect)

        Score = num_font.render(f"Score: {score}", True, (3, 252, 198))
        Score_rect = Score.get_rect(center = (WIDTH/2, HEIGHT/2 + 200))
        game_display.blit(Score, Score_rect)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                endScreen = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                endScreen = False
                #changes continuing and reset values if player decides to continue
                continuing = True
                reset = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                endScreen = False
                pygame.quit()
                break
            if event.type == pygame.QUIT:
                endScreen = False
                pygame.quit()
                break
    return reset, continuing

#This code allows tiles to spawn into the gameboard. It gives the chance of a 2 or a 4 spawning.
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

#We used this code to constantly update the gameboard. This function works with old_state and current_state to do so.
#Used to make sure that the board changes after a player input
def boardcheck(old_state, current_state):
    same_board = True
    for y in range(len(current_state)):
        for x in range(len(current_state[0])):
            if old_state[y][x] != current_state[y][x]:
                same_board = False
    return same_board

#This code checks if the board is full. It is part of the process of checking if there are no more moves available. Also makes sure that our tile spawning algorithm does not get stuck.
def boardFull(gameboard):
    fullBoard = True
    for y in range(len(gameboard)):
        if gameboard[y].count(None) != 0:
            fullBoard = False
    return fullBoard


#These slide fucntions shift the tiles in a direction based on player input. 
#Done by pulling a row from the gameboard and starting from the right, finding an empty spot, and then finding the closest non-empty tile to the right and swapping the two
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

#same as the slideRight, but just starts from the left
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

#same as slideRight, just creating a list to store the values in a single column to keep the same algorithm
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
        #maps changes in the column list back to the gameboard
        for index in range(len(column)):
            gameboard[index][col_ind] = column[index]
    return gameboard

#same as slideUp just starting from the bottom
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

#sees if two numbers beside each other are the same, adding the two and then making one empty
def combineLeft(gameboard, score):
    for row in gameboard:
        for i in range(len(row)-1):
            if row[i] == row[i+1] and row[i] != None:
                row[i] = row[i] + row[i+1]
                score += row[i]
                row[i+1] = None
    return gameboard, score

#same as combineLeft just starting from the other side and comparing a tile with the tile to the left instead of right
def combineRight(gameboard, score):
    for row in gameboard:
        for i in range(len(row)-1, 0, -1):
            if row[i] == row[i-1] and row[i] != None:
                row[i] = row[i] + row[i-1]
                score += row[i]
                row[i-1] = None
    return gameboard, score

#same column list creation in slideUp and same algorirthm as other combines
def combineUp(gameboard, score):
    for col_ind in range(len(gameboard[0])):
        column = [gameboard[k][col_ind] for k in range(len(gameboard))]
        for i in range(len(column)-1):
            if column[i] == column[i+1] and column[i] != None:
                column[i] = column[i] + column[i+1]
                score += column[i]
                column[i+1] = None
        for index in range(len(column)):
            gameboard[index][col_ind] = column[index]
    return gameboard, score

#same column list creation in slideUp and same algorirthm as other combines
def combineDown(gameboard, score):
    for col_ind in range(len(gameboard[0])):
        column = [gameboard[k][col_ind] for k in range(len(gameboard))]
        for i in range(len(column)-1, 0, -1):
            if column[i] == column[i-1] and column[i] != None:
                column[i] = column[i] + column[i-1]
                score += column[i]
                column[i-1] = None
        for index in range(len(column)):
            gameboard[index][col_ind] = column[index]
    return gameboard, score

#checks to see if there are possible combines for when the board is full to make sure their aren't false losses
def checkCombines(gameboard):
    phantom_board = [[gameboard[y][x] for x in range(len(gameboard[0]))] for y in range(len(gameboard))]
    combines = False
    #boardcheck used to see if combines had any effect
    up_state, _ = combineUp(phantom_board, 0)
    left_state, _ = combineLeft(phantom_board, 0)
    if not boardcheck(gameboard, up_state):
        combines = True
    elif not boardcheck(gameboard, left_state):
        combines = True
    return combines

while True:
    #creates empty Gameboard
    Gameboard = [[None,None,None,None],
                [None,None,None,None],
                [None,None,None,None],
                [None,None,None,None]]
    
    #spawns two cells in a random spot
    spawn_cell_state, spawn_y, spawn_x = spawnTile(Gameboard)
    Gameboard[spawn_y][spawn_x] = spawn_cell_state
    spawn_cell_state, spawn_y, spawn_x = spawnTile(Gameboard)
    Gameboard[spawn_y][spawn_x] = spawn_cell_state

    #creates an old state to use in the boardcheck function
    old_state =  [[Gameboard[y][x] for x in range(len(Gameboard[0]))] for y in range(len(Gameboard))]

    #initialization of variables in for loop
    reset = False
    continuing = False

    score = 0
    step = 0

    while not reset:
        if not step % 15:
            move = np.random.randint(0,4)
            if move == 0:    
                #algorithm to create desired tiles
                Gameboard = slideRight(Gameboard)
                Gameboard, score = combineRight(Gameboard, score)
                Gameboard = slideRight(Gameboard)

                #checks if board is full to spawn tiles or not
                if not boardFull(Gameboard):
                    #only spawns a tile if board has changed from the user input
                    if not boardcheck(old_state, Gameboard):
                        spawn_cell_state, spawn_y, spawn_x = spawnTile(Gameboard)
                        Gameboard[spawn_y][spawn_x] = spawn_cell_state
                else:
                    #checks if there are any valid moves left
                    if not checkCombines(Gameboard):
                        #ends game if no possible moves
                        gameEnd(score)
                        reset = True

            #other directions are the same code, just changing which slide and combine algorithms used
            if move == 1:
                Gameboard = slideLeft(Gameboard)
                Gameboard, score = combineLeft(Gameboard, score)
                Gameboard = slideLeft(Gameboard)

                if not boardFull(Gameboard):
                    if not boardcheck(old_state, Gameboard):
                        spawn_cell_state, spawn_y, spawn_x = spawnTile(Gameboard)
                        Gameboard[spawn_y][spawn_x] = spawn_cell_state
                else:
                    if not checkCombines(Gameboard):
                        gameEnd(score)
                        reset = True


            if move == 2:
                Gameboard = slideUp(Gameboard)
                Gameboard, score = combineUp(Gameboard, score)
                Gameboard = slideUp(Gameboard)

                if not boardFull(Gameboard):
                    if not boardcheck(old_state, Gameboard):

                        spawn_cell_state, spawn_y, spawn_x = spawnTile(Gameboard)
                        Gameboard[spawn_y][spawn_x] = spawn_cell_state
                else:
                    if not checkCombines(Gameboard):
                        gameEnd(score)
                        reset = True


            if move == 3:
                Gameboard = slideDown(Gameboard)
                Gameboard, score = combineDown(Gameboard, score)
                Gameboard = slideDown(Gameboard)

                if not boardFull(Gameboard):
                    if not boardcheck(old_state, Gameboard):

                        spawn_cell_state, spawn_y, spawn_x = spawnTile(Gameboard)
                        Gameboard[spawn_y][spawn_x] = spawn_cell_state
                else:
                    if not checkCombines(Gameboard):
                        gameEnd(score)
                        reset = True


        #updates old_state for comparison with the next board
        old_state =  [[Gameboard[y][x] for x in range(len(Gameboard[0]))] for y in range(len(Gameboard))]
        
        #draws board
        drawBoard(Gameboard, score)
        pygame.display.update()

        #checks to see if game is won
        for y in range(len(Gameboard)):
            for x in range(len(Gameboard[0])):
                if Gameboard[y][x] == 2048 and continuing == False:
                    #only runs this code if player hasn't already agreed to continue
                    reset, continuing = gameWin(score)

        #updates board after win so the 2048 square shows
        #drawBoard(Gameboard)
        #pygame.display.update()

        step += 1
        #sets FPS to 60
        clock.tick(60)

