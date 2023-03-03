from csv import reader
from settings import tile_size
from os import walk
import pygame

def import_folder(path):
    surface_list = []

    #walk returns 3 parameters to do with the path sourced. We only want the list of images to loop over them
    for _, __, img_files in walk(path):
        #instead of manually adding each coin frame, we loop through all of the coin images
        for image in img_files:
            full_path = path + '/' + image
            img_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(img_surface)

    return surface_list

def import_csv_layout(file_path):
    map_base_map = []
    with open(file_path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            map_base_map.append(list(row))
        return map_base_map

def import_cut_graphic(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_number_x = int(surface.get_size()[0]/tile_size)
    tile_number_y = int(surface.get_size()[1]/tile_size)

    #Getting the current position on the tile we are in
    cut_tiles = []
    for row in range(tile_number_y):
        for column in range(tile_number_x):
            x = column * tile_size
            y = row * tile_size
            new_surface = pygame.Surface((tile_size, tile_size), flags = pygame.SRCALPHA)
            #Selecting the first slice of the tile by getting the top left position of the tile
            #This gets blitted onto a new surface
            new_surface.blit(surface,(0,0),pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surface)
    
    return cut_tiles