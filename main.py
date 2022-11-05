from datetime import datetime
import random
import os
from abc import ABC, abstractmethod
import pygame

pygame.init()
pygame.display.set_caption("MoltafDefence")
win = pygame.display.set_mode((700, 700))

enemyhousepic = pygame.transform.scale(pygame.image.load(os.path.join("assets" ,"HouseOfEnemy.jpg")), (120, 120))
enemy1pic = pygame.transform.scale(pygame.image.load(os.path.join("assets" ,"enemy1.png")), (80, 80))
enemy2pic = pygame.transform.scale(pygame.image.load(os.path.join("assets" ,"enemy2.png")), (80, 80))
bulletpic = pygame.transform.scale(pygame.image.load(os.path.join("assets" ,"bullet.png")), (40, 40))
bombpic = pygame.transform.scale(pygame.image.load(os.path.join("assets" ,"Bomb.jpg")), (120, 120))
defenderpic = pygame.transform.scale(pygame.image.load(os.path.join("assets" ,"Tower.png")), (90, 90))
backgroundpic = pygame.transform.scale(pygame.image.load(os.path.join("assets" ,"background.jpg")), (700, 700))

damagefont = pygame.font.SysFont("chalkduster. ttf" , 20)
coinfont = pygame.font.SysFont("chalkduster. ttf" , 72)
endgamefont = pygame.font.SysFont("chalkduster. ttf" , 100)
damage = 100
coin = 400

class Enemyhouse:
    def __init__(self):
        self.__x = 0
        self.__y = 570
        self.enemies = []

    def make(self, win):
        win.blit(enemyhousepic, (self.__x, self.__y))

    def makeEnemy(self):
        if 0 <= len(self.enemies) <= 3:
            enemyyyyy = [Enemy2, Enemy1]
            enemy = random.choice(enemyyyyy)
            self.enemies.append(enemy())


    def draw_enemy(self, win):
        for Enemy in self.enemies:
            Enemy.make(win)

    def move_enemy(self):
        for Enemy in self.enemies:
            Enemy.move()

    def enemy_win(self):
        for Enemy in self.enemies:
            if 0<= Enemy.x <=40 and 0<= Enemy.y <=40:
                
                self.enemies.remove(Enemy)
                return True, str(Enemy)
        return False, "THE END"

    def RIP_enemy(self):
        for Enemy in self.enemies:
            if Enemy.health <= 0:
                self.enemies.remove(Enemy)
                return True
        return False


class Enemy(ABC):
    def __init__(self):
        self.x = 0
        self.y = 600
        self.speed = 0


    
    def move(self):
        if self.y == 600 and self.x < 600:
            self.x += self.speed
        elif 25<self.y <= 600 and self.x == 600:
            self.y -= self.speed
        else:
            self.x -= self.speed

    @abstractmethod
    def make(self, win):
        pass

class Enemy2(Enemy):
    def __init__(self):
        super().__init__()
        self.speed = 2
        self.health = 100

    def make(self, win):
        win.blit(enemy2pic, (self.x, self.y))

    def __str__(self):
        return "Enemy2"

class Enemy1(Enemy):
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.health = 200

    def make(self, win):
        win.blit(enemy1pic, (self.x, self.y))

    def __str__(self):
        return "Enemy1"

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.damage = 20
        self.speed = 4

    def move_bullet_down(self):
        self.y += self.speed

    def move_bullet_right(self):
        self.x += self.speed
    
    def move_bullet_up(self):
        self.y -= self.speed


    def draw_bullet(self, win):
        win.blit(bulletpic, (self.x, self.y))


class Defender:
    towers = []
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []
        

    @classmethod
    def create_tower(cls, x, y):
        cls.towers.append(cls(x, y))

    
    def draw_tower(win):
        for defender in Defender.towers:
            win.blit(defenderpic, (defender.x, defender.y))


    def draw_bullet(self, win):
        for bullet in self.bullets:
            bullet.draw_bullet(win)

    def bullet_D(self):
        for bullet in self.bullets:
            bullet.move_bullet_down()

    def bullet_R(self):
        for bullet in self.bullets:
            bullet.move_bullet_right()

    def bullet_U(self):
        for bullet in self.bullets:
            bullet.move_bullet_up()

    def RIP_bullet(self):
        for bullet in self.bullets:
            if bullet.x > 650 or bullet.y > 650 or bullet.y < 10:
                self.bullets.remove(bullet)


Enemyhouse = Enemyhouse()
defender = Defender(150, 50)
Defender.create_tower(500, 250)
Defender.create_tower(200, 500)

blue = (  0,  0,255)
yellow = (255,255,  0)

def end():
    end_text = endgamefont.render("Kheylia Age Barandeh Nabashan\nVali Piroozan\nKhasteh Nabashan", 1, (255, 0, 0))
    win.blit(end_text, (700/2 - end_text.get_width() / 2, 700/2 - end_text.get_width() / 2))
    pygame.display.update()
    print("THE END")
    pygame.time.delay(5000)

def make_game():

    win.blit(backgroundpic, (0, 0))
    

    Enemyhouse.make(win)
    Enemyhouse.draw_enemy(win)

    Defender.draw_tower(win)

    for tower in Defender.towers:
        tower.draw_bullet(win)

    win.blit(bombpic, (10, 10))

    health_text = coinfont.render(str(damage), 1, blue)
    coin_text = coinfont.render(str(coin) + "$", 1, yellow)


    win.blit(coin_text, (250, 300))
    win.blit(health_text, (35, 30))

    pygame.time.delay(10)

    pygame.display.update()

run = True
while run:
    now = datetime.now()
    if int(now.strftime("%f")[:2]) % 50 == 0:
        Enemyhouse.makeEnemy()
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if coin >= 500:
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            defender.create_tower(x-50, y-50)
            coin -= 500

    for defender2 in Defender.towers:
        if len(defender2.bullets) < 1:
            for Enemy in Enemyhouse.enemies:
                if 0 < defender2.x - Enemy.x < 100 and 0 < Enemy.y - defender2.y < 200 and defender2.x > Enemy.x:
                    defender2.bullets.append(Bullet(defender2.x + 30, defender2.y + 30))
                elif 0 < Enemy.x - defender2.x < 200 and 0 < Enemy.y - defender2.y < 100 and  Enemy.x > defender2.x :
                    defender2.bullets.append(Bullet(defender2.x + 30, defender2.y + 30))

                elif 0< Enemy.x - defender2.x <100 and 0< defender2.y - Enemy.y<50 and  Enemy.y < defender2.y :
                    defender2.bullets.append(Bullet(defender2.x + 30, defender2.y + 30))

    for defender, Enemy in zip(Defender.towers, Enemyhouse.enemies):
        for bullet in defender.bullets:
            if -30 <= Enemy.x - bullet.x <= 30 and -30 <= Enemy.y - bullet.y <= 30:
                Enemy.health -= bullet.damage


    for defender1 in defender.towers:
        if defender1.y > 470:
            defender1.bullet_D()
        if 130< defender1.y <= 470:
            defender1.bullet_R()
        if defender1.y <= 130:
            defender1.bullet_U()   
            
    Enemyhouse.move_enemy()

    for defender in Defender.towers:
        defender.RIP_bullet()

    res = Enemyhouse.enemy_win()
    if res[0]:
        if res[1] == "Enemy2":
            damage -= 10
        elif res[1] == "Enemy1":
            damage -= 15


    if Enemyhouse.RIP_enemy():
        coin += 250

    if damage <= 0:
        end()

    make_game()
    