import pygame
from tiles import AnimateTile
from random import randint

class Enemy(AnimateTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, '../Graphics/enemy/run')
        self.speed = randint(1, 3)

    def move(self):
        self.rect.x += self.speed

    #changing the direction of the enemy when it hits a wall.
    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    #overriding update method inherited from AnimateTile
    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()