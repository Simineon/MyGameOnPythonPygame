import pygame
from globals import *
from events import EventHandler
from sprite import Entity, NPC
from Label import Label


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, image: pygame.Surface, position: tuple, parameters: dict) -> None:
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = position)
        #параметры :>

        self.textures = parameters['textures']
        self.group_list = parameters['group_list']
        self.block_group = self.group_list['block_group']
        self.air_group = self.group_list['air_group']
        self.enemy_group = self.group_list['enemy_group']
        self.inventory = parameters['inventory']


        # прам. жизни :D ❤️❤️❤️❤️❤️
        self.health = parameters['health']


        self.velocity = pygame.math.Vector2()
        self.mass = 5
        self.terminal_velocity = self.mass * TERMINALVELOCITY

        self.grouded = True
        self.attakind = True
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.velocity.x = 1
        if keys[pygame.K_a]:
            self.velocity.x = -1
        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            if self.velocity.x > 0:
                self.velocity.x -= 0.1
            elif self.velocity.x < 0:
                self.velocity.x += 0.1
            if abs(self.velocity.x) < 0.3:
                self.velocity.x = 0

        if self.grouded and EventHandler.keydown(pygame.K_SPACE):
            self.grouded = False
            self.velocity.y =- PLAYERJUMPPOWER

        if EventHandler.clicked(1):
            for enemy in self.enemy_group:
                if enemy.rect.collidepoint(self.good_mouse_pos()):
                    self.inventory.slots[self.inventory.active_slot].attack(self, enemy)
        if EventHandler.clicked(1):
            for enemy in self.enemy_group:
                if enemy.rect.collidepoint(self.good_mouse_pos()):
                    self.inventory.slots[self.inventory.active_slot].attack(self, enemy)

    def move(self):
        self.velocity.y += GRAVITY * self.mass

        if self.velocity.y > self.terminal_velocity:
            self.velocity.y = self.terminal_velocity

        self.rect.x += self.velocity.x * PLAYERSPEED
        self.check_collisions('horizontal')
        self.rect.y += self.velocity.y
        self.check_collisions('vertical')

    def check_collisions(self,direction):
        if direction == "horizontal":
            for block in self.block_group:
                if block.rect.colliderect(self.rect):
                    if self.velocity.x > 0: # в право
                        self.rect.right = block.rect.left
                    if self.velocity.x < 0: #в лево
                        self.rect.left = block.rect.right
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
                self.grouded = True
            else:
                self.grouded = False
    def block_handing(self):
        placed = False
        collision = False
        mouse_pos = self.good_mouse_pos()
        if EventHandler.clicked_any():
            for block in self.block_group:
                if block.rect.collidepoint(mouse_pos):
                    collision = True
                    if EventHandler.clicked(1):
                        self.inventory.add_item(block)
                        block.kill()
                if EventHandler.clicked(3):
                    if not collision:
                        placed = True
            for air in self.air_group:
                if air.rect.collidepoint(mouse_pos):
                    collision = True
                    if EventHandler.clicked(1):
                        self.inventory.add_item(air)
                        air.kill()
                if EventHandler.clicked(3):
                    if not collision:
                        placed = True
        if placed and not collision:
            self.inventory.use(self, self.get_block_pos(mouse_pos))
    def good_mouse_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        player_offset = pygame.math.Vector2()
        player_offset.x = SCREENWIDHT / 2- self.rect.centerx
        player_offset.y = SCREENHEIGHT / 2- self.rect.centery
        return (mouse_pos[0] - player_offset.x, mouse_pos[1] - player_offset.y)
    def get_block_pos(self,mouse_pos: tuple):
        return (int((mouse_pos[0]//TILESIZE)*TILESIZE), int((mouse_pos[1]//TILESIZE)*TILESIZE))

    def update(self):
        self.input()
        self.move()
        self.block_handing()
        died = False

        if self.health <= 0:
            died = True
            self.kill()