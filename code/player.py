from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(join(BASE_DIR, 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)

        # movement
        self.player_direction = pygame.math.Vector2(0, 0)
        self.player_speed = PLAYER_SPEED

        # collision
        self.mask = pygame.mask.from_surface(self.image)
    
    def input(self):
        keys = pygame.key.get_pressed()
        self.player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction

    def move(self, dt):
        self.rect.center += self.player_direction * self.player_speed * dt


    def update(self, dt):
        self.input()
        self.move(dt)