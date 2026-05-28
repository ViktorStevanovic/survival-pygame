from settings import *
from player import Player
from sprites import CollisionSprite, Sprite
from random import randint
from pytmx.util_pygame import load_pygame
 
class Game():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Survival')

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED, vsync=1)
        self.running = True
        self.clock = pygame.time.Clock()
        
        # groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

        self.player = Player((200, 200), self.collision_sprites, self.all_sprites)

    
    def setup(self):
        map = load_pygame(join(BASE_DIR, 'data', 'maps', 'world.tmx'))
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, self.all_sprites, self.collision_sprites)

        for col in map.get_layer_by_name('Collisions'):
            col_surf = pygame.Surface((col.width, col.height)).convert_alpha()
            CollisionSprite((col.x, col.y), col_surf, self.collision_sprites)



    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()