from colors import Colors
import pygame
from position import Position


# This class is inherited by all the blocks and provides basic functions to move, identify positions, and draw
class Block:
    # initializes with any variables needed
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

    # function to move the block by adding a row and col value to their location
    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    # function to get all the positions of the block
    def get_cell_positions(self):
        # gets all the tiles occupied in the current rotation state
        tiles = self.cells[self.rotation_state]
        # create empty list for positions
        moved_tiles = []
        # iterates through each tile
        for position in tiles:
            # assigns an x and y coordinate
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            # adds coordinate to list
            moved_tiles.append(position)

        # returns coordinates for all tiles
        return moved_tiles

    # function to rotate block clockwise
    def rotate(self):
        # changes to the next index in the dict for next position stored
        self.rotation_state += 1
        # if no more positions after current index
        if self.rotation_state == len(self.cells):
            # reset back to first index
            self.rotation_state = 0

    # function to undo a rotation is move was not possible
    def undo_rotation(self):
        # reverts rotation state
        self.rotation_state -= 1
        # if was at first index
        if self.rotation_state == 0:
            # resets back to last index
            self.rotation_state = len(self.cells) - 1

    # function to draw all the tiles in the block
    def draw(self, screen, offset_x, offset_y):
        # creates list of each tile
        tiles = self.get_cell_positions()
        # iterates through all tiles
        for tile in tiles:
            # draws each tile with a provided offset to fit into grid and have a border
            tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size,
                                    offset_y + tile.row * self.cell_size,
                                    self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)
