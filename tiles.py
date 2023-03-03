import pygame 
from importSupport import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x, y))

    #This method scrolls the screen
    def update(self, shift):
        self.rect.x += shift

#Inheriting common attributes from main class for all the other tile classes(e.g: coins tiles and so on)
class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class AnimateTile(Tile):
    def __init__(self,size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift

#centering the coin so it doesn't spin in the top left of the tile
class Coin(AnimateTile):
    def __init__(self, size, x, y, path):
        super().__init__(size,x,y,path)
        #places coin starting point in the centre of the tile
        center_x = x + int(size/2)
        center_y = y + int(size/2)
        self.rect = self.image.get_rect(center = (center_x, center_y))