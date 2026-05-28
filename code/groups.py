from pygame import Surface
from pygame.rect import FRect, Rect

from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw_custom(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if hasattr(sprite, 'object')]
        bullet_sprites = [sprite for sprite in self if hasattr(sprite, 'bullet')]


        for layer in [ground_sprites, object_sprites, bullet_sprites]:
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
            