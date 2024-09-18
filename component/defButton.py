import pygame
import sys
from button import ImageButton

pygame.init()


WIDHT, HEIGHT = 600, 500

screen = pygame.display.set_mode((WIDHT,HEIGHT))
pygame.display.set_caption("Button Test")


green_button = ImageButton(WIDHT/2-(252/2), 100, 252, 74, "PLAY", "green_button.png", "green_button_hover.png","click.mp3")
green_button2 = ImageButton(WIDHT/2-(252/2), 300, 252, 74, "Exit", "red_button.png", "red_button_hover.png","click.mp3")
green_button3 = ImageButton(WIDHT/2-(252/2), 200, 252, 74, "Setting", "green_button.png", "green_button_hover.png","click.mp3")



def main_menu():
    running = True
    while running:
        screen.fill((0,0,0))

        font = pygame.font.Font(None, 72)
        text_surface = font.render("INTER menu ", True,(255,255,255))
        text_rect = text_surface.get_rect(center=(300, 50))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == green_button:
                print('Play started')

            green_button.handle_event(event)
            green_button2.handle_event(event)
            green_button3.handle_event(event)

        green_button.check_hover(pygame.mouse.get_pos())
        green_button.draw(screen)
        green_button2.check_hover(pygame.mouse.get_pos())
        green_button2.draw(screen)
        green_button3.check_hover(pygame.mouse.get_pos())
        green_button3.draw(screen)
        pygame.display.flip()

main_menu()