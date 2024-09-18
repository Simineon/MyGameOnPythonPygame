import pygame
from globals import *
from sprite import Entity, Mob, NPC
from player import Player
from textureDate import solo_texture_date,atlas_texture_date
from opensimplex import OpenSimplex
from camera import Camera
from inventory import Inventory
from items import *
import random


class Scene:
    def __init__(self, app):
        self.app = app
        self.screen = app.screen

        self.textures = self.gen_solo_textures()
        self.textures.update(self.gen_atlas_textures('Res/texAtl.png'))


        player_texture = pygame.image.load('Res/player.png').convert_alpha()
        player_texture = pygame.transform.scale(player_texture,(TILESIZE,TILESIZE))



        self.sprites = Camera()
        self.blocks = pygame.sprite.Group()
        self.air = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.group_list: dict[str, pygame.sprite.Group] = {
            'sprites':self.sprites,
            'block_group':self.blocks,
            'air_group':self.air,
            'enemy_group':self.enemy_group

        }
        #инвентарь
        self.inventory = Inventory(self.app, self.textures)
        #self.entity = Entity([self.sprites, self.blocks], image=self.textures['dirt'])

        self.player = Player([self.sprites], self.textures['player_static'], (550, 200),parameters=
        {'group_list':self.group_list,'textures':self.textures, 'inventory':self.inventory, 'health': 10})

        Mob([self.sprites, self.enemy_group], self.textures['mob1'], (800,-500), parameters={'block_group':self.blocks,
                                                                           'player':self.player,'damage':1,})

        NPC([self.sprites, self.enemy_group], self.textures['mob3'], (1000,-500), parameters={'block_group':self.blocks,
                                                                           'player':self.player,'talk':0,})
        #Mob([self.sprites, self.enemy_group], self.textures['mob4'], (1100,-500), parameters={'block_group':self.blocks,
        #                                                                   'player':self.player,'damage':1,})
        #Mob([self.sprites, self.enemy_group], self.textures['mob5'], (1200,-500), parameters={'block_group':self.blocks,
        #                                                                   'player':self.player,'damage':1,}


        self.gen_world()

    def gen_solo_textures(self) -> dict:
        textures ={}

        for name, date, in solo_texture_date.items():
            textures[name] = pygame.transform.scale(pygame.image.load(date['file_path']).convert_alpha(), (date['size']))

        return textures
    def gen_atlas_textures(self, filepath):
        textures = {}

        atlas_img = pygame.transform.scale(pygame.image.load(filepath).convert_alpha(), (TILESIZE*16, TILESIZE*16)) #4.11 = dirt

        for name, date, in atlas_texture_date.items():
            textures[name] = pygame.Surface.subsurface(atlas_img, pygame.Rect(date['position'][0]*TILESIZE,
                                                                              date['position'][1]*TILESIZE,date['size'][0],date['size'][1]))

        return textures
    def gen_world(self):
        noise_generator = OpenSimplex(seed=92392893)
        heightmap = []
        def Gen1():
            for y in range(400):#max - 450
                noise_value = noise_generator.noise2(y * 0.05,  0)
                height = int((noise_value * 1)* 4 + 40)
                heightmap.append(height)
            for x in range(len(heightmap)):
                for y in range(heightmap[x]):
                    y_offset = 5 -y + 6
                    block_type = 'dirt'
                    if y == heightmap[x]-1:
                        block_type = 'grass'
                    if y < heightmap[x]-6:
                        block_type = 'stone'
                    Entity([self.sprites, self.blocks], self.textures[block_type], (x*TILESIZE,y_offset*TILESIZE),name=block_type)
            for x in range(5):
                block_type = 'wood'
                Entity([self.sprites, self.blocks], self.textures[block_type], (x * TILESIZE+512, y_offset * 30.920),name=block_type)
                #(x * TILESIZE+512, y_offset * 30.920)
            for x in range(1):
                block_type = 'wood'
                Entity([self.sprites, self.blocks], self.textures[block_type], (x * TILESIZE+512, y_offset * 32),name=block_type)
            for x in range(1):
                block_type = 'wood'
                Entity([self.sprites, self.blocks], self.textures[block_type], (x * TILESIZE+640, y_offset * 32),name=block_type)
            for x in range(1):
                block_type = 'wood'
                Entity([self.sprites, self.blocks], self.textures[block_type], (x * TILESIZE+640, y_offset * 32),name=block_type)
            for x in range(1):
                block_type = 'tree'
                Entity([self.sprites, self.air], self.textures[block_type], (x * TILESIZE+700, y_offset * 38.4),name=block_type)
            for x in range(1):
                block_type = 'tree'
                Entity([self.sprites, self.air], self.textures[block_type], (x * TILESIZE+400, y_offset * 37.3),name=block_type)
            for x in range(1):
                block_type = 'tree'
                Entity([self.sprites, self.air], self.textures[block_type], (x * TILESIZE+800, y_offset * 37.3),name=block_type)
            for x in range(1):
                block_type = 'tree'
                Entity([self.sprites, self.air], self.textures[block_type], (x * TILESIZE+1150, y_offset * 37.3),name=block_type)
            #да это сложно :(
            for x in range(3):
                block_type = 'deamond'
                Entity([self.sprites, self.blocks], self.textures[block_type], (x * TILESIZE + 512, y_offset * 22.390),name=block_type)
                for y in range(2):
                    block_type = 'deamond'
                    Entity([self.sprites, self.blocks], self.textures[block_type], (x * TILESIZE+512, y_offset * 23.45),name=block_type)
        Gen1()

    def update(self):
        self.sprites.update()
        self.inventory.update()

    def draw(self):
        self.app.screen.fill('lightblue')
        self.sprites.draw(self.player, self.app.screen)
        if self.player.health == 0:
            time_text = Label(350, 100)
            time_text.set_text('GAME OVER!', 90, 'red')
            time_text.draw(50, 50)
            if EventHandler.keydown(pygame.K_r):
                print('restart - False')
        self.inventory.draw()
