import pygame
import sys
from button import ImageButton
from main import Game

pygame.init()

WIDHT, HEIGHT = 960, 600

screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("INTER")
main_background = pygame.image.load("res/background.png")

def main_menu():
    green_button = ImageButton(WIDHT / 2 - (252 / 2), 150, 252, 74, "PLAY", "res/green_button.png",
                               "res/green_button_hover.png", "res/click.mp3")
    green_button2 = ImageButton(WIDHT / 2 - (252 / 2), 350, 252, 74, "Exit", "res/red_button.png", "res/red_button_hover.png",
                                "res/click.mp3")
    setting_button = ImageButton(WIDHT / 2 - (252 / 2), 250, 252, 74, "Setting", "res/green_button.png",
                                "res/green_button_hover.png", "res/click.mp3")
    running = True
    while running:
        screen.fill((0,0,0))
        screen.blit(main_background, (0, 0))

        font = pygame.font.Font(None, 72)
        text_surface = font.render("INTER menu ", True,(255,255,255))
        text_rect = text_surface.get_rect(center=(WIDHT/2,100))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == green_button:
                print('game started')
                fade()
                new_game()

            if event.type == pygame.USEREVENT and event.button == setting_button:
                print('setting open')
                fade()
                settings_menu()

            if event.type == pygame.USEREVENT and event.button == green_button2:
                running =False
                pygame.quit()
                sys.exit()



            for btn in [green_button, green_button2,setting_button]:
                btn.handle_event(event)
        for btn in [green_button, green_button2, setting_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()

def settings_menu():
    audio_button = ImageButton(WIDHT / 2 - (252 / 2), 150, 252, 74, "Audio", "res/green_button.png", "res/green_button_hover.png","res/click.mp3")
    vidio_button = ImageButton(WIDHT / 2 - (252 / 2), 250, 252, 74, "Vidio", "res/green_button.png","res/green_button_hover.png", "res/click.mp3")
    back_button = ImageButton(WIDHT / 2 - (252 / 2), 350, 252, 74, "Back", "res/green_button.png","res/green_button_hover.png", "res/click.mp3")

    running = True
    while running:
        screen.fill((0,0,0))
        screen.blit(main_background, (0,0))
        font = pygame.font.Font(None, 72)
        text_surface = font.render("Setting", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDHT / 2, 100))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False



            for btn in [audio_button, vidio_button, back_button]:
                btn.handle_event(event)

        for btn in [audio_button, vidio_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        pygame.display.flip()


def new_game():
    Game()
    game = Game()
    game.run()

def fade():
    running = True
    fade_alpha = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = True

        fade_surface = pygame.Surface((WIDHT,HEIGHT))
        fade_surface.fill((0,0,0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0,0))

        fade_alpha += 5
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
