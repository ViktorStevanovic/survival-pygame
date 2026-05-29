from settings import *
from player import Player
from enemy import Enemy
from sprites import CollisionSprite, Sprite, Gun, Bullet
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game():
    def __init__(self) -> None:
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.display.set_caption('Survival')

        fullscreen_mode = False

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED, vsync=1)
        self.running = True
        self.clock = pygame.time.Clock()
        
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        # spawn locations
        self.enemy_spawn_points = []

        self.setup()

    def input(self):
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()

        if mouse_keys[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(pos, self.bullet_image, self.gun.player_direction, self.all_sprites, self.bullet_sprites)
            self.shoot_sound.play()
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if pygame.time.get_ticks() - self.shoot_time >= self.gun_cooldown:
            self.shoot_time = 0
            self.can_shoot = True

    def load_images(self):
        self.bullet_image = pygame.image.load(join(BASE_DIR, 'images', 'gun', 'bullet.png'))
        self.bullet_image = pygame.transform.scale(self.bullet_image, (self.bullet_image.width / 2, self.bullet_image.height / 2))

        self.enemy_frames = {'bat': [], 'skeleton': [], 'blob': []}

        for monster in self.enemy_frames.keys():
            for folder_path, sub_folders, file_names in walk(join(BASE_DIR, 'images', 'enemies', monster)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split(".")[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.enemy_frames[monster].append(surf)

    def setup(self):
        # load images
        self.load_images()

        # load sounds
        self.impact_sound = pygame.mixer.Sound(join(BASE_DIR, 'audio', 'impact.ogg'))
        self.game_music = pygame.mixer.music.load(join(BASE_DIR, 'audio', 'music.wav'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # -1 = loop

        self.shoot_sound = pygame.mixer.Sound(join(BASE_DIR, 'audio', 'shoot.wav'))
        self.shoot_sound.set_volume(1)

        # custom event
        self.spawn_enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.spawn_enemy_event, 1000)

        # create entities
        map = load_pygame(join(BASE_DIR, 'data', 'maps', 'world.tmx'))
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, self.all_sprites, self.collision_sprites)

        for col in map.get_layer_by_name('Collisions'):
            col_surf = pygame.Surface((col.width, col.height)).convert_alpha()
            CollisionSprite((col.x, col.y), col_surf, self.collision_sprites)

        for ent in map.get_layer_by_name('Entities'):
            if ent.name == 'Player':
                self.player = Player((ent.x, ent.y), self.collision_sprites, self.all_sprites)
                self.gun = Gun(self.player, self.all_sprites)

            if ent.name == 'Enemy':
                self.enemy_spawn_points.append((ent.x, ent.y))

        
    def spawn_enemy(self):
        enemy_type = list(self.enemy_frames)[randint(0, (len(self.enemy_frames) - 1))]
        spawn_pos = self.enemy_spawn_points[randint(0, (len(self.enemy_spawn_points) - 1))]

        Enemy(spawn_pos, self.enemy_frames[enemy_type], self.player, self.collision_sprites, self.enemy_sprites, self.all_sprites)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == self.spawn_enemy_event:
                    self.spawn_enemy()
                
            self.gun_timer()
            self.input()

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw_custom(self.player.rect.center)

            bullets = self.bullet_sprites.sprites()
            for bullet in bullets:
                if pygame.sprite.spritecollide(bullet, self.enemy_sprites, True, pygame.sprite.collide_mask):
                    self.impact_sound.play()
                    bullet.kill()

            # game over
            if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
                self.running = False

            pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()