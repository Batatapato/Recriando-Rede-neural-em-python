import pygame as pg
import time
import math
import random as rand 
from scale_image import scale_image
from rotaciona_carro import blit_rotate_center

pista = scale_image(pg.image.load("img/pista6.png"),0.6) 

borda_pista = scale_image(pg.image.load("img/pista6_transparent.png"),0.6)
borda_pista_mask = pg.mask.from_surface(borda_pista)
chegada = pg.image.load("img/finish.png")
chegada = pg.transform.scale(chegada, (90, 20))
chegada_mask = pg.mask.from_surface(chegada)


carro = scale_image(pg.image.load("img/carro0.png"),0.06)
carro = pg.transform.rotate(carro, 90)

x_pista,y_pista = pista.get_width(), pista.get_height()
WIN = pg.display.set_mode((x_pista, y_pista))

pg.display.set_caption("aaaaaaaaaaaaa")

FPS = 60
class AbstractCar:
   
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel =0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = rand.randint(730, 770), 530
        self.acceleration = 0.2
        
    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
    def draw(self,win):
              
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
        self.img = self.IMG
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration/2, -self.max_vel/2)
        self.move()
          
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def colisao(self, mask, x=0, y=0):
        car_mask = pg.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
def draw(win,images,PlayerCar):
    for img, pos in images:
        win.blit(img,pos)

    PlayerCar.draw(win)
    pg.display.update()

def move_player(PlayerCar):
    keys = pg.key.get_pressed()
    moved =  False
    if keys[pg.K_a] and PlayerCar.vel != 0:
        PlayerCar.rotate(left=True)
    if keys[pg.K_d] and PlayerCar.vel != 0:
        PlayerCar.rotate(right=True)
    if keys[pg.K_w]:
        moved = True
        PlayerCar.move_forward()
    if keys[pg.K_s]:
        moved = True
        PlayerCar.move_backward()
    if not moved:
        PlayerCar.reduce_speed()
    
 
class PlayerCar(AbstractCar):
     IMG = carro
     START_POS = (180, 200)
     def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()
     def bounce(self):
        self.vel = -self.vel
        self.move()

run = True
clock = pg.time.Clock()
images = [(pista,(0,0)), (borda_pista,(0,0)), (chegada,(720,610))]#708,620
PlayerCar = PlayerCar(4, 4)
while run:
    clock.tick(FPS)

    draw(WIN, images, PlayerCar)
    


  

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
  
    move_player(PlayerCar)

    if PlayerCar.colisao(borda_pista_mask) != None:
        PlayerCar.bounce()
    if PlayerCar.colisao(chegada_mask, 720, 610) != None:
        print("fim")
        
pg.quit()
