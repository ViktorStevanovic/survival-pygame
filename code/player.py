from imports import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, collision_sprites, *groups):
        super().__init__(*groups)
        self.object = True

        self.load_images()

        self.image = pygame.image.load(join(BASE_DIR, 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)

        # movement
        self.player_direction = pygame.math.Vector2(0, 0)
        self.player_speed = 500

        # animation
        self.frame_index = 0
        self.state = 'left'

        # collision
        self.collision_sprites = collision_sprites


    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join(BASE_DIR, 'images', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split(".")[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        self.player_direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        self.player_direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction

    def move(self, dt):
        self.hitbox_rect.x += self.player_direction.x * self.player_speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.player_direction.y * self.player_speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def animate(self, dt):
        # get state
        if self.player_direction.x != 0:
            if self.player_direction.x > 0:
                self.state = 'right'
            else:
                self.state = 'left'
        if self.player_direction.y != 0:
            if self.player_direction.y > 0:
                self.state = 'down'
            else:
                self.state = 'up'
                
        if self.player_direction == (0, 0):
            self.frame_index = 0
        
        # animate
        self.frame_index += 5 * dt
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

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
        self.animate(dt)