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
    def __init__(self, x, y, gravity, velocity, color, size, travelLen, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.velocity = velocity
        self.gravity = gravity
        self.color = color
        self.prevx = self.rect.x
        self.prevy = self.rect.y
        self.travelLen = travelLen
        self.originx = x
        self.speed = speed

    def update(self):
        self.rect.y += self.velocity
        self.velocity += self.gravity
        if self.rect.x >= self.originx + self.travelLen:
            self.speed *= -1
        elif self.rect.x <= self.originx:
            self.speed *= -1
        self.rect.x += self.speed

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
        if self.rect.y >= screen_height:
            time.sleep(0.2)
            pygame.quit()


def put_text(size, text, font, surface, x, y):
    font = pygame.font.Font(font, size)
    text = font.render(text, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = x, y
    surface.blit(text, text_rect)


gameName = 'SIMPLE'

for index in range(0, len(gameName)):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    put_text(200, gameName[0:index+1], 'TitilliumWeb-Light.ttf',
             screen, screen_width/2, screen_height/2)
    pygame.display.flip()
    time.sleep(0.4)
    if gameName[0:index+1] == gameName:
        time.sleep(0.4)
        put_text(75, 'PLATFORMER', 'TitilliumWeb-Light.ttf',
                 screen, screen_width/2, (screen_height/2)+125)
        pygame.display.flip()
        time.sleep(0.7)
        put_text(50, 'PHYSICS', 'TitilliumWeb-Light.ttf',
                 screen, screen_width/2, (screen_height/2)+190)
        pygame.display.flip()
        time.sleep(1.5)
    screen.fill((0, 0, 0))

start = True

while start == True:
    put_text(100, 'PRESS SPACE TO PLAY', 'TitilliumWeb-Light.ttf',
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
              Platform(50, (screen_height/2)+200, 900, 100, (210, 180, 140), False), Platform(970, 50, 30, 400, (210, 180, 140), False)], 2: [Platform(0, 100, 300, 30, (210, 180, 140), False), Platform(0, 130, 300, 570, (255, 0, 0), True), Platform(0, 320, 330, 150, (255, 0, 0), True), Platform(400, 0, 880, 600, (250, 0, 0), True), Platform(370, 580, 400, 20, (250, 0, 0), True), Platform(300, 650, 980, 50, (210, 180, 140), False)], 3: [Platform(0, 100, 300, 600, (210, 180, 140), False), Platform(300, 500, 980, 200, (210, 180, 140), False)]}

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

    if level == 3:
        if len(enemies) == 0:
            enemies = [Enemy((screen_width/2)-190, screen_height /
                             2, 0.5, 0, (255, 0, 0), 35, 500, 5)]
    if player.rect.right >= screen_width:
        level += 1
        player.rect.x = 100
        player.rect.y = 50
    for item in levels[level]:
        if collide_rect(item, player):
            if item.killer == True:
                time.sleep(0.2)
                pygame.quit()
            player.jumps = 0
            player.velocity = 0
            if collide_rect(item, player):
                player.rect.x = player.prevx
                player.rect.y = player.prevy
    for item in enemies:
        item.update()
        for platform in levels[level]:
            if collide_rect(item, platform):
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

    if level == 1:
        if player.rect.x > (screen_width/2) + 150:
            put_text(30, 'YOU CAN WALL JUMP',
                     'TitilliumWeb-Light.ttf', screen, 1100, 500)
        else:
            put_text(30, 'USE ARROWS TO MOVE AROUND',
                     'TitilliumWeb-Light.ttf', screen, screen_width/2, (screen_height/2) - 100)
            put_text(30, 'GO TO THE RIGHT SIDE OF THE',
                     'TitilliumWeb-Light.ttf', screen, screen_width/2, (screen_height/2) - 70)
            put_text(30, 'SCREEN TO COMPLETE THE LEVEL',
                     'TitilliumWeb-Light.ttf', screen, screen_width/2, (screen_height/2) - 40)
    if level == 2:
        if player.rect.y > 600:
            put_text(30, 'YOU DID IT :D',
                     'TitilliumWeb-Light.ttf', screen, 800, 625)
        else:
            put_text(30, 'DONT TOUCH RED :)',
                     'TitilliumWeb-Light.ttf', screen, 800, 625)

    for item in enemies:
        item.draw(screen)
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)
