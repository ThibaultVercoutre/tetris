import copy
import time

from Grid import Grid
from Tetromino import Tetromino

class Robot:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.all_positions: list[list[Tetromino]] = []
        self.path: list[str] = []

    def find_all_positions(self, grid: Grid, current_tetromino: Tetromino, next_tetromino: Tetromino):
        start_time = time.time()
        self.all_positions = []
        
        current_tetromino_rotations = [
            Tetromino(current_tetromino.shape, current_tetromino.color, rotation)
            for rotation in range(4)
        ]
        next_tetromino_rotations = [
            Tetromino(next_tetromino.shape, next_tetromino.color, rotation)
            for rotation in range(4)
        ]

        current_widths = [len(tetromino.shape[0]) for tetromino in current_tetromino_rotations]
        next_widths = [len(tetromino.shape[0]) for tetromino in next_tetromino_rotations]

        for rotation in range(4):
            for col in range(0, grid.width - current_widths[rotation] + 1):
                tetromino_rotation = Tetromino(current_tetromino.shape, current_tetromino.color, rotation, col)
                temp_grid = copy.deepcopy(grid)
                self.find_drop_position(temp_grid, tetromino_rotation)

                for rotation_2 in range(4):
                    for col in range(0, grid.width - next_widths[rotation] + 1):
                        tetromino_rotation_2 = Tetromino(next_tetromino.shape, next_tetromino.color, rotation_2, col)
                        temp_grid_2 = copy.deepcopy(temp_grid)
                        
                        temp_grid_2.place_tetromino(tetromino_rotation)
                        temp_grid_2.clear_full_lines()
                        self.find_drop_position(temp_grid_2, tetromino_rotation_2)

                        self.all_positions.append([tetromino_rotation, tetromino_rotation_2])
        print(f"Time find all positions: {time.time() - start_time}")

    def first_position(self) -> list[Tetromino]:
        first_position = self.all_positions.pop(0)
        self.all_positions.append(first_position)
        return first_position

    def find_best_position(self, grid: Grid, current_tetromino: Tetromino, next_tetronimo: Tetromino) -> Tetromino:
        self.find_all_positions(grid, current_tetromino, next_tetronimo)
        min_points = float('inf')
        best_position = None

        start_time = time.time()

        for tetromino in self.all_positions:
            temp_grid = copy.deepcopy(grid)
            temp_grid.place_tetromino(tetromino[0])
            temp_grid.clear_full_lines()
            temp_grid.place_tetromino(tetromino[1])
            temp_grid.clear_full_lines()
            points = temp_grid.calculate_points_grid()

            # print(f"Points: {points}")

            if points < min_points:
                min_points = points
                best_position = tetromino[0]

        print(f"Time find best position: {time.time() - start_time}")

        return best_position

    def find_drop_position(self, grid: Grid, tetromino: Tetromino):
        while tetromino.can_move_down(grid.grid):
            tetromino.move_down(grid.grid)
    
    def find_path_to_position(self, current_tetromino: Tetromino, target_row, target_col, target_rotation):
        if current_tetromino.y is None or target_row is None:
            raise ValueError("target_row and current_tetromino.y must be defined")
        if current_tetromino.x is None or target_col is None:
            raise ValueError("target_col and current_tetromino.x must be defined")
        if current_tetromino.rotation is None or target_rotation is None:
            raise ValueError("target_rotation and current_tetromino.rotation must be defined")

        path = []
        # Calculate the number of rotations needed
        rotations_needed = target_rotation
        path.extend(['rotate'] * rotations_needed)

        # Calculate the horizontal movements needed
        if current_tetromino.x > target_col:
            path.extend(['left'] * (current_tetromino.x - target_col))
        elif current_tetromino.x < target_col:
            path.extend(['right'] * (target_col - current_tetromino.x))

        self.path = path
    
    def get_path(self, grid, current_tetromino: Tetromino, next_tetromino: Tetromino):
        best_position = self.find_best_position(grid, current_tetromino, next_tetromino)
        if best_position:
            self.find_path_to_position(current_tetromino, best_position.y, best_position.x, best_position.rotation)
        print(self.path)

    def next_path(self):
        return self.path.pop(0) if self.path else None
    
    def run_path(self, tetromino: Tetromino, grid: Grid):
        move = self.next_path()
        if move == 'rotate':
            tetromino.rotate(grid.grid)
        elif move == 'left':
            tetromino.move_left(grid.grid)
        elif move == 'right':
            tetromino.move_right(grid.grid)
        elif move == 'down':
            tetromino.move_down(grid.grid)