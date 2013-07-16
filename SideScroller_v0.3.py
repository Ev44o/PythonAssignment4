"""
Python Assignment 4 - Side Scroller

Author: Evan Pugh
Last modified by: Evan Pugh

Source File Name: SideScroller_0.3.py
Date last modified: July 15, 2013

Program Description: This program is a game where you control
        a frog using your mouse. The frog can move up and down.
        You progress from left to right by catching flies.
        When you hit a rock, that lowers your health. If you 
        reach 0 health. The game ends. The goal is to lose the
        least amount of heath and have the lowest score.
        Think of this game as if it were a golf game. :)

Version: 0.3
In this version: - implemented random rock images
                 - random rock start positions (off screen)
                 - changed hp loss to -10 from -5
                 - added random flies going random directions
                 - added enemy snake that follows you
                 - frog goes back if a rock is hit
                 - frog moves ahead if a fly is caught
"""
    
import pygame, random
from test.sortperf import randfloats
pygame.init()

screen = pygame.display.set_mode((600, 600))

class Frog(pygame.sprite.Sprite):
    # this class contains the information for the frog sprite
    def __init__(self):
        
        if not pygame.mixer:
            print("Sound error")
        else:
            pygame.mixer.init()
            self.sndBkgd = pygame.mixer.Sound("FrogsStart.wav")
            self.sndBkgd.play(-1)
        
        self.createFrog()
        
    def createFrog(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("frog1.gif") # load the frog picture
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        self.xPosition = 150
        
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        # set frog image position relative to the y axis position
        # of the mouse
        
        self.rect.center = (self.xPosition, mousey)

       
class Snake(pygame.sprite.Sprite):
    # this class contains the information for the Snake sprite
    def __init__(self):
        
        self.createSnake()
        
    def createSnake(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("snake1.gif") # load the Snake picture
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        # set Snake image position relative to the y axis position
        # of the mouse
        self.rect.center = (0, mousey)
        
                
class Fly(pygame.sprite.Sprite):
    # this class creates random fly sprites
    def __init__(self):
        # call the random fly method
        self.randFly()
        
        self.reset()
        # fly can be going at a range of speeds
        
    
    def randFly(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.randArrayNum = random.randrange(0,1)
        self.randImage = ["fly1.gif","fly2.gif"]
        # use the random number to assign the string from the randImage array
        self.randFlyImage = self.randImage[self.randArrayNum]
        
        self.image = pygame.image.load(self.randFlyImage)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        self.dy = random.randrange(-8, 8)
        self.dx = random.randrange(8, 14)
    
    def update(self):
        self.rect.centery -= self.dy
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
            
    def reset(self):
        self.randFly()
        self.rect.left = 600
        self.rect.centery = random.randrange(0, screen.get_width())
        
      
class Rock(pygame.sprite.Sprite):
    # this class creates random rock sprites
    def __init__(self):
        # pick a random rock image
        self.randRock()
        
        self.reset()
        # rock will look stationary on the ground as you go by
        # this value should be the same as the ground speed
        self.dx = 6
    
    def randRock(self):
        
        pygame.sprite.Sprite.__init__(self)
        # use a random number picker to choose one of the rock images
        self.randArrayNum = random.randrange(0,3)
        self.randImage = ["rock1.gif","rock2.gif","rock3.gif","rock4.gif"]
        # use the random number to assign the string from the randImage array
        self.randRockImage = self.randImage[self.randArrayNum]
        # insert the string to load
        self.image = pygame.image.load(self.randRockImage)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
    
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
    
    def reset(self):
        self.randRock() # choose a new random rock
        # move it off screen at a random start location for better realism
        self.rect.left = random.randrange(600, 800)
        self.rect.centery = random.randrange(0, screen.get_width()) # pick a random location
        
class Grass(pygame.sprite.Sprite):
    # this class creates the background image
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("grass1.gif")
        self.rect = self.image.get_rect()
        self.dx = 6
        self.reset()
        
    def update(self):
        self.rect.right -= self.dx
        if self.rect.left <= -1200:
            self.reset() 
    
    def reset(self):
        self.rect.left = 0

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        # this class controls the score and health
        pygame.sprite.Sprite.__init__(self)
        # start with 100% health
        self.health = 100
        self.score = 0
        self.font = pygame.font.SysFont("None", 35)
        
    def update(self):
        self.text = "Health: %d, Score: %d" % (self.health, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
    
def game():
    # this method brings all the classes together and builds the game
    pygame.display.set_caption("Frog Escape!")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    frog = Frog()
    #create a snake instance
    snake = Snake()
    # create 2 fly instance
    fly1 = Fly()
    fly2 = Fly()
    # create 6 rock instance
    rock1 = Rock()
    rock2 = Rock()
    rock3 = Rock()
    rock4 = Rock()
    rock5 = Rock()
    rock6 = Rock()
    # create the background instance
    grass = Grass()
    # start the scoreboard instance
    scoreboard = Scoreboard()
    
    #group all the sprites according to their use
    snakeSprite = pygame.sprite.Group(snake)
    safeSprites = pygame.sprite.OrderedUpdates(grass, frog)
    
    flySprites = pygame.sprite.Group(fly1, fly2)
    rockSprites = pygame.sprite.Group(rock1, rock2, rock3, rock4, rock5, rock6)
    scoreSprite = pygame.sprite.Group(scoreboard)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30) # the num of updates (frame rate) per second
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
        
        hitFlies = pygame.sprite.spritecollide(frog, flySprites, False)
        if hitFlies:
            # gain points for every fly you eat
            scoreboard.score += 10
            # move ahead for every fly eaten
            frog.xPosition += 25
            if frog.rect.right >= screen.get_width():
                keepGoing = False
            for theFly in hitFlies:
                theFly.reset()

        hitRocks = pygame.sprite.spritecollide(frog, rockSprites, False)
        if hitRocks:
            # lose health every time you hit a bad object (rock)
            scoreboard.health -= 10
            #fall back ever rock hit
            frog.xPosition -= 5
            if scoreboard.health <= 0:
                keepGoing = False
            for theRock in hitRocks:
                theRock.reset()
        
        # call the update of every class
        snakeSprite.update()
        safeSprites.update()
        flySprites.update()
        rockSprites.update()
        scoreSprite.update()
        
        # draw all the sprites on screen
        
        safeSprites.draw(screen)
        rockSprites.draw(screen)
        snakeSprite.draw(screen)
        flySprites.draw(screen)
        
        
        scoreSprite.draw(screen)
        
        pygame.display.flip()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
    return scoreboard.score


    
def instructions(score):
    pygame.display.set_caption("Frog escape!")

    # show the frog and the background while the user reads the
    # instructions etc
    frog = Frog()
    grass = Grass()
    
    allSprites = pygame.sprite.Group(grass, frog)
    insFont = pygame.font.SysFont(None, 35)
    insLabels = []
    instructions = (
    "Frog escape.    Last score: %d" % score ,
    "",
    "Description: You are trying to get away",
    "from a hungry snake. You are a frog who",
    "seems to have all the bad luck. Not long",
    "ago you stumbled upon a hole in the ",
    "ground and it happened to be the home of",
    "a very hungry snake. Now you must get",
    "away as quickly as possible.",
    "",
    "Instructions: Use the mouse to control ",
    "the frog. Avoid things that will slow ",
    "you down and hurt you, and eat bugs to",
    "get a boost away from the snake. The ",
    "goal is to have a low score and high",
    "health when you reach the other side.",
    "",
    "ClickPress ESC to quit."
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 0))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # if the user presses the ESC key quit
                    keepGoing = False
                    donePlaying = True
        # update the sprites
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
         
    pygame.mouse.set_visible(True)
    return donePlaying
        
def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = instructions(score)
        if not donePlaying:
            score = game()


if __name__ == "__main__":
    main()
    
    
