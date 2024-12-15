import pygame
import random
import numpy as np

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30

GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

TETROMINOS = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

class Tetromino:
    def __init__(self, shape=None, color=None, rotation=None, col=None):
        self.shape = shape if shape != None else random.choice(list(TETROMINOS.values()))
        self.rotation = rotation if rotation != None else 0
        if self.rotation:
            for _ in range(self.rotation):
                self.shape = [list(row) for row in zip(*self.shape[::-1])]
        self.rotation = rotation if rotation != None else random.randint(0, 3)
        self.x = col if col != None else GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.color = color if color != None else random.choice([RED, BLUE, GREEN, YELLOW])
        self.color_dark = [c // 2 for c in self.color]
        self.color_light = [(255 + c) // 2 for c in self.color]

    def get_all_rotations(self):
        rotations = []
        current_shape = self.shape
        for _ in range(4):
            current_shape = [list(row) for row in zip(*current_shape[::-1])]
            rotations.append(current_shape)
        return rotations

    def can_move_down(self, grid: list[list[int]]) -> bool:
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell != 0:
                    if self.y + y + 1 >= len(grid) or self.x + x >= len(grid[0]) or grid[self.y + y + 1][self.x + x] != BLACK:
                        return False
        return True

    def move_down(self, grid):
        if self.can_move_down(grid):
            self.y += 1
        else:
            for y, row in enumerate(self.shape):
                for x, cell in enumerate(row):
                    if cell:
                        grid[self.y + y][self.x + x] = WHITE
            return False
        return True

    def can_move_left(self, grid):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    if self.x + x - 1 < 0 or grid[self.y + y][self.x + x - 1] != BLACK:
                        return False
        return True

    def move_left(self, grid):
        if self.can_move_left(grid):
            self.x -= 1

    def can_move_right(self, grid):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    if self.x + x + 1 >= GRID_WIDTH or grid[self.y + y][self.x + x + 1] != BLACK:
                        return False
        return True

    def move_right(self, grid):
        if self.can_move_right(grid):
            self.x += 1

    def draw_cell(self, screen, x, y):
        pygame.draw.rect(
            screen,
            self.color,
            (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        )

    def draw_cell(self, screen, x, y, dx, dy):
        pygame.draw.rect(screen, self.color, (x, y, dx, dy))

        points = [(x, y), (x + dx, y), (x + 3*dx/4, y + dy/4), (x + dx/4, y + dy/4)]
        pygame.draw.polygon(screen, self.color_dark, points)
        points = [(x, y), (x + dx/4, y + dy/4), (x + dx/4, y + 3*dy/4), (x, y + dy)]
        pygame.draw.polygon(screen, self.color_dark, points)

        points = [(x + 3*dx/4, y + dy/4), (x + dx, y), (x + dx, y + dy), (x + 3*dx/4, y + 3*dy/4)]
        pygame.draw.polygon(screen, self.color_light, points)
        points = [(x + dx/4, y + 3*dy/4), (x + 3*dx/4, y + 3*dy/4), (x + dx, y + dy), (x, y + dy)]
        pygame.draw.polygon(screen, self.color_light, points)


    def draw(self, screen):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_cell(screen, self.x * BLOCK_SIZE + x * BLOCK_SIZE, self.y * BLOCK_SIZE + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)

    def draw_next(self, screen, x_offset, y_offset):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_cell(screen, x_offset + x * BLOCK_SIZE, y_offset + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)

    def rotate(self, grid):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        self.rotation = (self.rotation + 1) % 4


    def __str__(self):
        return f"Tetromino(shape={self.shape}, color={self.color}, rotation={self.rotation}, x={self.x}, y={self.y})"