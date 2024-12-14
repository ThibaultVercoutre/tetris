import pygame
import random
from typing import List

from Tetromino import Tetromino
from Grid import Grid

# Paramètres de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT, BAR_WIDTH = 300, 600, 200
BLOCK_SIZE = 30

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Créer la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH + BAR_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Horloge pour contrôler le framerate
clock = pygame.time.Clock()

# Grille de Tetris (10 x 20 cases)
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

def calculate_points(lines_cleared):
    if lines_cleared == 1:
        return 40
    elif lines_cleared == 2:
        return 100
    elif lines_cleared == 3:
        return 300
    elif lines_cleared == 4:
        return 1200
    return 0

# Boucle principale du jeu
def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH + 200, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    font = pygame.font.SysFont('Arial', 25)

    running = True
    grid = Grid(GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE)
    current_tetromino = Tetromino()
    next_tetromino = Tetromino()
    clock = pygame.time.Clock()
    fall_time = 0
    points = 0

    while running:
        fall_speed = 0.5  # Vitesse de chute en secondes
        fall_time += clock.get_rawtime()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.move_left(grid.grid)
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.move_right(grid.grid)
                elif event.key == pygame.K_DOWN:
                    current_tetromino.move_down(grid.grid)
                elif event.key == pygame.K_UP:
                    current_tetromino.rotate()

        if fall_time / 1000 >= fall_speed:
            if not current_tetromino.move_down(grid.grid):
                for y, row in enumerate(current_tetromino.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            grid.grid[current_tetromino.y + y][current_tetromino.x + x] = current_tetromino.color
                lines_cleared = grid.clear_full_lines()
                points += calculate_points(lines_cleared)
                current_tetromino = next_tetromino
                next_tetromino = Tetromino()
            fall_time = 0

        screen.fill(BLACK)
        grid.draw(screen)
        current_tetromino.draw(screen)
        next_tetromino.draw_next(screen, SCREEN_WIDTH + 20, 100)

        # Afficher les points
        points_text = font.render(f"Points: {points}", True, WHITE)
        screen.blit(points_text, (SCREEN_WIDTH + 20, 20))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()