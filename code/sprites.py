from typing import Any

from settings import *

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface(size)
        self.image.fill("#805B91")
        self.rect = self.image.get_frect(center = pos)