from settings import tile_no_vert, tile_size, screen_width
import pygame
from tiles import AnimateTile, StaticTile
from importSupport import import_folder
from random import choice, randint

class sky:
    #horizon is where we switch between the terrain tiles and the sky tiles
    def __init__(self, horizon):
        self.top = pygame.image.load('../Graphics/decoration/sky/sky_abovehorizon.png').convert()
        self.middle = pygame.image.load('../Graphics/decoration/sky/sky_athorizon.png').convert()
        self.bottom = pygame.image.load('../Graphics/decoration/sky/sky_belowhorizon.png').convert()
        self.horizon = horizon

        #stretching the tile all the way across the screen to create a screen effect
        self.top = pygame.transform.scale(self.top,(screen_width,tile_size))
        self.middle = pygame.transform.scale(self.middle,(screen_width,tile_size))
        self.bottom = pygame.transform.scale(self.bottom,(screen_width,tile_size))

    def draw(self, surface):
        for row in range(tile_no_vert):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top,(0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))

class clouds:
    def __init__(self, horizon, level_width, cloud_number):
        cloud_surf_list = import_folder('../Graphics/decoration/clouds')
        min_x = -screen_width
        min_y = 0
        max_x = level_width + screen_width
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(0, x, y, cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)

