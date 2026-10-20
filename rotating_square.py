import pygame
WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Cube(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.Surface((80, 80), pygame.SRCALPHA)
        self.original_image.fill((0, 0, 0))
        pygame.draw.rect(self.original_image, "red", (35,0,10,10))

        self.image = self.original_image
        self.rect = self.original_image.get_rect(center=(x, y))
        self.angle = 0

    def update(self):
        print(self.angle)
        self.angle += 0.1   # spin; delete this line to keep it fixed at 45°
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        pygame.draw.rect(screen,"red",self.rect,2) #rect of spike


cube_group = pygame.sprite.Group()
cube = Cube(400,300)
cube_group.add(cube)

running = True
while running:
    clock.tick(60)

    screen.fill((255,255,255))
    cube_group.update()
    cube_group.draw(screen)

    #pygame.draw.rect(screen,"blue",cube.rect,2) #rect of spike

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
