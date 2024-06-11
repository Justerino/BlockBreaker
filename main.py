import pygame
import sys
from game import Game
from colors import Colors

# initialize pygame
pygame.init()

# set font style and surfaces for fonts
title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

# create background rects for UI elements
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

# set screen dimensions and title
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Tetris in Python")

# set clock variable
clock = pygame.time.Clock()

# create instance of game class
game = Game()

# create event to control game speed
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)


# main function
def main():
    # game loop
    while True:
        # check for events
        for event in pygame.event.get():
            # exit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # check if player pushed key
            if event.type == pygame.KEYDOWN :
                # if game is over and paused, any key press starts new game
                if game.game_over:
                    game.game_over = False
                    game.reset()

                # checks for left, right, down and up arrow key inputs
                if event.key == pygame.K_LEFT and (not game.game_over):
                    game.move_left()
                if event.key == pygame.K_RIGHT and (not game.game_over):
                    game.move_right()
                if event.key == pygame.K_DOWN and (not game.game_over):
                    game.move_down()
                    game.update_score(0, 1)
                if event.key == pygame.K_UP and (not game.game_over):
                    game.rotate()

            # automatically moves pieces down over time
            if event.type == GAME_UPDATE and (not game.game_over):
                game.move_down()

        # Drawing
        # score has to be rendered during loop
        score_value_surface = title_font.render(str(game.score), True, Colors.white)
        # sets background color
        screen.fill(Colors.dark_blue)
        # draws score UI
        screen.blit(score_surface, (365, 20, 50, 50))
        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,
                                                                      centery=score_rect.centery))

        # draws next piece UI
        screen.blit(next_surface, (375, 180, 50, 50))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)

        # if game over is true displays game over text
        if game.game_over:
            screen.blit(game_over_surface, (320, 450, 50, 50))

        # draws main tetris grid + pieces
        game.draw(screen)

        # updates display per iteration
        pygame.display.update()
        # limits FPS to 60
        clock.tick(60)


# run the main function only if this module is executed as the main script
if __name__ == "__main__":
    # call the main function
    main()
