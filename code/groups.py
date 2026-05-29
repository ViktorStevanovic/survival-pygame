from imports import *

class AllSprites(pygame.sprite.Group):
    def __init__(self, settings, *sprites):
        super().__init__(*sprites)
        self.settings = settings
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw_custom(self, target_pos):
        self.offset.x = -(target_pos[0] - self.settings.window_width / 2)
        self.offset.y = -(target_pos[1] - self.settings.window_height / 2)

        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if hasattr(sprite, 'object')]
        bullet_sprites = [sprite for sprite in self if hasattr(sprite, 'bullet')]


        for layer in [ground_sprites, object_sprites, bullet_sprites]:
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
            