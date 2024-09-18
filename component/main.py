import pygame
import sys
from globals import *
from scene import Scene
from events import EventHandler

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDHT, SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = Scene(self)
    def run(self):
        while self.running:
            self.update()
            self.draw()
        self.close()
    def update(self):
        EventHandler.poll_events()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        pygame.display.update()
        self.clock.tick(FPS)
        if FPS < 59:
            print("error! fps < ",FPS)
            pygame.quit()
        if EventHandler.keydown(pygame.K_ESCAPE):
            pygame.quit()

        self.scene.update()
    def draw(self):
        self.scene.draw()
    def close(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()