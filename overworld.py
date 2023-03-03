import pygame
from gameData import allLevels

class Stage(pygame.sprite.Sprite):
    def __init__(self, position, status, icon_speed):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        if status == 'available':
            self.image.fill('red')
        else:
            self.image.fill('grey')
        self.rect = self.image.get_rect(center = position)

        #creating a detection box inside the stage, depending on the speed of the icon
        self.collision_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2), self.rect.centery - (icon_speed / 2), icon_speed, icon_speed)

#called it icon to not confuse it with the player class in the actual game. Icon is the player being controlled in the overworld
class Icon(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = pygame.Surface((20,20))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = position)

    def update(self):
        #ensures there is no offset between the icon position and the center of the rectangle
        self.rect.center = self.position

class Overworld:
    def __init__(self, start_level, max_level, surface, create_level):
        #setting up the overworld
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 10

        #sprites
        self.setup_stages()
        self.setup_icon()

    def setup_stages(self):
        self.stages = pygame.sprite.Group()

        #checking if the stage is unlocked based on whether the index of the current stage is less than the maximum level. 
        for index, stage_data in enumerate(allLevels.values()):
            if index <= self.max_level:
                stage_sprite = Stage(stage_data['stage_pos'], 'available', self.speed)
            else:
                stage_sprite = Stage(stage_data['stage_pos'], 'locked', self.speed)
            self.stages.add(stage_sprite)

    def draw_paths(self):
        #getting the position of the available levels, to place lines between them
        if self.max_level > 0:
            points = [stage['stage_pos'] for index, stage in enumerate(allLevels.values()) if index <= self.max_level]
            pygame.draw.lines(self.display_surface, 'green', False, points, 6)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.stages.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys [pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('before')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)


    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.stages.sprites()[self.current_level].rect.center)

        if target == "next":
            end = pygame.math.Vector2(self.stages.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.stages.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    def update_icon_position(self):
        if self.moving and self.move_direction:
            self.icon.sprite.position += self.move_direction * self.speed
            target_stage = self.stages.sprites()[self.current_level]
            if target_stage.collision_zone.collidepoint(self.icon.sprite.position):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def run(self):
        self.input()
        self.update_icon_position()
        self.icon.update()
        self.draw_paths()
        self.stages.draw(self.display_surface)
        self.icon.draw(self.display_surface)
