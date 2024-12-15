import pygame
import random

from Tetromino import Tetromino

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

    def is_game_over(self):
        for x in range(self.width):
            if self.grid[0][x] != BLACK:
                return True
        return False
    
    def calculate_points_grid(self):
        points = 0
        for y in range(self.height):
            points += sum(1 for cell in self.grid[y] if cell != BLACK)*(self.height - y)
            if y != 0:
                for x in range(self.width):
                    if (self.grid[y][x] == BLACK or self.grid[y][x] == 0) and y > 0 and self.grid[y-1][x] != BLACK:
                        points += 4
        return points

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
    
    def place_tetromino(self, tetromino: Tetromino):
        for r in range(len(tetromino.shape)):
            for c in range(len(tetromino.shape[0])):
                if tetromino.shape[r][c] != 0 and tetromino.shape[r][c] != BLACK:
                    if 0 <= tetromino.y + r < self.height and 0 <= tetromino.x + c < self.width:
                        self.grid[tetromino.y + r][tetromino.x + c] = tetromino.color

    def remove_tetromino(self, tetromino: Tetromino):
        for r in range(len(tetromino.shape)):
            for c in range(len(tetromino.shape[0])):
                if tetromino.shape[r][c] != 0:
                    if 0 <= tetromino.y + r < self.height and 0 <= tetromino.x + c < self.width:
                        self.grid[tetromino.y + r][tetromino.x + c] = BLACK

    def collides(self, tetromino, row, col):
        for r in range(len(tetromino)):
            for c in range(len(tetromino[0])):
                if tetromino[r][c] != 0:
                    if (row + r >= self.height or
                        col + c >= self.width or
                        col + c < 0 or
                        self.grid[row + r][col + c] != 0):
                        return True
        return False

    def console_display(self):
        for row in self.grid:
            print(''.join('#' if cell != BLACK else ' ' for cell in row))