import pygame
import random

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Définir les couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Grid:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.grid = [[BLACK for _ in range(width)] for _ in range(height)]

    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(
                    screen, 
                    WHITE, 
                    (x * self.block_size, y * self.block_size, self.block_size, self.block_size),
                    1
                )
                if self.grid[y][x] != BLACK:
                    pygame.draw.rect(screen, self.grid[y][x], (x * self.block_size, y * self.block_size, self.block_size, self.block_size))

                    color_dark = tuple(max(c - 50, 0) for c in self.grid[y][x])
                    color_light = tuple(min(c + 50, 255) for c in self.grid[y][x])

                    points = [(x * self.block_size, y * self.block_size), (x * self.block_size + self.block_size, y * self.block_size), 
                              (x * self.block_size + 3 * self.block_size / 4, y * self.block_size + self.block_size / 4), 
                              (x * self.block_size + self.block_size / 4, y * self.block_size + self.block_size / 4)]
                    pygame.draw.polygon(screen, color_dark, points)
                    
                    points = [(x * self.block_size, y * self.block_size), (x * self.block_size + self.block_size / 4, y * self.block_size + self.block_size / 4), 
                              (x * self.block_size + self.block_size / 4, y * self.block_size + 3 * self.block_size / 4), 
                              (x * self.block_size, y * self.block_size + self.block_size)]
                    pygame.draw.polygon(screen, color_dark, points)

                    points = [(x * self.block_size + 3 * self.block_size / 4, y * self.block_size + self.block_size / 4), 
                              (x * self.block_size + self.block_size, y * self.block_size), 
                              (x * self.block_size + self.block_size, y * self.block_size + self.block_size), 
                              (x * self.block_size + 3 * self.block_size / 4, y * self.block_size + 3 * self.block_size / 4)]
                    pygame.draw.polygon(screen, color_light, points)
                    
                    points = [(x * self.block_size + self.block_size / 4, y * self.block_size + 3 * self.block_size / 4), 
                              (x * self.block_size + 3 * self.block_size / 4, y * self.block_size + 3 * self.block_size / 4), 
                              (x * self.block_size + self.block_size, y * self.block_size + self.block_size), 
                              (x * self.block_size, y * self.block_size + self.block_size)]
                    pygame.draw.polygon(screen, color_light, points)

    def clear_full_lines(self):
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        lines_cleared = self.height - len(new_grid)
        self.grid = [[BLACK for _ in range(self.width)] for _ in range(lines_cleared)] + new_grid
        return lines_cleared
