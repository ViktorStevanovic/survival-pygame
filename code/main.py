from settings import *
from player import Player
from sprites import CollisionSprite
from random import randint

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

        self.player = Player((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), self.collision_sprites, self.all_sprites)

        for i in range(6):
            x, y = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
            w, h = randint(60, 200), randint(60, 100)  
            CollisionSprite((x, y), (w, h), (self.all_sprites, self.collision_sprites))

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