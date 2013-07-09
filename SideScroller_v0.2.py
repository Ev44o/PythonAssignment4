"""
Python Assignment 4 - Side Scroller
Author: Evan Pugh
Date: July 3, 2013

Version: 0.2
In this version: - Added 100 health to frog and increment of -5hp per hit object 
                 - added rocks as bad objects that take away health
                 - increased speed 
                 - updated description and instructions
                 - changed all font size to 35
                 - added a few more comments
"""
    
import pygame, random
pygame.init()

screen = pygame.display.set_mode((600, 600))

class Frog(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("frog1.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
    '''    if not pygame.mixer:
            print("Sound error")
        else:
            pygame.mixer.init()
            self.sndGulp = pygame.mixer.Sound("gulp.ogg")
            self.sndCollide = pygame.mixer.Sound("collide.ogg")
            self.sndEngine.play(-1)'''
        
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        # set frog image position relative to the y axis position
        # of the mouse
        self.rect.center = (100, mousey)
                
class Fly(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("fly1.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dx = 8
    
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.right > screen.get_height():
            self.reset()
            
    def reset(self):
        self.rect.left = 600
        self.rect.centery = random.randrange(0, screen.get_width())
      
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("rock1.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        # rock will look stationary on the ground as you go by
        # this value should be the same as the ground speed
        self.dx = 6
        
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.top > screen.get_height():
            self.reset()
    
    def reset(self):
        self.rect.left = 600
        self.rect.centery = random.randrange(0, screen.get_width())
        
    
class Grass(pygame.sprite.Sprite):
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
    pygame.display.set_caption("Frog Escape!")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    frog = Frog()
    fly1 = Fly()
    rock1 = Rock()
    grass = Grass()
    scoreboard = Scoreboard()

    safeSprites = pygame.sprite.OrderedUpdates(grass, frog)
    flySprites = pygame.sprite.Group(fly1)
    rockSprites = pygame.sprite.Group(rock1)
    scoreSprite = pygame.sprite.Group(scoreboard)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        # give 100 score
        if frog.rect.colliderect(fly1.rect):
            '''frog.sndGulp.play()   make a gulp sound'''
            fly1.reset()
            scoreboard.score += 10

        hitRocks = pygame.sprite.spritecollide(frog, rockSprites, False)
        if hitRocks:
            #frog.sndCollide.play()
            # lose health every time you hit a bad object (rock)
            scoreboard.health -= 5
            if scoreboard.health <= 0:
                keepGoing = False
            for theRock in hitRocks:
                theRock.reset()
        
        safeSprites.update()
        flySprites.update()
        rockSprites.update()
        scoreSprite.update()
        
        safeSprites.draw(screen)
        flySprites.draw(screen)
        rockSprites.draw(screen)
        scoreSprite.draw(screen)
        
        pygame.display.flip()
    
    #return mouse cursor
    pygame.mouse.set_visible(True) 
    return scoreboard.score
    
def instructions(score):
    pygame.display.set_caption("Frog escape!")

    frog = Frog()
    grass = Grass()
    
    allSprites = pygame.sprite.Group(grass, frog)
    insFont = pygame.font.SysFont(None, 35)
    insLabels = []
    instructions = (
    "Frog escape.    Last score: %d" % score ,
    "",
    "Instructions: Use the mouse to control ",
    "the frog. Avoid things that will slow ",
    "you down and hurt you, and eat bugs ",
    "to get a boost away from the snake.",
    "The goal is to have a low score and",
    "finish fast",
    "",
    "Description: You are trying to get away",
    "from a hungry snake. You are a frog who",
    "seems to have all the bad luck. Not long",
    "ago you stumbled upon a hole in the ",
    "ground and happened to be the home of a",
    "very hungry snake. Now you must get away",
    "as quickly as possible.",
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
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
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
    
    
