#Создай собственный Шутер!
from pygame import *
from random import randint

win_width= 700
window= display.set_mode((win_width, 500))

display.set_caption('Space Wars')
background= transform.scale(image.load('galaxy.jpg'),(700, 500))

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.load('fire.ogg')
#mixer.music.play()

font.init()
font1 = font.Font(None, 70)
font2 = font.Font(None, 36)
lost= 0 


class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y,player_speed, weidth, height):
        super().__init__()
        self.image= transform.scale(image.load(player_image), (weidth, height))
        self.speed= player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def blit(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, weidth, height):
        super().__init__(player_image, player_x, player_y, player_speed, weidth, height)
    def update(self):
        self.rect.y -= self.speed
        self.blit()
        if self.rect.y < 0:
            self.kill

class Rocket(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed,weidth, height):
        super().__init__(player_image, player_x, player_y, player_speed, weidth, height)
    def move(self):
        keys_pressed= key.get_pressed()
        if keys_pressed[K_s] and self.rect.y < 410:
            self.rect.y += self.speed
        if keys_pressed[K_w] and self.rect.y > 300:
            self.rect.y -= self.speed
        if keys_pressed[K_d] and self.rect.x < 610:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet= Bullet('bullet.png', self.rect.centerx, self.rect.top, 5, 25, 25)
        bullets.add(bullet)

nice= 0


class UFO(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed,weidth, height):
        super().__init__(player_image, player_x, player_y, player_speed, weidth, height)
    def update(self):
        if self.rect.y < 500:
            self.rect.y += self.speed
        else:
            self.rect.y = -50
            global lost
            lost= lost + 1

player= Rocket('rocket.png',350,400, 5, 100, 100)

clock= time.Clock()

enemies= sprite.Group()

game= True
finish= False

bullets= sprite.Group()

for i in range(1, 4):
    enemy= UFO('ufo.png', randint(80, win_width - 80), -50, randint(1, 5), 80, 50)
    enemies.add(enemy)

while game:
    for e in event.get():
        if e.type == QUIT:
            game= False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #fire_sound.play()
                player.fire()
    if not finish:
        window.blit(background,(0,0))

        text_lose= font2.render('Пропущено: ' + str(lost), 1, (255,255,255))
        text_nice= font2.render('Счет: ' + str(nice), 1, (255,255,255))
        window.blit(text_lose, (10,40))
        window.blit(text_nice, (10,10))

        enemies.draw(window)
        enemies.update()
    
        player.move()
        player.blit()
        bullets.update()
        display.update()
        FPS= 60
        clock.tick(FPS)

        collide= sprite.groupcollide(enemies, bullets, True, True)
        for c in collide:
            nice= nice + 1
            enemy = UFO('ufo.png', randint(80, win_width - 80), -40, randint(1, 5), 80, 50)
            enemies.add(enemy)

        if sprite.spritecollide(player, enemies, False) or lost == 3:
            finish= True
            lose = font1.render('YOU LOSER!:(', True, (255,255,255))
            window.blit(lose, (200,200))

        if nice == 10:
            win = font1.render('YOU WIN!:)', True, (255,255,255))
            finish= True
            window.blit(win, (200,200))



    



    
