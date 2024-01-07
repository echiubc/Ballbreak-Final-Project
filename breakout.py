# Ethan Chiu
# Brick Breaker Game

'''
Game Demo: https://youtu.be/-K6EEuqjHN4
Documentation: see 'Game Info.docx' in the game files

About Game:

The game has sound effects

Use the left and right arrow keys to control the paddle
After each wall is broken, a new wall is introduced with stronger bricks and more columns
The ball does not reset location after a wall is broken
More points will be given for breaking each wall
This brings a little luck into the game

Every time the score is divisible by 30, the ball will be do explosive damage

Hard mode gets a 2x score multiplier
Easy mode gets a 0.5x score multiplier



'''

import pygame, time, sys, random, math
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()


# display settings
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Breakout")

# background colour
background = (0, 0, 0)

# brick colours
clrRed = (255, 51, 0)
clrYellow = (255, 255, 0)
clrBlue = (26, 140, 255)

clrRandom1 = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
clrRandom2 = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
clrRandom3 = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

listOfColours = [clrRandom1, clrRandom2, clrRandom3]

# paddle colours
paddleClr = (255, 255, 255)
paddleOutline = (100, 100, 100)

# ball colours
ballClr = (255, 255, 153)
ballOutline = (255, 255, 51)


# define game variables

columns = 4
rows = 6

gameSpeed = 90
paddleWidth = 125
strengthOfBrick = 1

wallDestroyed = 1

# main menu buttons

class menuButtons():
    def __init__(self, text, y):
        self.yPos = y
        self.text = text
        self.mouse = True
        self.clicked = False
        self.font = pygame.font.Font("DOTMATRI.ttf", 50)
        self.textRender = self.font.render(self.text, True, clrYellow)
        self.textRect = self.textRender.get_rect(center=(screenWidth/2, self.yPos))
        self.clickSound = pygame.mixer.Sound("Assets/beep.wav")

    def draw(self):
        if self.mouse == True:
            self.textRender = self.font.render(self.text, True, clrRed)
            self.textRect = self.textRender.get_rect(center=(screenWidth/2, self.yPos))
            screen.blit(self.textRender, self.textRect)
        
        else:
            self.textRender = self.font.render(self.text, True, clrYellow)
            self.textRect = self.textRender.get_rect(center=(screenWidth/2, self.yPos))
            screen.blit(self.textRender, self.textRect)

    def buttonClicked(self):

        mousePos = pygame.mouse.get_pos()
        buttonClicked = None
        if self.textRect.collidepoint(mousePos):
            self.mouse = True
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                buttonClicked = self.text
                self.clickSound.play()

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        else:
            self.mouse = False
        
        if buttonClicked == None:
            return ''
        else:
            return buttonClicked


# wall class

