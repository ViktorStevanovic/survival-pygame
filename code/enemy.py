from typing import Any

from imports import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, player, settings, collision_sprites, *groups):
        super().__init__(*groups)
        # animation
        self.frames = frames
        self.frame_index = 0
        
        # settings
        self.object = True
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -60)
        self.settings = settings

        # attributes
        self.player = player
        self.speed = self.settings.enemy_speed

        # movement
        self.collision_sprites = collision_sprites
        self.direction = pygame.math.Vector2(0, 0)

    def move(self, dt):
        enemy_point = pygame.Vector2(self.rect.centerx, self.rect.centery)
        player_point = pygame.Vector2(self.player.rect.centerx, self.player.rect.centery)

        # move towards the player position
        self.direction = (player_point - enemy_point)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        if self.direction.length() > 0:
            self.hitbox_rect.x += self.direction.x * self.speed * dt
            self.collision('horizontal')
            self.hitbox_rect.y += self.direction.y * self.speed * dt
            self.collision('vertical')
            self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom

    def animate(self, dt):
        self.frame_index += 5 * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self, dt):
        self.move(dt)
        self.animate(dt)