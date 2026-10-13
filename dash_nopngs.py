import pygame
import math

pygame.init()

WIDTH=1280
HEIGHT=720
cube_width=80
cube_height=80
cube_rect_width = 40
cube_rect_height = 40

spike_width = 100
spike_height = 75
spike_rect_width = 60
spike_rect_height = 120
fps=60

font=pygame.font.SysFont("Arial",20)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

#class Objects

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("spike.png")
        self.image = pygame.transform.scale(self.image, (spike_rect_width,spike_rect_height))
        self.image = pygame.transform.scale(self.image, (spike_width, spike_height))
        self.rect = self.image.get_rect() #creates hitbox for spike sprite
        #self.rect.size = (50,75)
        self.rect.center = [x, y] #center of hitbox
        self.speed = 7 #speed going to the left

    def update(self):
        self.rect.x -= self.speed
        #print(self.rect.x)
        if self.rect.x <= -25:
            self.kill()


class Cube(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((cube_width, cube_height))
        self.image.fill("white")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y] #rect = hitbox
        self.vel = 0


    def update(self):
        # Gravity
        self.vel += 1#0.5
        self.rect.y += int(self.vel)

        #print(self.vel)


        # Stay on the ground

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel = 0


        # Jump
        if pygame.mouse.get_pressed()[0] == 1:
            #if self.rect.centery >= HEIGHT - int(cube_height/2):
            if self.rect.bottom >= HEIGHT:
                self.vel = -17

        #print(self.rect.centery)



cube_group = pygame.sprite.Group()
player = Cube(5*cube_width, HEIGHT) #????? sommehow 60??????????????????????????????????????????????
cube_group.add(player)

spike_group = pygame.sprite.Group()
#spike = Spike(WIDTH, HEIGHT-15)
spike = Spike(WIDTH-50, HEIGHT-15)
spike_group.add(spike)

Running = True
while Running:
    clock.tick(60)

    #BG
    screen.fill("light blue")

    #blit
    cube_group.draw(screen)
    cube_group.update()
    spike_group.draw(screen)
    spike_group.update()

    pygame.draw.rect(screen, "red", player.rect, 2)
    pygame.draw.rect(screen,"red",spike.rect,2)
    
    if pygame.sprite.groupcollide(cube_group, spike_group,False,False) or player.rect.right == spike.rect.left:
        Running = False


    #FPS
    fps=clock.get_fps()
    #fps_val=font.render(str(math.floor(fps)),True,"black")
    fps_val=font.render(f"fps:{str(round(fps,2))}",True,"black")
    screen.blit(fps_val,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False


    pygame.display.update()


pygame.quit()