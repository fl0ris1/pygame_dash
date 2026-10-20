import pygame
import math

pygame.init()

#CONST
"""WIDTH=1280
HEIGHT=720"""
WIDTH = 1280
HEIGHT = 700

cube_width=80
cube_height=80
cube_rect_width = 40
cube_rect_height = 40

spike_width = 50
spike_height = 50
spike_hitbox_width = 30

#Settings up
font=pygame.font.SysFont("Arial",20)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
FPS=60


#Classes
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((spike_width,spike_height),pygame.SRCALPHA) #create surface for spike: 50 wide, 75 tall
        pygame.draw.polygon(self.image, "black", #draw 3 point polygon
    [
        (spike_width // 2, 0), #middle top. self.image is the canvas
        (0, spike_height), #bottom left
        (spike_width, spike_height) #bottom right 
    ]
)
        self.rect = self.image.get_rect(center=(x,y)) #creates hitbox for spike sprite
        self.hitbox = pygame.Rect(0, 0, 20, spike_height-10) #creates a smaller rect that follows self.rect
        self.hitbox.bottom = self.rect.bottom
        self.speed = 7 #speed going to the left

    def update(self):
        self.rect.x -= self.speed #spikes rect -7 to move to the left
        self.hitbox.center = self.rect.center
        #print(self.rect.x)
        if self.rect.x <= -cube_width: #delete if touching left border
            self.rect.x = WIDTH


    def draw_hitbox(self):
        pygame.draw.rect(screen,"blue",self.rect,2) #rect of spike
        pygame.draw.rect(screen,"red",self.hitbox,2) #rect of spike


class Cube(pygame.sprite.Sprite):
    def __init__(self, x, y, playerNo):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.Surface((cube_width, cube_height), pygame.SRCALPHA) #canvas basically
        self.original_image.fill("white") #fill the surface with white

        self.image = self.original_image
        self.rect = self.original_image.get_rect(center=(x,y)) #create rect

        self.playerNo = playerNo
        self.vel = 0 #velocity
        self.angle = 0
        self.angle_val = 5


    def update(self):
        print(self.angle)
        #print(self.playerNo)
        if self.playerNo == 1:
            # Gravity
            self.vel += 1#0.5always increase vel
            self.rect.y += int(self.vel) #add velocity to the y

            # Stay on the ground

            if self.rect.bottom >= HEIGHT: #if bottom of rectangle is touching or under the ground
                self.rect.bottom = HEIGHT #bottom of rectangle is on the ground
                self.vel = 0 #reset velocity
                self.angle = 0
                self.image = pygame.transform.rotate(self.original_image, self.angle)
                self.rect = self.image.get_rect(midbottom = (self.rect.centerx,HEIGHT))
                #self.rect = self.image.get_rect(center = self.rect.center)

            else:
                self.angle -= self.angle_val
                self.image = pygame.transform.rotate(self.original_image, self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)

            # Jump
            if pygame.mouse.get_pressed()[0] == 1: #left mouse click activated
                #if self.rect.centery >= HEIGHT - int(cube_height/2):
                if self.rect.bottom >= HEIGHT: #if touching ground
                    #self.angle_val+=0.1
                    #print(self.angle_val)
                    self.vel = -18 #?????????????Somehow works

            #print(self.rect.centery)

        elif self.playerNo == 2:
            # Gravity
            self.vel -= 1#0.5always increase vel
            self.rect.y += int(self.vel) #add velocity to the y

            # Stay on the ground

            if self.rect.top <= 0: #if bottom of rectangle is touching or under the ground
                self.rect.top = 0 #bottom of rectangle is on the ground
                self.vel = 0 #reset velocity
                self.angle = 0
                self.image = pygame.transform.rotate(self.original_image, self.angle)
                #self.rect = self.image.get_rect(midbottom = (self.rect.centerx,HEIGHT))
                self.rect = self.image.get_rect(center = self.rect.center)

            else:
                self.angle += 2.7
                self.image = pygame.transform.rotate(self.original_image, self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)

            # Jump
            if pygame.mouse.get_pressed()[0] == 1: #left mouse click activated
                if self.rect.top <= 0:
                    self.vel = 18

    def draw_hitbox(self):
        pygame.draw.rect(screen, "green", self.rect, 2) #rect of cube
    

#creating groups and adding
cube_group = pygame.sprite.Group()
player = Cube(5*cube_width, HEIGHT,1)
player2 = Cube(5*cube_width, 0, 2)
cube_group.add(player,player2)

spike_group = pygame.sprite.Group()
spike = Spike(WIDTH, HEIGHT-spike_height//2)
spike_group.add(spike)

Running = True

while Running:
    clock.tick(FPS) #fps
    #dt = clock.tick(FPS)/1000

    #BG
    screen.fill("light blue")

    #blit
    cube_group.update()
    cube_group.draw(screen)
    for cube in cube_group:
        cube.draw_hitbox()

    spike_group.update()
    spike_group.draw(screen)
    for spikes in spike_group:
        spikes.draw_hitbox()
    
    #if pygame.sprite.groupcollide(cube_group, spike_group,False,False): #or player.rect.right == spike.rect.left: #Check collision
    if player.rect.colliderect(spike.hitbox):
        Running = False


    #fps_val=font.render(str(math.floor(fps)),True,"black")
    fps_val=font.render(f"fps:{str(round(clock.get_fps(),2))}",True,"black")
    screen.blit(fps_val,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False


    pygame.display.update()

while True: #ignore; TEMPORARY FIX
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

pygame.quit()