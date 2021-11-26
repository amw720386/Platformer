# imports the necessary modules for this project
from pygame.sprite import collide_rect
import time
import pygame
import random

# initiates pygame and creates a variable for tick rate
pygame.init()
clock = pygame.time.Clock()

# standard variable setting and creates a screen for the game to be played on
screen_width = 1280
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')
level = 1
BEIGE = (210, 180, 140)
RED = (255, 0, 0)
lives = 3
enemies = []


# platform class where you can determine thet color, size, position and whether a platform kills you or not
class Platform:
    def __init__(self, x, y, sizex, sizey, color, killer):
        self.rect = pygame.Rect(x, y, sizex, sizey)
        self.killer = killer
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# character class, if I want to make this game 2 player in the future


class Character:
    def __init__(self, x, y, gravity, velocity, color, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.gravity = gravity
        self.velocity = velocity
        self.jumps = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


# in this i've made enemies extremely adjustable, with varying speed, whether they jump and whether they move
class Enemy:
    def __init__(self, x, y, gravity, velocity, color, size, travelLen, speed, jump, walk):
        self.rect = pygame.Rect(x, y, size, size)
        self.velocity = velocity
        self.gravity = gravity
        self.color = color
        self.prevx = self.rect.x
        self.prevy = self.rect.y
        self.travelLen = travelLen
        self.originx = x
        self.speed = speed
        self.ifjump = ''
        self.jump = jump
        self.walk = walk
        self.canjump = True

    def update(self):
        # rolls to see if the enemy can jump
        self.ifjump = random.randint(0, 60)
        self.rect.y += self.velocity  # standard gravity stuff
        self.velocity += self.gravity
        # this makes the enemies walk back and forth (if their allowed to)
        if self.walk == True:
            if self.rect.x >= self.originx + self.travelLen:
                self.speed *= -1
                self.rect.x -= 10
            elif self.rect.x <= self.originx:
                self.speed *= -1
                self.rect.x += 10
            self.rect.x += self.speed
        if self.jump == True:  # makes enemies jump if their allowed to
            if self.ifjump == 1 and self.canjump == True:
                self.velocity -= 10
                self.canjump = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# this is currently the only use of the character class


class Avatar(Character):
    def __init__(self, x, y, gravity, velocity, color, size):
        super().__init__(x, y, gravity, velocity, color, size)
        self.prevx = self.rect.x
        self.prevy = self.rect.y

    def update(self):
        self.rect.y += self.velocity  # standard gravity stuff again
        self.velocity += self.gravity


# have this because I don't want to be writing out the fontfile everytime
gamefont = 'Platformer\TitilliumWeb-Light.ttf'

# this function is self explanatory, it "puts" the text using the positioning of .get_rect()


def put_text(size, text, font, surface, x, y):
    font = pygame.font.Font(font, size)
    text = font.render(text, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = x, y
    surface.blit(text, text_rect)


def gameEnd():  # this function is processed when the game ends and the player is out of lives
    player.velocity = 0  # this is so that the player doesnt continue to fall when they respawn
    # the next two lines are resetting the x and y positions of the player
    player.rect.x = startPos[1][0]
    player.rect.y = startPos[1][1]
    # the rest is just text rendering, to make the end game screen I have
    screen.fill((0, 0, 0))
    put_text(200, 'GAME OVER', gamefont, screen,
             screen_width/2, screen_height/2)
    pygame.display.flip()
    time.sleep(0.5)
    put_text(75, 'RESTARTING', gamefont,
                 screen, screen_width/2, (screen_height/2)+140)
    pygame.display.flip()
    time.sleep(2)


def restart():  # this resets the position of the player and is called when they die
    player.rect.x = startPos[level][0]
    player.rect.y = startPos[level][1]


# this is the games name and comes in handy for when rendering the title screen
gameName = 'SIMPLE'

for index in range(0, len(gameName)):  # renders the title screen
    for event in pygame.event.get():  # checks for whether the player wants to close the game
        if event.type == pygame.QUIT:
            pygame.quit()
    put_text(200, gameName[0:index+1], gamefont,
             screen, screen_width/2, screen_height/2)  # based off of the gameName var, the text renders
    pygame.display.flip()
    time.sleep(0.4)
    # the rest is for rendering the words 'platformer' and 'physics'
    if gameName[0:index+1] == gameName:
        time.sleep(0.4)
        put_text(75, 'PLATFORMER', gamefont,
                 screen, screen_width/2, (screen_height/2)+125)
        pygame.display.flip()
        time.sleep(0.7)
        put_text(50, 'PHYSICS', gamefont,
                 screen, screen_width/2, (screen_height/2)+190)
        pygame.display.flip()
        time.sleep(1.5)
    screen.fill((0, 0, 0))

start = True

while start == True:  # this is the game startup page, where you have to press space to continue
    put_text(100, 'PRESS SPACE TO PLAY', gamefont,
             screen, screen_width/2, screen_height/2)
    for event in pygame.event.get():  # also allow the player to quit here
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = False
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.flip()
screen.fill((0, 0, 0))

# this is all the starting positions for each level
startPos = {1: [screen_width/2, screen_height/2],
            2: [100, 50], 3: [100, 50], 4: [100, 50], 5: [100, 600], 6: [100, 350], 7: [100, 50], 8: [100, 550]}

player = Avatar(startPos[level][0], startPos[level]  # this creates the player, with the details being customizable
                [1], 0.5, 0, (255, 255, 255), 35)

# this is my database for levels, its adjustable and is labeled based on level.
levels = {1: [Platform((screen_width/2) - 300/2, (screen_height/2)+50, 300, 100, BEIGE, False), Platform(50, (screen_height/2)+200, 900, 100, BEIGE, False), Platform(970, 50, 30, 400, BEIGE, False)],
          2: [Platform(0, 100, 300, 30, BEIGE, False), Platform(0, 130, 300, 570, RED, True), Platform(0, 320, 330, 150, RED, True), Platform(400, 0, 880, 600, (250, 0, 0), True), Platform(370, 580, 400, 20, (250, 0, 0), True), Platform(300, 650, 980, 50, BEIGE, False)],
          3: [Platform(0, 100, 300, 600, BEIGE, False), Platform(300, 500, 980, 200, BEIGE, False)],
          4: [Platform(0, 100, 300, 600, BEIGE, False), Platform(350, 0, 930, 400, RED, True), Platform(350, 450, 250, 20, BEIGE, False), Platform(650, 0, 630, 550, RED, True), Platform(650, 600, 630, 20, BEIGE, False)],
          5: [Platform(0, 650, 200, 50, BEIGE, False), Platform(200, 650, 150, 50, RED, True), Platform(350, 650, 200, 50, BEIGE, False), Platform(550, 650, 150, 50, RED, True), Platform(700, 650, 200, 50, BEIGE, False), Platform(900, 650, 150, 50, RED, True), Platform(1050, 650, 230, 50, BEIGE, False)],
          6: [Platform(0, 400, 300, 10, BEIGE, False), Platform(550, 400, 300, 10, BEIGE, False), Platform(1100, 400, 180, 10, BEIGE, False)],
          7: [Platform(0, 100, 300, 100, BEIGE, False), Platform(300, 100, 980, 100, RED, True), Platform(0, 600, 1280, 100, BEIGE, False)],
          8: [Platform(0, 600, 1280, 100, BEIGE, False)]}

#this is my game loop
while True:
    keys = pygame.key.get_pressed() #this gets the player movements for left or right
    if keys[pygame.K_LEFT]:
        player.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player.rect.x += 5
    for event in pygame.event.get(): #allows for the player to close the program
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN: #allows player to jump
            if event.key == pygame.K_UP and player.jumps == 0:
                player.velocity -= 11
                player.jumps = 1

    player.update() #updates player

    if player.rect.y >= screen_height: #code below is for what happens if the player touches the bottom of the screen
        if lives == 1:
            level = 1
            lives = 3
            enemies = []
            gameEnd()
        else:
            lives -= 1
            restart()

    if len(enemies) == 0: #creates enemies based off of level
        if level == 3: #for level 3
            enemies = [Enemy((screen_width/2)-190, screen_height /
                             2, 0.5, 0, RED, 35, 550, 3, True, True)]
        if level == 5: #for level 5
            enemies = [Enemy(350, 615, 0.5, 0, RED, 35, 165, 3, False, True), Enemy(
                787.5, 615, 0.4, 0, RED, 35, 0, 0, True, False)]
    if player.rect.right >= screen_width: #this is what happens when the player touches the right of the screen
        if level == max(levels.keys()):
            level = 1
        else:
            level += 1
        player.rect.x = startPos[level][0]
        player.rect.y = startPos[level][1]
        enemies = []
    
    for item in levels[level]:
        if collide_rect(item, player): #this checks for collisions between players and platforms
            if item.killer == True: #checks if the platform should kill you
                if lives == 1: 
                    level = 1
                    player.prevx = startPos[level][0]
                    player.prevy = startPos[level][1]
                    lives = 3
                    enemies = []
                    gameEnd()
                else:
                    player.prevx = startPos[level][0]
                    player.prevy = startPos[level][1]
                    lives -= 1
                    restart()
            player.jumps = 0
            player.velocity = 0
            player.rect.x = player.prevx
            player.rect.y = player.prevy

    for item in enemies: #upates enemies 
        item.update()
        if collide_rect(player, item): #checks if an enemy touches the player
            if lives == 1:
                level = 1
                lives = 3
                enemies = []
                gameEnd()
            else:
                lives -= 1
                restart()
        for platform in levels[level]: #this does collisions for enemies and platforms
            if collide_rect(item, platform):
                item.canjump = True
                item.rect.x = item.prevx
                item.rect.y = item.prevy
                item.velocity = 0
    player.prevx = player.rect.x #this is required so that players cant just pass through platforms and can walljump
    player.prevy = player.rect.y
    for item in enemies: #same as the above code but for enemies
        item.prevx = item.rect.x
        item.prevy = item.rect.y
    screen.fill((0, 0, 0))

    for item in levels[level]: #drawing the actual platforms
        item.draw(screen)

    put_text(40, f'LIVES: {lives}', gamefont, screen, 75, 25) #everything below is for text rendering during levels
    if level == 1:
        if player.rect.x > (screen_width/2) + 150:
            put_text(30, 'YOU CAN WALL JUMP',
                     gamefont, screen, 1100, 500)
        else:
            put_text(30, 'USE ARROWS TO MOVE AROUND',
                     gamefont, screen, screen_width/2, (screen_height/2) - 100)
            put_text(30, 'GO TO THE RIGHT SIDE OF THE',
                     gamefont, screen, screen_width/2, (screen_height/2) - 70)
            put_text(30, 'SCREEN TO COMPLETE THE LEVEL',
                     gamefont, screen, screen_width/2, (screen_height/2) - 40)
    if level == 2:
        if player.rect.y > 600:
            put_text(30, 'YOU DID IT :D',
                     gamefont, screen, 800, 625)
        else:
            put_text(30, 'DONT TOUCH RED :)',
                     gamefont, screen, 800, 625)
    if level == 3:
        put_text(30, 'DONT TOUCH ENEMIES', gamefont,
                 screen, (screen_width/2) + 175, (screen_height/2)-175)
    if level == 5:
        put_text(30, 'HEHE, LOTS OF ENEMIES', gamefont,
                 screen, (screen_width/2), (screen_height/2) + 150)
    if level == 6:
        put_text(30, 'HARD JUMPS D:', gamefont,
                 screen, (screen_width/2), (screen_height/2) - 200)
    if level == 7:
        put_text(30, 'HOW?', gamefont,
                 screen, (screen_width/2), (screen_height/2))
    if level == 8:
        put_text(50, 'VICTORY! GO TO THE RIGHT TO RESTART', gamefont,
                 screen, screen_width/2, (screen_height/2) - 50)

    for item in enemies: #drawing enemies
        item.draw(screen)
    player.draw(screen) #drawing the player

    pygame.display.flip()
    clock.tick(60)
