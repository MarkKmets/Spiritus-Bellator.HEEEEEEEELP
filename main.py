#підключаємо модуль
import pygame
from treba import *
#створення та іменування вікна

window=pygame.display.set_mode((win_wid,win_hei))
pygame.display.set_caption(caption)


#музика
pygame.mixer.init()
pygame.mixer.music.load(main_music)
pygame.mixer.music.play(-1)
over= pygame.mixer.Sound(defeat)
shot= pygame.mixer.Sound(fire)


#змінні прапорці
bullets=pygame.sprite.Group()
#класи
class GameSprite(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,name):
        super().__init__()
        self.image=pygame.transform.scale(pygame.image.load(name),(win_wid,win_hei))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def __init__(self,x,y,width,height,x_speed,y_speed,name,orien):
        GameSprite.__init__(self,x,y,width,height,name)
        self.x_speed=x_speed
        self.y_speed=y_speed
        self.orien=orien
    def update(self):
        if ghost.rect.x <= win_wid-50 and ghost.x_speed > 0 or ghost.rect.x >= 0 and ghost.x_speed < 0:
            self.rect.x += self.x_speed
        touched = pygame.sprite.spritecollide(self, walls, False)
        if self.x_speed > 0:
            for p in touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if ghost.rect.y <= win_hei-50 and ghost.y_speed > 0 or ghost.rect.y >= 0 and ghost.y_speed < 0:
            self.rect.y += self.y_speed
        touched = pygame.sprite.spritecollide(self, walls, False)
        if self.y_speed > 0:
            for p in touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def draw(self):
        if self.orien=='right':
            window.blit(self.image,(self.rect.x,self.rect.y))
        elif self.orien=='left':
            window.blit(pygame.transform.flip(self.image,True,False),(self.rect.x,self.rect.y))
    def fire(self):
        shot.play()
        if self.orien=='right':
            bullets.add(Bullet(self.rect.right, self.rect.centery, 15, 20, "bullet_right.png", 15))
        elif self.orien=='left':
            bullets.add(Bullet(self.rect.left, self.rect.centery, 15, 20, "bullet_left.png", -15))    

        
class Enemy(GameSprite):
    def __init__(self,x,y,width,height,name,x1,x2,side):
        GameSprite.__init__(self,x,y,width,height,name)
        self.start=x1
        self.end=x2
        self.speed=5
        self.side=side
    def update(self):
        if self.rect.x <=self.start:
            self.side=ri
        elif self.rect.x >=self.end:
            self.side=le
        if self.side==le:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self,x,y,width,height,name,speed):
        GameSprite.__init__(self,x,y,width,height,name)
        self.speed=speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_x+10:
            self.kill()
        elif self.rect.x <0:
            self.kill()
#створення гравця
picture=GameSprite(0,0,win_wid,win_hei,display_picture)       
ghost=Player(75,610,50,50,0,0,ghost_picture,ri)
final=GameSprite(900,600,75,75,door_picture)
holy_water=GameSprite(465,380,50,50,water_picture)
label=GameSprite(350,675,400,100,text_picture)
#створення демонів
demons=pygame.sprite.Group()
demons.add(Enemy(155,10,50,60,demon_picture,150,850,ri))
demons.add(Enemy(230,160,50,60,demon_picture,225,775,ri))
demons.add(Enemy(5,310,50,60,demon_picture,0,325,ri))
#створення стін
walls=pygame.sprite.Group()
walls.add(GameSprite(0,450,225,75,"wall2.png"))
walls.add(GameSprite(225,675,225,75,"wall2.png"))
walls.add(GameSprite(450,675,225,75,"wall2.png"))
walls.add(GameSprite(375,525,225,75,"wall2.png"))
walls.add(GameSprite(225,75,225,75,"wall2.png"))
walls.add(GameSprite(225,225,225,75,"wall2.png"))
walls.add(GameSprite(450,75,225,75,"wall2.png"))
walls.add(GameSprite(675,75,225,75,"wall2.png"))
walls.add(GameSprite(825,450,225,75,"wall2.png"))
walls.add(GameSprite(525,225,225,75,"wall2.png"))
walls.add(GameSprite(225,375,75,225,"wall1.png"))
walls.add(GameSprite(675,300,75,225,"wall1.png"))
walls.add(GameSprite(375,300,75,225,"wall1.png"))
walls.add(GameSprite(525,300,75,225,"wall1.png"))
walls.add(GameSprite(150,75,75,225,"wall1.png"))
walls.add(GameSprite(825,150,75,225,"wall1.png"))
secretwall=GameSprite(675,525,75,225,"wall1.png")

#основний ігровий цикл
while play: 
    #обробка подій
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            play=False
        elif e.type==pygame.KEYDOWN:
            if e.key==pygame.K_LEFT:
                ghost.x_speed=-7
                ghost.orien=le
            elif e.key==pygame.K_RIGHT:
                ghost.x_speed=7
                ghost.orien=ri
            elif e.key==pygame.K_UP:
                ghost.y_speed=-7
            elif e.key==pygame.K_DOWN:
                ghost.y_speed=7
            elif e.key==pygame.K_SPACE:

                if bulletsamount>0:
                    ghost.fire()
                    bulletsamount-=1

        elif e.type==pygame.KEYUP:
            if e.key==pygame.K_LEFT:
                ghost.x_speed=0
            elif e.key==pygame.K_RIGHT:
                ghost.x_speed=0
            elif e.key==pygame.K_UP:
                ghost.y_speed=0
            elif e.key==pygame.K_DOWN:
                ghost.y_speed=0
    if not finish:
        
        picture.draw()
        final.draw()
        ghost.draw()
        walls.draw(window)
        demons.draw(window)
        bullets.draw(window)
        secretwall.draw()
        bullets.update()
        demons.update()
        ghost.update()
        pygame.sprite.groupcollide(bullets,walls,True,False)
        pygame.sprite.groupcollide(bullets,demons,True,True)

        if bulletsamount==0:
            reloading+=1
            if reloading>=35:
                bulletsamount+=7
                reloading=0

        
        if not door_open:
                    holy_water.draw()
                    if pygame.sprite.collide_rect(ghost, holy_water):
                        door_open=True
                        del holy_water


        if pygame.sprite.spritecollide(ghost, demons, False):
            finish = True
            pygame.mixer.music.stop()
            over.play()
            # обчислюємо ставлення
            img = pygame.image.load('game_over.png')
            window.blit(pygame.transform.scale(img, (win_wid, win_hei)), (0, 0))


        if pygame.sprite.collide_rect(ghost, final):
            if door_open==True:
                pygame.mixer.music.stop()
                finish = True
                img = pygame.image.load('winner.png')
                window.blit(pygame.transform.scale(img, (win_wid, win_hei)), (0, 0))
            else:
                label.draw()
        # оновлення сцени
    
    pygame.time.delay(30)
    pygame.display.update()
