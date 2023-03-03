import pygame

class userInterface:
    def __init__(self, surface):
        
        self.display_surface = surface
        self.health_bar = pygame.image.load('../Graphics/gameinterface/health.png').convert_alpha()
        #where the health bar starts in the top left
        self.health_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        self.coin = pygame.image.load('../Graphics/gameinterface/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (20, 75))
        self.text = pygame.font.Font('../Graphics/gameinterface/ARCADEPI.ttf', 30)

    def player_health(self, current_health, full_health):
        #displaying the health bar in the top left
        self.display_surface.blit(self.health_bar, (20,10))
        #checking how much of the health bar to fill depending on the player health
        player_health_ratio = current_health / full_health
        current_bar_width = self.bar_max_width * player_health_ratio
        health_bar_rect = pygame.Rect((self.health_bar_topleft), (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, 'red', health_bar_rect)

    def player_coins(self, no_of_coins):
        self.display_surface.blit(self.coin, self.coin_rect)
        no_of_coins_surface = self.text.render(str(no_of_coins), False, 'Black')
        no_of_coins_rect = no_of_coins_surface.get_rect(midleft = (self.coin_rect.right + 5, self.coin_rect.centery))
        self.display_surface.blit(no_of_coins_surface, no_of_coins_rect)