class wall():
    def __init__(self):
        self.width = screenWidth // columns
        self.height = 50
        self.blocks = []
    def createWall(self):
        
        blockIndividual = []
        for row in range(rows):
            blockRow = []
            # check every block in that row
            for column in range(columns):
                # generate x and y positions for each block and create a rectangle from that
                blockX = column * self.width
                blockY = row * self.height
                rect = pygame.Rect(blockX, blockY, self.width, self.height)
                # assign block strength based on row
                if row < 2:
                    strength = strengthOfBrick + 2
                elif row < 4:
                    strength = strengthOfBrick + 1
                elif row < 6:
                    strength = strengthOfBrick

                # create a list at this point to store the rect and colour data
                blockIndividual = [rect, strength]
                # append that individual block to the block row
                blockRow.append(blockIndividual)
            # append the row to the full list of blocks
            self.blocks.append(blockRow)

    def drawWall(self):
        listOfColours.append((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        for row in self.blocks:
            for block in row:
                # assign a colour based on block strength
                if block[1] > 3:
                    
                    blockClr = listOfColours[block[1]-1]
                elif block[1] == 3:
                    blockClr = listOfColours[2]
                elif block[1] == 2:
                    blockClr = listOfColours[1]
                elif block[1] == 1:
                    blockClr = listOfColours[0]
                else:
                    blockClr = (0,0,0)
                    block[0] = (0,0,0,0)
                pygame.draw.rect(screen, blockClr, block[0])
                pygame.draw.rect(screen, background, (block[0]), 2) # display some separation between bricks


class paddle():
    def __init__(self):
        # define paddle variables 
        self.height = 20
        self.width = paddleWidth
        self.x = int((screenWidth / 2) - (self.width / 2))
        self.y = screenHeight - (self.height *2)
        self.speed = 10
        self.rect = Rect(self.x,self.y,self.width,self.height)
        self.direction = 0

    def move(self):
        # move the paddle using left and right arrow keys
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screenWidth:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        # draw the paddle
        pygame.draw.rect(screen, paddleClr, self.rect)
        pygame.draw.rect(screen, paddleOutline, self.rect, 3)

# Old attempted code

# class explosionParticles():
#     def __init__(self, x, y, colour, radius):
#         '''
#         Radius is a consistent SPEED of the particle when it moves in any direction
#         '''
#         self.colour = colour
#         self.x = x
#         self.y = y
#         self.angle = random.uniform(0, math.radians(360)) # picks a random angle for particles to move in
        

#         # uses trigonometry to find X and Y speed to make the particle move at speed "radius"
#         self.speedX = radius * math.cos(self.angle)
#         self.speedY = radius * math.sin(self.angle)

#         # picks a random size for each particle
#         self.size = random.uniform(1,6)
#         self.rect = Rect(self.x, self.y, self.size, self.size)

        

#     def draw(self):
#         '''
#         The particles will bug out if self.x goes below zero
#         Stops drawing the particle if particle goes below x = 0

#         Particles move at determined X and Y speed
#         '''
#         rowCount = 0
#         if self.x > 0:
#             pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, 0)

#             self.x += self.speedX
            
#             self.y += self.speedY

#             for row in brickWall.blocks:
                
#                 itemCount = 0
#                 for item in row:
#                     # check collision
#                     if self.rect.colliderect(item[0]):
#                         # reduce the block's strength by doing damage to it
#                         if brickWall.blocks[rowCount][itemCount][1] > 1:
#                             brickWall.blocks[rowCount][itemCount][1] -= 1
#                         else: # the rectangle will still "exist", but it will have no properties once it's destroyed
#                             brickWall.blocks[rowCount][itemCount][0] = (0,0,0,0)
                            

class ball():
    def __init__(self, x, y):
        self.ballRad = 10
        self.x = x - self.ballRad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ballRad * 2, self.ballRad * 2)
        self.speedX = random.randint(-5,5)
        self.speedY = -4
        self.speedMax = 5
        self.damagePerHit = 1
        self.gameOver = 0
        self.score = 0
        self.brickBreakingSound = pygame.mixer.Sound("Assets/brickBreaking.wav")
        self.brickBounceSound = pygame.mixer.Sound("Assets/ballbounce.wav")
        self.explosionSound = pygame.mixer.Sound("Assets/explosion.wav")
        self.pointsPerWallBroken = 50
        
    def move(self):

        # collision threshold
        collisionThreshold = 5

        global wallDestroyed
        # start off with the assumption that the wall has been destroyed completely
        wallDestroyed = 1
        rowCount = 0
        # Every time the score goes up by 50, the ball will do 3 damage
        if self.score % 50 == 0:
            self.damagePerHit += 3
        else:
            self.damagePerHit = 1
        # Every time the score goes up by 75, each hit does 1 more damage
        if self.score % 75 == 0:
            self.damagePerHit += 1
        
    
        

        for row in brickWall.blocks:
            itemCount = 0
            for item in row:
                # check collision
                if self.rect.colliderect(item[0]):
                    # if ball collides with the top of a brick
                    if abs(self.rect.bottom - item[0].top) < collisionThreshold and self.speedY > 0:
                        self.speedY *= -1
                    # if ball collides with the bottom of a brick
                    if abs(self.rect.top - item[0].bottom) < collisionThreshold and self.speedY < 0:
                        self.speedY *= -1
                    # if ball collides with the left side of a brick
                    if abs(self.rect.right - item[0].left) < collisionThreshold and self.speedX > 0:
                        self.speedX *= -1
                    # if ball collides with the right side of a brick
                    if abs(self.rect.left - item[0].right) < collisionThreshold and self.speedX < 0:
                        self.speedX *= -1

                    # reduce the block's strength by doing damage to it
                    if brickWall.blocks[rowCount][itemCount][1] > 1:
                        brickWall.blocks[rowCount][itemCount][1] -= self.damagePerHit
                        self.brickBounceSound.play()
                        self.score += 1
                    else: # the rectangle will still "exist", but it will have no properties once it's destroyed
                        brickWall.blocks[rowCount][itemCount][0] = (0,0,0,0)
                        self.brickBreakingSound.play()
                        self.score += 1

                # check if block still exists, in which case the wall is not destroyed
                if brickWall.blocks[rowCount][itemCount][0] != (0,0,0,0):
                    wallDestroyed = 0
                # increase item counter 
                itemCount += 1

            # increase row counter
            rowCount += 1
        # after iterating through all the blocks, check if the wall is destroyed
        if wallDestroyed == 1:
            self.gameOver = 1
            self.score += self.pointsPerWallBroken # breaking a wall gives "pointsPerWallBroken amount of points
            self.pointsPerWallBroken += 50 # harder walls will give more points
            

        # check for collision with walls 
        if self.rect.left < 0 or self.rect.right > screenWidth:
            self.speedX *= -1
            self.brickBounceSound.play()

        # check for collision with top and bottom of the screen
        if self.rect.top < 0:
            self.speedY *= -1
            self.brickBounceSound.play()
        if self.rect.bottom > screenHeight:
            self.gameOver = -1

        # check for collision with the paddle
        if self.rect.colliderect(playerPaddle):
            # check if colliding from the top
            if abs(self.rect.bottom - playerPaddle.rect.top) < collisionThreshold and self.speedY > 0:
                self.speedY *= -1
                self.speedX += playerPaddle.direction
                self.brickBounceSound.play()
                if self.speedX > self.speedMax:
                    self.speedX = self.speedMax
                elif self.speedX < 0 and self.speedX < -self.speedMax:
                    self.speedX = -self.speedMax
            else:
                self.speedX *= -1

        self.rect.x += self.speedX
        self.rect.y += self.speedY

        return self.gameOver

    def draw(self):
        pygame.draw.circle(screen, ballClr, (self.rect.x + self.ballRad, self.rect.y + self.ballRad), self.ballRad)
        pygame.draw.circle(screen, ballOutline, (self.rect.x + self.ballRad, self.rect.y + self.ballRad), self.ballRad, 3)

    def explode(self):
        '''
        explosion powerup
        spawns a explosion of particles from where the game ball is
        '''

        # Old attempted code
        # particleList = []
        # if len(particleList) < 20:
        #     particleList.append(explosionParticles(self.rect.x + self.ballRad, self.rect.y + self.ballRad, clrRed, 5))
        # else:
        #     for particle in particleList:
        #         particle.size -= 0.2

        # for particle in range(len(particleList)):
        #     particleList[particle].draw()


        rowCount = 0
        global wallDestroyed

        self.explosionRect = Rect(self.rect.x -150 + self.ballRad, self.rect.y - 150 + self.ballRad, 300, 300)

        # check if ball hitbox collides with bricks
        for row in brickWall.blocks:
            # itemCount = 0
            for item in row:
                if self.rect.colliderect(item[0]):
                    pygame.draw.rect(screen, clrYellow, self.explosionRect)
                    rowCount = 0
                    # check if explosion hitbox collides with bricks
                    for row in brickWall.blocks:
                        itemCountExplode = 0
                        for item in row:
                                
                            if self.explosionRect.colliderect(item[0]):


                            # check collision
                            # for particle in particleList:
                            #     if particle.rect.colliderect(item[0]):
                                self.explosionSound.set_volume(0.5)
                                self.explosionSound.play()
                                    # reduce the block's strength by doing damage to it
                                if brickWall.blocks[rowCount][itemCountExplode][1] > 1:
                                    brickWall.blocks[rowCount][itemCountExplode][1] -= self.damagePerHit
                                    self.score += 1

                                            
                                else: # the rectangle will still "exist", but it will have no properties once it's destroyed
                                    brickWall.blocks[rowCount][itemCountExplode][0] = (0,0,0,0)
                                    self.score += 1

                                # check if block still exists, in which case the wall is not destroyed
                                if brickWall.blocks[rowCount][itemCountExplode][0] != (0,0,0,0):
                                    wallDestroyed = 0
                
                            itemCountExplode += 1
                        rowCount += 1

        if wallDestroyed == 1:
            self.gameOver = 1
            self.score += self.pointsPerWallBroken # breaking a wall gives "pointsPerWallBroken amount of points
            self.pointsPerWallBroken += 50 # harder walls will give more points

                    
                                    



# create a wall

brickWall = None

# requires a function to work
def createWall():
    global brickWall
    brickWall = wall()
    brickWall.createWall()

createWall()

runGame = "TitleScreen"

# Title screen
difficultyLevel = "Normal"
while runGame == "TitleScreen":

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = "QuitGame"

    # Game Title
    screen.fill(background)
    font = pygame.font.Font("DOTMATRI.ttf", 100)
    gameTitle = font.render("Breakout", True, clrBlue)
    gameTitleRect = gameTitle.get_rect(center=(screenWidth/2, screenHeight/2-200))
    screen.blit(gameTitle, gameTitleRect)

    # Game Difficulty

    difficultyButton = menuButtons("Difficulty: " + difficultyLevel, screenHeight/2 + 150)
    difficulty = difficultyButton.buttonClicked()
    difficultyButton.draw()
    
    if difficulty == "Difficulty: Normal":
        time.sleep(0.2)
        difficultyLevel = "Hard"
    elif difficulty == "Difficulty: Hard":
        time.sleep(0.2)
        difficultyLevel = "Impossible"
    elif difficulty == "Difficulty: Impossible":
        time.sleep(0.2)
        difficultyLevel = "Easy"
    elif difficulty == "Difficulty: Easy":
        time.sleep(0.2)
        difficultyLevel = "Normal"

    # Start game

    startGameButton = menuButtons("Start Game", screenHeight/2-50)
    startGame = startGameButton.buttonClicked()
    startGameButton.draw()
    if startGame == "Start Game":
        time.sleep(0.5)
        if difficultyLevel == "Normal":
            gameSpeed = 90
            paddleWidth = 125
        elif difficultyLevel == "Hard":
            gameSpeed = 120
            paddleWidth = 90
        elif difficultyLevel == "Impossible":
            gameSpeed = 150
            paddleWidth = 70
        elif difficultyLevel == "Easy":
            gameSpeed = 60
            paddleWidth = 170

        runGame = "InGame"

    # Game guide

    howToPlayGameButton = menuButtons("How to Play", screenHeight/2 +50)
    howToPlayGame = howToPlayGameButton.buttonClicked()
    howToPlayGameButton.draw()
    if howToPlayGame == "How to Play":
        runGame = "HowToPlay"

    # Quit game

    quitGameButton = menuButtons("Quit Game", screenHeight/2+250)
    quitGame = quitGameButton.buttonClicked()
    quitGameButton.draw()
    if quitGame == "Quit Game":
        runGame = "QuitGame"
        time.sleep(0.5)
        pygame.quit()
        pygame.mixer.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(gameSpeed)

# How to Play Screen

while runGame == "HowToPlay":

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = "QuitGame"

    screen.fill(background)
    font = pygame.font.Font("DOTMATRI.ttf", 20)
    Guide1 = font.render("1. Use the arrow keys to move the paddle", True, (255,255,255))
    textRect = Guide1.get_rect(center=(screenWidth/2, 30))
    screen.blit(Guide1, textRect)

    Guide2 = font.render("2. Every once in a while, the ball will get stronger", True, (255,255,255))
    textRect = Guide2.get_rect(center=(screenWidth/2, 70))
    screen.blit(Guide2, textRect)

    Guide3 = font.render("3. After a wall is broken, more walls spawn with increasing difficulty", True, (255,255,255))
    textRect = Guide3.get_rect(center=(screenWidth/2, 110))
    screen.blit(Guide3, textRect)

    Guide4 = font.render("4. Hitting the ball with a moving paddle will affect the ball's horizontal speed", True, (255,255,255))
    textRect = Guide4.get_rect(center=(screenWidth/2, 150))
    screen.blit(Guide4, textRect)

    Guide5 = font.render("5. Try and get the highest score you can", True, (255,255,255))
    textRect = Guide5.get_rect(center=(screenWidth/2, 190))
    screen.blit(Guide5, textRect)

    Guide6 = font.render("6. Difficulty changes the speed of the ball and the paddle size", True, (255,255,255))
    textRect = Guide6.get_rect(center=(screenWidth/2, 230))
    screen.blit(Guide6, textRect)

    Guide7 = font.render("7. Hard mode has twice the score of Normal, and Easy has half", True, (255,255,255))
    textRect = Guide7.get_rect(center=(screenWidth/2, 270))
    screen.blit(Guide7, textRect)

    Guide8 = font.render("8. More columns spawn in as each wall is broken", True, (255,255,255))
    textRect = Guide8.get_rect(center=(screenWidth/2, 310))
    screen.blit(Guide8, textRect)


    startGameButton = menuButtons("Start Game", screenHeight/2+150)
    startGame = startGameButton.buttonClicked()
    startGameButton.draw()
    if startGame == "Start Game":
        time.sleep(0.5)
        if difficultyLevel == "Normal":
            gameSpeed = 90
            paddleWidth = 125
        elif difficultyLevel == "Hard":
            gameSpeed = 120
            paddleWidth = 90
        elif difficultyLevel == "Impossible":
            gameSpeed = 150
            paddleWidth = 70
        elif difficultyLevel == "Easy":
            gameSpeed = 60
            paddleWidth = 170

        runGame = "InGame"

    pygame.display.update()
    clock.tick(gameSpeed)

# Game 

# create a paddle
playerPaddle = paddle()

# create a ball
gameBall = None
def createBall():
    gameBall = ball(playerPaddle.x + (125 //2), playerPaddle.y - playerPaddle.height)
    return gameBall

gameBall = createBall()

while runGame == "InGame":

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = "QuitGame"


    screen.fill(background)

    # draw wall
    brickWall.drawWall()
    font = pygame.font.Font("DOTMATRI.ttf", 20)
    displayScore = font.render("Score: " + str(gameBall.score), True, clrYellow)
    textRect = displayScore.get_rect(center=(screenWidth/2, screenHeight/2 + 100))
    screen.blit(displayScore, textRect)

    # draw paddle
    playerPaddle.draw()
    playerPaddle.move()

    # draw ball
    gameBall.draw()
    gameBall.move()
    if gameBall.score % 30 == 0 and gameBall.score != 0:
        gameBall.explode()

    # Victory/Lose screen
    font = pygame.font.Font("DOTMATRI.ttf", 75)
    
    
    if gameBall.gameOver == 1:
        gameBall.gameOver = 0
        strengthOfBrick += 1
        columns += 1
        createWall()

        
        levelUpSound = pygame.mixer.Sound("Assets/levelUp.wav")
        levelUpSound.play()
   
    elif gameBall.gameOver == -1:
        
        
        screen.fill(background)
        font = pygame.font.Font("DOTMATRI.ttf", 75)
        # Game over text
        textLose = font.render("GAME OVER!!", True, clrRed)
        textRect = textLose.get_rect(center=(screenWidth/2, screenHeight/2))
        screen.blit(textLose, textRect)

        # Displays score
        if difficultyLevel == "Easy":
            gameBall.score = gameBall.score // 2 # Easy gets 0.5x score multiplier
        elif difficultyLevel == "Hard":
            gameBall.score = gameBall.score * 2 # Hard gets 2x score multiplier
        elif difficultyLevel == "Impossible":
            gameBall.score = gameBall.score * 4 # Impossible gets 4x score multiplier
        textDisplayScore = font.render("Score: " + str(gameBall.score), True, clrBlue)
        textRect = textDisplayScore.get_rect(center=(screenWidth/2, screenHeight/2 + 100))
        screen.blit(textDisplayScore, textRect)
        
        youLoseSound = pygame.mixer.Sound("Assets/youLose.wav")
        youLoseSound.play()
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        pygame.mixer.quit()
        sys.exit()
    pygame.display.update()
    clock.tick(gameSpeed)

pygame.quit()
pygame.mixer.quit()
