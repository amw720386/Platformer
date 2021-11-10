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


class Avatar(Character):
    def __init__(self, x, y, gravity, velocity, color, size):
        super().__init__(x, y, gravity, velocity, color, size)

    def update(self):
        self.rect.y += self.velocity
        self.velocity += self.gravity


player = Avatar(screen_width/2, screen_height /
                2, 0.5, 0, (255, 255, 255), 35)

levels = {1: [Platform((screen_width/2) - 300/2, (screen_height/2)+50, 300, 100, (210, 180, 140), False), Platform(375, (screen_height/2)+50, 115, 100, (255, 0, 0), True),
          Platform(50, (screen_height/2)+200, 900, 100, (210, 180, 140), False), Platform(900, 51, 10, 399, (255, 0, 0), True), Platform(910, 50, 30, 400, (210, 180, 140), False)], 2: [Platform(50, 100, 300, 100, (210, 180, 140), False)]}
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
    if level == 1:
        if player.rect.right >= screen_width:
            level += 1
            player.rect.x = 100
            player.rect.y = 50
    if player.rect.y >= screen_height:
        time.sleep(0.2)
        pygame.quit()
    for item in levels[level]:
        if collide_rect(item, player):
            if item.killer == True:
                time.sleep(0.2)
                pygame.quit()
            player.jumps = 0
            player.velocity = 0
            while collide_rect(item, player):
                player.rect.x = prevxy[0]
                player.rect.y = prevxy[1]
    prevxy = [player.rect.x, player.rect.y]
    screen.fill((0, 0, 0))

    for item in levels[level]:
        item.draw(screen)
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60)
