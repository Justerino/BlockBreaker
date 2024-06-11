import pygame
import random
from grid import Grid
from blocks import *

# Game class controls most game functions such as moving the piece, updating the score, playing the sounds,
# drawing the grid/pieces and other similar functions
class Game:
    # initializes with any variables needed
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.mp3")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.wav")

        pygame.mixer.music.load("Sounds/BGM.wav")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    # function to update score and calculate score based on how many lines cleared at once
    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared >= 3:
            self.score += 500
        self.score += move_down_points

    # gets the next random block, ensuring 1 of each type of block per set is produced with no duplicates
    # and resetting list if empty
    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)

        return block

    # function to check if block can move left
    def move_left(self):
        # move left
        self.current_block.move(0, -1)
        # if move was not possible
        if (not self.block_inside()) or (not self.block_fits()):
            # undo move
            self.current_block.move(0, 1)

    # function to check if block can move right
    def move_right(self):
        # move right
        self.current_block.move(0, 1)
        # if move was not possible
        if (not self.block_inside()) or (not self.block_fits()):
            # undo move
            self.current_block.move(0, -1)

    # function to move block down
    def move_down(self):
        # move down
        self.current_block.move(1, 0)
        # if move not possible or bottom of grid
        if self.block_inside() == False or self.block_fits() == False:
            # undo move
            self.current_block.move(-1, 0)
            # lock the block in place after the undo
            self.lock_block()

    # function to lock block in place
    def lock_block(self):
        # get all the tiles of the current block
        tiles = self.current_block.get_cell_positions()
        # iterate through all the tiles of that block
        for position in tiles:
            # assign tiles of that block to the grid
            self.grid.grid[position.row][position.column] = self.current_block.id
        # generate new current and next block
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        # clear rows if any were made from locked block
        rows_cleared = self.grid.clear_full_rows()
        # if rows were cleared assign points and play sound
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        # if the block did not fit, game over
        if not self.block_fits():
            self.game_over = True

    # function to reset game
    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    # function to check is block is inside another piece
    def block_fits(self):
        # get all piece locations
        tiles = self.current_block.get_cell_positions()
        # iterate for each tile where piece is
        for tile in tiles:
            # if tile is not empty
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        # else tile is empty
        return True

    # function to rotate blocks clockwise
    def rotate(self):
        # calls function in block.py to rotate piece
        self.current_block.rotate()
        # if rotation is not possible
        if (not self.block_inside()) or (not self.block_fits()):
            # call undo rotation function
            self.current_block.undo_rotation()
        # if rotation is possible
        else:
            # keep rotation and play sound
            self.rotate_sound.play()

    # function to check if block is within grid boundaries
    def block_inside(self):
        # get all piece locations
        tiles = self.current_block.get_cell_positions()
        # iterate for each tile where piece is
        for tile in tiles:
            # if no tiles are out of bounds
            if not self.grid.is_inside(tile.row, tile.column):
                # allow placement
                return False
        # tile is out of bounds
        return True

    # function to draw blocks
    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        # IBlock offset
        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        # OBlock offset
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        # All other blocks
        else:
            self.next_block.draw(screen, 270, 270)
