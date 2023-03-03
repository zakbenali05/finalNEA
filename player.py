from turtle import update
import pygame
from importSupport import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, update_current_health):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.player_animations['Idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        #attributes to do with the movement of the player
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        #Setting the status of the player (where the player is in relation to the map)
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.update_current_health = update_current_health
        #making the player invincible for a short period when colliding with an enemy, to ensure the players health only decreases by the desired amount each collision
        self.invincible = False
        self.invincibility_duration = 600
        self.invincible_time = 0

    def import_character_assets(self):
        character_file_path = '../Graphics/character/'
        self.player_animations = {'Idle':[],'Run':[],'Jump':[],'Fall':[]}

        for animation in self.player_animations.keys():
            full_path = character_file_path + animation
            self.player_animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.player_animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
                
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        #choosing which animation to display depending on the characters position

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom= self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'Jump'
        elif self.direction.y > 1:
            self.status = 'Fall'
        else:
            if self.direction.x != 0:
                self.status = 'Run'
            else:
                self.status = 'Idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def get_damage(self):
        if not self.invincible:
            self.update_current_health(-20)
            self.invincible = True
            self.invincible_time = pygame.time.get_ticks()

    def invinciblity_timer(self):
        if self.invincible:
            #checking if the player has been invincible for the duration of their invincibility timer
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_time >= self.invincibility_duration:
                self.invincible = False

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.invinciblity_timer()