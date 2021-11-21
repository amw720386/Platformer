import random
from typing import Text
import pygame
import time
from pygame.sprite import collide_rect

pygame.init()
clock = pygame.time.Clock()

screen_width = 1280
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')
level = 1


class Platform:
    def __init__(self, x, y, sizex, sizey, color, killer):
        self.rect = pygame.Rect(x, y, sizex, sizey)
        self.killer = killer
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Character:
    def __init__(self, x, y, gravity, velocity, color, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.gravity = gravity
        self.velocity = velocity
        self.jumps = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Enemy:
    def __init__(self, x, y, gravity, velocity, color, size, travelLen, speed, jump):
        self.rect = pygame.Rect(x, y, size, size)
        self.velocity = velocity
        self.gravity = gravity
        self.color = color
        self.prevx = self.rect.x
        self.prevy = self.rect.y
        self.travelLen = travelLen
        self.originx = x
        self.speed = speed
        self.ifjump = random.choices(['yes', 'no'], weights=[1, 25])
        self.jump = jump
        self.canjump = True

    def update(self):
        self.ifjump = random.randint(0, 60)
        self.rect.y += self.velocity
        self.velocity += self.gravity
        if self.rect.x >= self.originx + self.travelLen:
            self.speed *= -1
            self.rect.x -= 10
        elif self.rect.x <= self.originx:
            self.speed *= -1
            self.rect.x += 10
        self.rect.x += self.speed
        if self.jump == True:
            if self.ifjump == 1 and self.canjump == True:
                self.velocity -= 10
                self.canjump = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Avatar(Character):
    def __init__(self, x, y, gravity, velocity, color, size):
        super().__init__(x, y, gravity, velocity, color, size)
        self.prevx = self.rect.x
        self.prevy = self.rect.y

    def update(self):
        self.rect.y += self.velocity
        self.velocity += self.gravity


gamefont = 'TitilliumWeb-Light.ttf'


def put_text(size, text, font, surface, x, y):
    font = pygame.font.Font(font, size)
    text = font.render(text, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = x, y
    surface.blit(text, text_rect)


def gameEnd():
    player.velocity = 0
    player.rect.x = startPos[1][0]
    player.rect.y = startPos[1][1]
    screen.fill((0, 0, 0))
    put_text(200, 'GAME OVER', gamefont, screen,
             screen_width/2, screen_height/2)
    pygame.display.flip()
    time.sleep(1)
    put_text(75, 'RESTARTING', gamefont,
                 screen, screen_width/2, (screen_height/2)+140)
    pygame.display.flip()
    time.sleep(3)


def restart():
    player.rect.x = startPos[level][0]
    player.rect.y = startPos[level][1]


def draw_rect_alpha(surface, color, rect):
    shape_surface = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surface, color, shape_surface.get_rect())
    surface.blit(shape_surface, rect)


gameName = 'SIMPLE'

for index in range(0, len(gameName)):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    put_text(200, gameName[0:index+1], gamefont,
             screen, screen_width/2, screen_height/2)
    pygame.display.flip()
    time.sleep(0.4)
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

while start == True:
    put_text(100, 'PRESS SPACE TO PLAY', gamefont,
             screen, screen_width/2, screen_height/2)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = False
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.flip()
screen.fill((0, 0, 0))

player = Avatar(screen_width/2, screen_height /
                2, 0.5, 0, (255, 255, 255), 35)

levels = {1: [Platform((screen_width/2) - 300/2, (screen_height/2)+50, 300, 100, (210, 180, 140), False),
              Platform(50, (screen_height/2)+200, 900, 100, (210, 180, 140), False), Platform(970, 50, 30, 400, (210, 180, 140), False)], 2: [Platform(0, 100, 300, 30, (210, 180, 140), False), Platform(0, 130, 300, 570, (255, 0, 0), True), Platform(0, 320, 330, 150, (255, 0, 0), True), Platform(400, 0, 880, 600, (250, 0, 0), True), Platform(370, 580, 400, 20, (250, 0, 0), True), Platform(300, 650, 980, 50, (210, 180, 140), False)], 3: [Platform(0, 100, 300, 600, (210, 180, 140), False), Platform(300, 500, 980, 200, (210, 180, 140), False)], 4: [Platform(0, 100, 300, 600, (210, 180, 140), False)]}

startPos = {1: [screen_width/2, screen_height/2],
            2: [100, 50], 3: [100, 50], 4: [100, 50]}

lives = 3
enemies = []

while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player.rect.x += 5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player.jumps == 0:
                player.velocity -= 11
                player.jumps = 1

    player.update()

    if player.rect.y >= screen_height:
        if lives == 1:
            level = 1
            lives = 3
            enemies = []
            gameEnd()
        else:
            lives -= 1
            restart()
    if level == 3:
        if len(enemies) == 0:
            enemies = [Enemy((screen_width/2)-190, screen_height /
                             2, 0.5, 0, (255, 0, 0), 35, 550, 3, True)]
    if player.rect.right >= screen_width:
        level += 1
        player.rect.x = startPos[level][0]
        player.rect.y = startPos[level][1]
        enemies = []
    for item in levels[level]:
        if collide_rect(item, player):
            if item.killer == True:
                if lives == 1:
                    item.killer = False
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
    for item in enemies:
        item.update()
        if collide_rect(player, item):
            if lives == 1:
                level = 1
                lives = 3
                enemies = []
                gameEnd()
            else:
                lives -= 1
                restart()
        for platform in levels[level]:
            if collide_rect(item, platform):
                item.canjump = True
                item.rect.x = item.prevx
                item.rect.y = item.prevy
                item.velocity = 0
    player.prevx = player.rect.x
    player.prevy = player.rect.y
    for item in enemies:
        item.prevx = item.rect.x
        item.prevy = item.rect.y
    screen.fill((0, 0, 0))

    for item in levels[level]:
        item.draw(screen)

    put_text(40, f'LIVES: {lives}', gamefont, screen, 75, 25)
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

    for item in enemies:
        item.draw(screen)
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)
