import pygame
from colors import Colors


# class to create the grid where blocks are placed and have functions to check if location in grid is occupied
class Grid:
    # initializes the variables needed
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    # function to return bool and check if location is within grid boundaries
    def is_inside(self, row, column):
        if 0 <= row < self.num_rows and 0 <= column < self.num_cols:
            return True
        return False

    # function to check is location is empty
    def is_empty(self, row, column):
        # checks if location == 0 (no ID value inside)
        if self.grid[row][column] == 0:
            return True
        return False

    # function to check if row is full match
    def is_row_full(self, row):
        # iterates for each column in the row
        for column in range(self.num_cols):
            # if the square is empty
            if self.grid[row][column] == 0:
                # row is not complete
                return False
        # row is complete
        return True

    # function to empty a row
    def clear_row(self, row):
        # iterates for each column in the row
        for column in range(self.num_cols):
            # sets the square to 0 (empty)
            self.grid[row][column] = 0

    # function to move row down after clearing row below it
    def move_row_down(self, row, num_rows):
        # iterates for each column in the row
        for column in range(self.num_cols):
            # moves row down 1 and clears where row previously was
            self.grid[row + num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    # function to clear a row specifically after completing row with blocks
    def clear_full_rows(self):
        # variable to track how many rows were cleared for points
        completed = 0
        # iterates for each row cleared
        for row in range(self.num_rows - 1, 0, -1):
            # checks if row was full
            if self.is_row_full(row):
                # clears row
                self.clear_row(row)
                # adds one to completed row count
                completed += 1
            # else no rows were completed so not cleared
            elif completed > 0:
                # move the row down
                self.move_row_down(row, completed)
        # returns amount of completed rows
        return completed

    # function to reset the entire grid
    def reset(self):
        # iterates for each row in the grid
        for row in range(self.num_rows):
            # iterates for each column in the grid
            for column in range(self.num_cols):
                # sets value to 0
                self.grid[row][column] = 0

    # function to draw the grid
    def draw(self, screen):
        # iterates for each row in the grid
        for row in range(self.num_rows):
            # iterates for each column in the grid
            for column in range(self.num_cols):
                # gets the cell value of each square
                cell_value = self.grid[row][column]
                # draws the rect in the cell based on what ID value inside the cell
                cell_rect = pygame.Rect(column*self.cell_size + 11, row*self.cell_size + 11,
                                        self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
