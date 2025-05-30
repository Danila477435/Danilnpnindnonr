from pygame import *
from time import sleep
import random
from random import randint

font.init()
font1 = font.SysFont(None ,80)
win = font1.render("You Win!!!", True, (255,255,255))
lose=font1.render("U Lose!!!", True, (180,0,0))
font2=font.Font(None,36)



speed = 8
mos_cor =0

score = 0
lost = 0 
goal = 45
max_lost = 10


class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (80,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))    


class Player(Gamesprite):
        def move (self):
            keys_pressed = key.get_pressed()

            if keys_pressed[K_LEFT] and self.rect.x >5:
                self.rect.x -= self.speed

            if keys_pressed[K_RIGHT] and self.rect.x < 650:
                self.rect.x += self.speed

        def fire(self):
            bullet  = Bullet('bullet.png', self.rect.centerx - 20, self.rect.top,-15)
            bullets.add(bullet)
            bullet = Bullet('bullet.png', self.rect.centerx - 60, self.rect.top,-15)
            bullets.add(bullet)

class Enemy(Gamesprite):
        def move(self):
            self.rect.y += self.speed
            global lost
            if self.rect.y > win_heigth:
                self.rect.x=randint(80, win_heigth - 80)
                self.rect.y=0
                lost=lost+1

class Asteroid(Gamesprite):
    def move(self):
        self.rect.y += self.speed
        if self.rect.y > win_heigth:
            self.rect.x=randint(80, win_heigth - 80)
            self.rect.y=0
        



class Bullet(Gamesprite):
    def move(self):
        self.rect.y +=self.speed
        if self.rect.y < 0:
            self.kill()




           


x1 = 700
y1=500

x2=600
y2=400

win_heigth = 500
win_width = 700

clock=time.Clock()
fps=60

num_mos = 0

background = transform.scale(image.load("galaxy.jpg"), (win_width, win_width))
window = display.set_mode((win_width, win_width))
display.set_caption("SpaceFire")

player = Player('rocket.png', 300, 550, 5)

bullets = sprite.Group()
spisokwithenemy = sprite.Group()
asteroids_group = sprite.Group()

for i in range(5):
    ufo = Enemy('ufo.png',randint(50,650), 0, 1 )
    spisokwithenemy.add(ufo)

for i  in range (1,3):
    asteroid = Asteroid('asteroid.png', randint(50,650), 0, 2)
    asteroids_group.add(asteroid)



finish = False

game = True

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

while game: 

    for e in event.get():
        if e.type == QUIT:
           game = False


   


        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()


    if not finish:
        window.blit(background, (0,0))
        text = font2.render("Счет:" + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text_lose = font2.render("Пропущенно:" +str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))

        player.draw()
        player.move()

        for enemy in spisokwithenemy:
            enemy.draw()
            enemy.move()

        for b in bullets:
            b.move()
            b.draw()

        for asteroid in asteroids_group:
            asteroid.draw()
            asteroid.move()




        collides = sprite.groupcollide(spisokwithenemy, bullets, True, True)
        for c in collides:
            score = score +1
            ufo = Enemy('ufo.png', randint(80, win_width-80), -40, randint(1,2))
            spisokwithenemy.add(ufo)



        


        if sprite.spritecollide(player, asteroids_group, False):
            finish = True
            finish_img = font1.render('You LOSE!', True, (180,0,0))

        if score >= goal:
            finish = True
            finish_img = font1.render('You WIN!', True, (0,250,0))
            for bullet in bullets:
                bullet.kill()

            for enemy in spisokwithenemy:
                enemy.kill()

            window.blit(finish_img, (200, 200))
    else:           
        sprite.spritecollide(player, spisokwithenemy, False) or lost >= max_lost or sprite.spritecollide(player, asteroids_group, False)
        finish = True
        finish_img = font1.render('You LOSE!', True, (180,0,0))
        for bullet in bullets:
            bullet.kill()

        for enemy in spisokwithenemy:
            enemy.kill()

        window.blit(finish_img, (200, 200))







    display.update()
    clock.tick(fps)               