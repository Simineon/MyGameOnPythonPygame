import pygame
from globals import *

back = (102, 255, 255)
window = pygame.display.set_mode((SCREENWIDHT, SCREENHEIGHT))
window.fill(back)

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)  # прямоугольник
        self.fill_color = back
        if color:
            self.fill_color = color
    def color(self, new_color):
        self.fill_color = new_color
    def fill(self):
        pygame.draw.rect(window, self.fill_color, self.rect)
    def outline(self, frame_color, thickness):  # обводка существующего прямоугольника
        pygame.draw.rect(window, frame_color, self.rect, thickness)


class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


#time_text = Label(150, 150, 50, 50, back)
#time_text.set_text('YOU WIN!', 90, 90)
#time_text.draw(50, 50)