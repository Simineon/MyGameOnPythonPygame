import pygame
from player import Player


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw(self, target: Player, display: pygame.Surface):
        offset = pygame.math.Vector2()
        offset.x = display.get_width() / 2 - target.rect.centerx
        offset.y = display.get_height() / 2 - target.rect.centery

        for sprite in self.sprites():
            sprite_offset = pygame.math.Vector2()
            sprite_offset.x = offset.x + sprite.rect.x
            sprite_offset.y = offset.y + sprite.rect.y

            display.blit(sprite.image, sprite_offset)
