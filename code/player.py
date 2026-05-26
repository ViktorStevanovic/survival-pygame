from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, collision_sprites, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(join(BASE_DIR, 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, 0)

        # movement
        self.player_direction = pygame.math.Vector2(0, 0)
        self.player_speed = PLAYER_SPEED

        # collision
        self.collision_sprites = collision_sprites
    
    def input(self):
        keys = pygame.key.get_pressed()
        self.player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction

    def move(self, dt):
        self.hitbox_rect.x += self.player_direction.x * self.player_speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.player_direction.y * self.player_speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.player_direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.player_direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.player_direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.player_direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom


    def update(self, dt):
        self.input()
        self.move(dt)