import math
import random
import pygame
from globals import *
from globals import TILESIZE

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups, image = pygame.Surface((TILESIZE,TILESIZE)), position = (0,0), name: str = 'default'):
        super().__init__(groups)
        self.name = name
        self.in_groups = groups

        self.image = image
        self.rect = self.image.get_rect(topleft = position)
    def update(self):
        pass


class Mob(Entity):
    def __init__(self, groups, image = pygame.Surface((TILESIZE,TILESIZE)), position = (0,0), parameters: dict = None):
        super().__init__(groups, image, position)
        # параметры мобов
        if parameters:
            self.block_group = parameters['block_group']
            self.player = parameters['player']
            self.damage = parameters['damage']

        self.velocity = pygame.math.Vector2()
        self.mass = 5
        self.speed = 0.5
        self.terminal_velocity = TERMINALVELOCITY * self.mass

        self.attacking = True
        self.attacked = False
        self.grounded = False


        self.attack_cooldown = 60
        self.counter = self.attack_cooldown

    def move(self):
        self.velocity.y += GRAVITY * self.mass
        if self.velocity.y > self.terminal_velocity:
            self.velocity.y = self.terminal_velocity

        if abs(math.sqrt((self.rect.x - self.player.rect.x)**2 + (self.rect.y - self.player.rect.y)**2)) < TILESIZE == pygame.time.wait(1):
            if self.rect.x > self.player.rect.x:
                self.velocity.x = -self.speed
            elif self.rect.x < self.player.rect.x:
                self.velocity.x = self.speed
            self.attacking = False
        else:
            self.attacking = True
            self.velocity.x = 0


        if self.rect.x > self.player.rect.x:
            self.velocity.x = -self.speed
        elif self.rect.x < self.player.rect.x:
            self.velocity.x = self.speed

        self.rect.x += self.velocity.x * PLAYERSPEED
        self.check_collisions('horizontal')
        self.rect.y += self.velocity.y
        self.check_collisions('vertical')

        if self.grounded and self.attacking and abs(self.velocity.x) < 0.1:
            self.velocity.y = -8
    def check_collisions(self, direction):
        if direction == "horizontal":
            for block in self.block_group:
                if block.rect.colliderect(self.rect):
                    if self.velocity.x > 0: # в право
                        self.rect.right = block.rect.left
                    if self.velocity.x < 0: #в лево
                        self.rect.left = block.rect.right
                    self.velocity.x = 0
        elif direction == "vertical":
            collisions = 0
            for block in self.block_group:
                if block.rect.colliderect(self.rect):
                    if self.velocity.y > 0: # в низ
                        collisions += 1
                        self.rect.bottom = block.rect.top
                    if self.velocity.y < 0: #вверх
                        self.rect.top = block.rect.bottom
            if collisions > 0:
                self.grounded = True
            else:
                self.grounded = False
    def check_player_collision(self):
        if self.attacking and not self.attacked:
            if self.rect.colliderect(self.player.rect):
                self.player.health -= self.damage
                self.attacked = True
                self.counter = self.attack_cooldown

                if self.player.rect.centerx > self.rect.centerx:
                    self.player.velocity.x = 3
                elif self.player.rect.centerx < self.rect.centerx:
                    self.player.velocity.x = -3

    def update(self):
        self.move()
        self.check_player_collision()
        if self.attacked:
            self.counter -= 1
            if self.counter < 0:
                self.counter = self.attack_cooldown
                self.attacked = False

class NPC(Entity):
    def __init__(self, npc, image = pygame.Surface((TILESIZE,TILESIZE)), position = (0,0), parameters: dict = None):
        super().__init__(npc, image, position)
        # параметры npc
        if parameters:
            self.block_group = parameters['block_group']
            self.player = parameters['player']
            self.talk = parameters['talk']


        self.velocity = pygame.math.Vector2()
        self.mass = 5
        self.speed = 0.5
        self.terminal_velocity = TERMINALVELOCITY * self.mass

        self.talking = True
        self.talked = False
        self.grounded = False


        self.talked_cooldown = 60
        self.counter = self.talked_cooldown

    def move(self):
        self.velocity.y += GRAVITY * self.mass
        if self.velocity.y > self.terminal_velocity:
            self.velocity.y = self.terminal_velocity

        if abs(math.sqrt((self.rect.x - self.player.rect.x)**2 + (self.rect.y - self.player.rect.y)**2)) < TILESIZE == pygame.time.wait(1):
            if self.rect.x > random.randint(0, 1000):
                self.velocity.x = -self.speed
            elif self.rect.x < random.randint(0, 1000):
                self.velocity.x = self.speed
            self.talking = False
        else:
            self.talking = True
            self.velocity.x = 0


        if self.rect.x > random.randint(0, 1000):
            self.velocity.x = -self.speed
        elif self.rect.x < random.randint(0, 1000):
            self.velocity.x = self.speed

        self.rect.x += self.velocity.x * PLAYERSPEED
        self.check_collisions('horizontal')
        self.rect.y += self.velocity.y
        self.check_collisions('vertical')

        if self.grounded and self.talking and abs(self.velocity.x) < 0.1:
            self.velocity.y = -8
    def check_collisions(self, direction):
        if direction == "horizontal":
            for block in self.block_group:
                if block.rect.colliderect(self.rect):
                    if self.velocity.x > 0: # в право
                        self.rect.right = block.rect.left
                    if self.velocity.x < 0: #в лево
                        self.rect.left = block.rect.right
                    self.velocity.x = 0
        elif direction == "vertical":
            collisions = 0
            for block in self.block_group:
                if block.rect.colliderect(self.rect):
                    if self.velocity.y > 0: # в низ
                        collisions += 1
                        self.rect.bottom = block.rect.top
                    if self.velocity.y < 0: #вверх
                        self.rect.top = block.rect.bottom
            if collisions > 0:
                self.grounded = True
            else:
                self.grounded = False
    def check_player_collision(self):
        if self.talking and not self.talked:
            if self.rect.colliderect(self.player.rect):
                self.player.health += self.talk
                self.talked = True
                self.counter = self.talked_cooldown

                if self.player.rect.centerx > self.rect.centerx:
                    self.player.velocity.x = 3
                elif self.player.rect.centerx < self.rect.centerx:
                    self.player.velocity.x = -3

    def update(self):
        self.move()
        self.check_player_collision()
        if self.talked:
            self.counter -= 1
            if self.counter < 0:
                self.counter = self.talked_cooldown
                self.talked = False

