import pygame
import sprites


class GameWindow(object):
    width: int
    height: int
    upd_freq: int
    main_loop_active: bool

    def __init__(self, width=1200, height=800, upd_freq=30):
        pygame.init()
        self.width = width
        self.height = height
        self.upd_freq = upd_freq
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.sprite_list = pygame.sprite.Group()
        pygame.display.set_caption("Jora's animation")

        tree = sprites.Tree(height)
        self.sprite_list.add(tree)
        head = sprites.Head(height, 150)
        self.sprite_list.add(head)

    def render(self):
        self.screen.fill((60, 60, 150))
        self.sprite_list.draw(self.screen)
        pygame.display.flip()

    def main_loop(self):
        self.main_loop_active = True

        while self.main_loop_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_loop_active = False

            self.sprite_list.update()
            self.render()
            self.clock.tick(self.upd_freq)


if __name__ == "__main__":
    gameWindow = GameWindow()
    gameWindow.main_loop()
