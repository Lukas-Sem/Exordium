import pygame

class SpriteSheet :
    def __init__(self,sheet):
        self.sheet = sheet
        self.sprite_sheet=pygame.image.load(sheet).convert_alpha()

    def get_image(self, x, y, width, height, colour):
        sprite = pygame.Surface((width, height)).convert_alpha()
        sprite.blit(self.sprite_sheet, (0,0), (x, y, width, height))
        sprite = pygame.transform.scale(sprite, (width * 1.5, height * 1.5))

        sprite.set_colorkey(colour)

        return sprite