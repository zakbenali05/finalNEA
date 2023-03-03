import pygame
from importSupport import import_csv_layout, import_cut_graphic
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Coin
from enemy import Enemy 
from decorations import sky, clouds
from player import Player
from gameData import allLevels
from enemyEffect import EnemyEffect
from random import randint

class Level:
    def __init__(self, current_level, surface, create_overworld, update_coins, update_current_health):
        #Setting up the screen
        self.display_surface = surface
        self.screen_shift = 0

        #connecting the overworld with the current level selected
        self.current_level = current_level
        level_data = allLevels[current_level]
        self.new_max_level = level_data['unlock']
        self.create_overworld = create_overworld

        #setting the player on the screen
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_initiate(player_layout, update_current_health)

        #game interface
        self.update_coins = update_coins

        #enemy death sprite group
        self.death_sprites = pygame.sprite.Group()

        #Setting up the ground/base of the map
        map_base = import_csv_layout(level_data['mapBase'])
        self.map_base_sprites = self.create_tile_group(map_base, 'mapBase')

        #setting up the coins on the map base/ground
        coin_layout = import_csv_layout(level_data['mapCoins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'mapCoins')

        #setting up the enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        #setting the boundaries the enemy has to stay in
        boundary_layout = import_csv_layout(level_data['boundaries'])
        self.boundary_sprites = self.create_tile_group(boundary_layout, 'boundary')
       
        #setting up the sky background and the water at the bottom
        self.sky = sky(8)
        level_width = len(map_base[0] * tile_size)
        self.clouds = clouds(400, level_width, 40)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                if value != '-1':
                    x = column_index * tile_size
                    y = row_index * tile_size

                    #List of all of the tiles corresponding to the map base/background
                    if type == 'mapBase':
                        mapBase_tile_list = import_cut_graphic('../Graphics/level_terrain/platformer_tiles.png')
                        tile_surface = mapBase_tile_list[int(value)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

                    if type == 'mapCoins':
                        sprite = Coin(tile_size, x, y, '../Graphics/coins/gold')

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'boundary':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def enemy_collision(self):
        #cycling through the enemy sprites placed on the map
        for enemy in self.enemy_sprites.sprites():
            #checking if the enemy collides with the boundaries(these boundaries can't be seen as they haven't been drawn)
            if pygame.sprite.spritecollide(enemy, self.boundary_sprites, False):
                enemy.reverse()

    def player_initiate(self, layout, update_current_health):
        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if value == '0':
                    sprite = Player((x,y), self.display_surface, update_current_health)
                    self.player.add(sprite)
                if value == '1':
                    key_surf = pygame.image.load('../Graphics/character/key_endgoal.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, key_surf)
                    self.goal.add(sprite)

    def horizontal_collide(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.map_base_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_collide(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.map_base_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction. y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def scroll_x_direction(self):
        player = self.player.sprite
        player_x_direction = player.rect.centerx
        direction_x = player.direction.x
        
        #if the player gets close to either side of the screen, the screen starts scrolling
        if player_x_direction < screen_width/4 and direction_x < 0:
            self.screen_shift = 8
            player.speed = 0
        elif player_x_direction > screen_width - (screen_width/4) and direction_x > 0:
            self.screen_shift = -8
            player.speed = 0
        #if the player is in the middle of the map, the screen doesn't scroll
        else:
            self.screen_shift = 0
            player.speed = 8

    def check_player_died(self):
        #checks if the player falls off the map, and resets them to the overworld if so
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    def check_player_win(self):
        #checks if the player reaches the end key, and resets them to the overworld with a new level unlocked if so
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def player_coin_collisions(self):
        #True, as we want to destroy the coin after collision
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            for coin in collided_coins:
                self.update_coins(randint(1,5))

    def player_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom 

                #checks if the bottom of the player touches the enemy within the range of the top half of the enemy, and that they fall directly on top of the enemy
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    #whenever an enemy is destroyed, the player jumps up
                    self.player.sprite.direction.y = -10
                    death_sprite = EnemyEffect(enemy.rect.center, 'death')
                    self.death_sprites.add(death_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def run(self):
        #adds the sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.screen_shift)

        #runs the level
        self.map_base_sprites.draw(self.display_surface)
        self.map_base_sprites.update(self.screen_shift)

        #sets the enemies
        self.enemy_sprites.update(self.screen_shift)
        self.boundary_sprites.update(self.screen_shift)
        self.enemy_collision()
        self.enemy_sprites.draw(self.display_surface)
        self.death_sprites.update(self.screen_shift)
        self.death_sprites.draw(self.display_surface)

        #adds the coins
        self.coin_sprites.update(self.screen_shift)
        self.coin_sprites.draw(self.display_surface)

        #adds the player sprite and player start/end point
        self.player.update()
        self.horizontal_collide()
        self.vertical_collide()
        self.scroll_x_direction()
        self.player.draw(self.display_surface)
        self.goal.update(self.screen_shift)
        self.goal.draw(self.display_surface)

        self.check_player_died()
        self.check_player_win()

        self.player_coin_collisions()
        self.player_enemy_collisions()
        