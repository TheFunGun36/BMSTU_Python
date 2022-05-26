import pygame
import os


class Tree(pygame.sprite.Sprite):
    def __init__(self, window_size_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', 'tree.png'))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (-800, window_size_y)


class Head(pygame.sprite.Sprite):
    def __init__(self, window_size_y, tree_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', 'head.png'))
        self.saved_image = pygame.image.load(os.path.join('images', 'head.png'))
        self.rect = self.image.get_rect()
        self.rect.center = (1000, window_size_y - 500)
        self.initial_velocity = 5
        self.tree_pos = tree_pos
        self.y_initial = self.rect.y
        self.counter = 0

    def update(self, *args, **kwargs) -> None:
        if self.rect.left > self.tree_pos:
            self.rect.x -= 15  # 30
            rect_saved = self.rect.copy()
            self.image = pygame.transform.rotate(self.saved_image, self.counter)
            self.rect.center = center_saved
            self.counter += 7  # 14.5
        elif self.rect.y - self.y_initial < 50:
            self.rect.y += 1


import pygame

pygame.init()
FPS = 30
RED = (200, 0, 0)
GREY = (100, 100, 100)
BLUE = (0, 0, 200)

clock = pygame.time.Clock()

display = pygame.display.set_mode((640, 480))
display.fill(GREY)
rocketImg = pygame.Surface((360, 400), pygame.SRCALPHA)

pygame.draw.polygon(rocketImg, BLUE, ((250, 150), (250, 200), (300, 175)))
pygame.draw.rect(rocketImg, BLUE, (150, 150, 100, 50))
pygame.draw.rect(rocketImg, BLUE, (50, 150, 100, 50))

spriteImg = rocketImg
spriteRect = rocketImg.get_rect()
spriteRect.center = (320, 240)

i = 0
run = True
h1, h2, h3 = 0, 0, 0
speed = 1

while run:
    clock.tick(FPS)

    display.fill(GREY)
    display.blit(spriteImg, (120, 0))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if i < 90:
        spriteImg = pygame.transform.rotate(rocketImg, i)
        spriteRect = spriteImg.get_rect()
        spriteRect.center = (320, 240)
    else:
        spriteImg = pygame.transform.rotate(rocketImg, 90)
        spriteImg = pygame.transform.scale(spriteImg, (480, 560))
        rocketImg.fill((0, 0, 0, 0))
        pygame.draw.polygon(rocketImg, BLUE, ((250 + h1, 150), (250 + h1, 200), (300 + h1, 175)))
        pygame.draw.rect(rocketImg, BLUE, (150 + h2, 150, 100, 50))
        pygame.draw.rect(rocketImg, BLUE, (50 + h3, 150, 100, 50))

    if i >= 90:
        h1 = (i - 90) * speed

    if i > 120:
        h3 = (i - 90) - (i - 120) ** 2
        speed = 2
    else:
        h3 = h1

    if i > 150:
        h2 = (i - 90) - (i - 150) ** 2
        speed = 3
    else:
        h2 = h1

    i += 1

pygame.quit()
