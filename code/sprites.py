from typing import Any
from imports import *
from math import atan2, degrees

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)

        # settings
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)

        # settings
        self.object = True
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, settings, player, *groups):
        super().__init__(*groups)
        # settings
        self.object = True
        self.settings = settings
        self.player = player
        self.distance = 100
        self.player_direction = pygame.Vector2(0, 1)

        # sprite setup
        self.gun_surf = pygame.image.load(join(BASE_DIR, 'images', 'gun', 'gun.png')).convert_alpha()
        self.gun_surf = pygame.transform.scale(self.gun_surf, (self.gun_surf.width / 2, self.gun_surf.height / 2))
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

        # shooting
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

    def get_direction(self):
        mouse_point = pygame.Vector2(pygame.mouse.get_pos())
        player_point = pygame.Vector2(self.settings.window_width / 2, self.settings.window_height / 2)
        self.player_direction = (mouse_point - player_point).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)
        
    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, image, direction, *groups):
        super().__init__(*groups)

        # settings
        self.bullet = True
        self.image = image
        self.rect = self.image.get_frect(center = pos)

        # movement
        self.direction = direction
        self.speed = 1200

        # attributes
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if pygame.time.get_ticks() - self.spawn_time > 2000:
            self.kill()