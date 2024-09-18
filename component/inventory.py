import pygame
from globals import *
from items import *
from events import EventHandler
from player import Player
from player import *
from textureDate import *

class Inventory:
    def __init__(self, app, textures) -> None:
        self.app = app
        self.screen = app.screen
        self.textures = textures
        self.health = parametrs={'health':10}



        #слоты еееееййййй :>
        self.slots = []
        self.slotsA = []
        for index in range(5):
            self.slots.append(Item())
        self.slots[0] = ShortSwordCItem("short_sword", 1)
        self.slots[1] = BlockItem("grass", 5)
        self.slots[2] = BlockItem("dirt", 5)
        self.slots[3] = BlockItem("stone", 5)
        self.slots[4] = BlockItem("stone", 5)
        self.active_slot = 0
        self.font = pygame.font.Font(None, 30)
        for index in range(5):
            self.slotsA.append(Item())
        self.slotsA[0] = BlockItem("stone", 5)
        self.slotsA[1] = BlockItem("deamond",0)
        self.slotsA[2] = BlockItem("dirt", 5)
        self.slotsA[3] = BlockItem("tree", 5)
        self.slotsA[4] = BlockItem("wood", 5)
        self.active_slotB = 0
        self.font = pygame.font.Font(None, 30)

    def debug(self):
        for slot in self.slots:
            print(slot)
    def use(self, player, position):
        if self.slots[self.active_slot].name != 'default':
            self.slots[self.active_slot].use(player,position)
        if self.slotsA[self.active_slotB].name != 'default':
            self.slotsA[self.active_slotB].use(player,position)

    def add_item(self, item):
        first_available_slot = len(self.slots)
        target_slot = len(self.slots)
        for index, slot in enumerate(self.slots):
            if slot.name  == "default" and index < first_available_slot:
                first_available_slot = index
            if slot.name == item.name:
                target_slot = index
        if target_slot < len(self.slots):
            self.slots[target_slot].quantity += items[item.name].quantity
        elif first_available_slot < len(self.slots):
            self.slots[first_available_slot] = items[item.name].item_type(item.name, items[item.name].quantity)

        first_available_slot = len(self.slotsA)
        target_slot = len(self.slotsA)
        for index, slot in enumerate(self.slotsA):
            if slot.name == "default" and index < first_available_slot:
                first_available_slot = index
            if slot.name == item.name:
                target_slot = index
        if target_slot < len(self.slotsA):
            self.slotsA[target_slot].quantity += items[item.name].quantity
        elif first_available_slot < len(self.slotsA):
            self.slotsA[first_available_slot] = items[item.name].item_type(item.name, items[item.name].quantity)

    def update(self):
        if EventHandler.keydown(pygame.K_RIGHT):
            if self.active_slot < len(self.slots)-1:
                self.active_slot += 1
            print(f'Active slot: {self.active_slot}')
        if EventHandler.keydown(pygame.K_LEFT):
            if self.active_slot > 0:
                self.active_slot -= 1
            print(f'Active slot: {self.active_slot}')
        if EventHandler.keydown(pygame.K_b):
            if self.active_slotB < len(self.slotsA)-1:
                self.active_slotB += 1
            print(f'Active slot: {self.active_slotB}')
        if EventHandler.keydown(pygame.K_v):
            if self.active_slotB > 0:
                self.active_slotB -= 1
            print(f'Active slot: {self.active_slotB}')

        if EventHandler.clicked_any():
            self.debug()
    def draw(self):
        pygame.draw.rect(self.screen, "gray", pygame.Rect(0,0,(TILESIZE*2)*len(self.slots), TILESIZE*2))
        pygame.draw.rect(self.screen, "red", pygame.Rect(1000, 0, (TILESIZE * 2) * len(self.slots), TILESIZE * 2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            pygame.draw.rect(self.screen, "gray", pygame.Rect(0, 0, (TILESIZE * 2) * len(self.slotsA), TILESIZE * 4))

        x_offset = TILESIZE/2
        y_offset = TILESIZE/2

        for i in range(len(self.slots)):
            if i == self.active_slot:
                pygame.draw.rect(self.screen, "white", pygame.Rect(i*(TILESIZE*2), 0, TILESIZE*2, TILESIZE*2))
            pygame.draw.rect(self.screen, "black", pygame.Rect(i * (TILESIZE * 2), 0, TILESIZE * 2, TILESIZE * 2),2)
            if self.slots[i].name != "default":
                self.screen.blit(self.textures[self.slots[i].name], (x_offset + (TILESIZE*2)*i, y_offset))
                self.amount_text = self.font.render(str(self.slots[i].quantity), True, "black")
                self.screen.blit(self.amount_text,((TILESIZE*2)*i+5, 5))
        pygame.draw.rect(self.screen, "black", pygame.Rect(0, 0, (TILESIZE * 2) * len(self.slots), TILESIZE * 2),2)
        for i in range(len(self.slotsA)):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                if i == self.active_slotB:
                    pygame.draw.rect(self.screen, "white",pygame.Rect(i * (TILESIZE * 2), 64.9, TILESIZE * 2, TILESIZE * 2))
                pygame.draw.rect(self.screen, "black", pygame.Rect(i * (TILESIZE * 2), 0, TILESIZE * 2, TILESIZE * 4),2)
                pygame.draw.rect(self.screen, "black", pygame.Rect(i * (TILESIZE * 2), 0, TILESIZE * 2, TILESIZE * 4),2)
            if self.slotsA[i].name != "default":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    self.screen.blit(self.textures[self.slotsA[i].name], (x_offset + (TILESIZE * 2) * i, 70)) #
                    self.amount_text = self.font.render(str(self.slotsA[i].quantity), True, "black")
                    self.screen.blit(self.amount_text, ((TILESIZE * 2) * i + 5, 70))
        pygame.draw.rect(self.screen, "black", pygame.Rect(0, 0, (TILESIZE * 2) * len(self.slotsA), TILESIZE * 2), 2)