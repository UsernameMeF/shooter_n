from pygame import *
from random import randint # Імпорти всіх бібліотек що нам потрібні
init()
import time as t


W = 500 # Ширина вікна
H = 700 # Висота вікна

window = display.set_mode((W, H)) # Робимо вікно
display.set_caption("Shooter") # Змінюємо названня
display.set_icon(image.load("rocket_n.png")) # Змінюємо іконку

back = transform.scale(image.load('galaxy_n.png'), (W, H)) # Робимо фон
#clock = time.Clock()
lost = 0 # 
killed = 0
life = 3

""" Звуки """


mixer.init() # Робимо можливим взагалі використовувати звуки
mixer.music.load('US3.mp3') # Загружаємо звук space.ogg
mixer.music.set_volume(0.3) # Змінюємо гучність звуку
fire = mixer.Sound('fire_n.wav') # Загружаємо звук fire.ogg в змінну fire
mixer.music.play() # Включаємо музику (space.ogg)

MUSIC_END = USEREVENT + 1
mixer.music.set_endevent(MUSIC_END)

""" ШРИФТИ """
font.init()
font1 = font.SysFont("Arial", 30, bold=True)
font2 = font.SysFont("Arial", 60, bold=True)



""" КЛАСИ """ 

class GameSprite(sprite.Sprite): # Створюємо класс GameSprite
    # Конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Викликаємо конструктор класу (Sprite):
        super().__init__()
        # Кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) # Загружаємо і змінюємо розмір player_image
        self.speed = player_speed
# Кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # Метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite): # Створюємо класс Player (основа класс GameSprite)
    def update(self):
        keys_pressed = key.get_pressed() # Перевіряємо натискання на клавіші
        if keys_pressed[K_a] and self.rect.x > 0: # Рух грацвя вліво якщо натиснута кнопка a-A
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < W - 80: # Рух гравця вправо якщо натиснута кнопка d-D
            self.rect.x += self.speed


    def fire (self):
        bullet = Bullet('bullet_n.png', self.rect.centerx, self.rect.top, 15, 20, 10)
        bullets.add(bullet)  


class Enemy(GameSprite): # Класс для ворогів
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > H: # Робимо так щоб ворог падав вниз
            self.rect.y = 0
            self.rect.x = randint(0, W - 80)
            lost += 1

class Asteroid(Enemy):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > H: # Робимо так щоб астероід падав вниз
            self.rect.y = 0
            self.rect.x = randint(0, W - 80)
            


class Bullet(GameSprite): # Класс для куль
    def update(self):
        self.rect.y -= self.speed # Переміщення куль
        if self.rect.y < 0:
            self.kill()



player = Player("rocket_n.png",W/2,H-100,80,100,10) # Створюємо гравця

monsters = sprite.Group() # Створюємо групу монстрів
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(5): # Створюємо цикл, в якому створуюємо монстрів для группи
    monster = Enemy("ufo_n.png", randint(0,W-80), randint(-150, -20), 80, 50, randint(4, 5))
    monsters.add(monster)

for i in range(3): # Створюємо цикл, в якому створуюємо монстрів для группи
    asteroid = Asteroid("asteroid_n.png", randint(0,W-80), randint(-500, -150), 80, 50, randint(2, 4))
    asteroids.add(asteroid)




""" ІГРОВИЙ ЦИКЛ """ 



game = True # Ігровий перемикач циклу
finish = False
num_fire = 0
rel_time = False
color_life = (0, 255, 0)


while game: # Ігровий цикл
    time.delay(50)
    for e in event.get(): # Перевіряємо події
        if e.type == QUIT: # Якщо натискаємо на червоний хрестик:
            game = False # Ігровий перемекач = False. Ігровий цикл, вікно закривається
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 6 or rel_time == False:
                    num_fire += 1
                    player.fire()
                    fire.play()
                if num_fire > 6 and rel_time is False:
                    rel_time = True
                    last_time = t.time()

        if e.type == MUSIC_END:
            print('music end event')
            mixer.music.play()


    if not finish:
    
        window.blit(back, (0, 0)) # Відмальовуємо фон
        player.reset() # малюємо гравця
        player.update() # запускаємо управління гравцем

        monsters.draw(window) # малюємо групу ворогів
        monsters.update() # Запускаємо рух ворогів

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()

        if rel_time:
            new_time = t.time()
            if new_time - last_time < 3:
                reload_txt = font1.render("Перезарядка...", True, (255, 0, 0))
                window.blit(reload_txt, (10, 90))
            else:
                rel_time = False
                num_fire = 0




        lost_txt = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255)) # Створюємо текст на екрані
        window.blit(lost_txt, (10, 10)) # Відмальовуємо текст


        killed_txt = font1.render("Збито: " + str(killed), 1, (255, 255, 255)) # Створюємо текст на екрані
        window.blit(killed_txt, (10, 50)) # Відмальовуємо текст



        life_txt = font2.render(str(life), 1, (color_life)) # Створюємо текст на екрані
        window.blit(life_txt, (450, 5)) # Відмальовуємо текст
        
        if life == 3:
            color_life = (0, 255, 0)

        if life == 2:
            color_life = (255, 255, 0)

        if life == 1:
            color_life = (255, 0, 0)

        if sprite.spritecollide(player, monsters, True): # Перевірка зіткнення гравця та монстрів
            life -= 1
            monster = Enemy("ufo_n.png", randint(0,W-80), -50, 80, 50, randint(2, 4))
            monsters.add(monster)

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for col in collides: 
            monster = Enemy("ufo_n.png", randint(0,W-80), -50, 80, 50, randint(2, 4))
            monsters.add(monster)
            killed += 1

        if killed > 50: # Якщо ми збили 25 нло, показуємо сповіщення про перемогу гравця написом на екрані + зупиняємо гру
            win = font2.render("YOU WIN!", True, (0, 255, 0))
            window.blit(win, (W/2-100, H/2-50))
            res_t = font1.render("R to restart", True, (0, 255, 0))
            window.blit(res_t, (W/2-50, H/2+25))
            finish = True

        if life <= 0 or lost >= 5: # Якщо ми витратили всі життя, або пропустили нло, ми програємо (надпис, зупиняємо гру)
            lose = font2.render("YOU LOSE!", True, (255, 0, 0))
            window.blit(lose, (W/2-115, H/2-50))
            res_t = font1.render("R to restart", True, (255, 0, 0))
            window.blit(res_t, (W/2-50, H/2+25))
            finish = True

        if sprite.spritecollide(player, asteroids, True):
            life -= 1
            asteroid = Asteroid("asteroid_n.png", randint(0,W-80), randint(-500, -150), 80, 50, randint(2, 4))
            asteroids.add(asteroid)


    else:
        keys_pressed = key.get_pressed()
        if keys_pressed[K_r]:
            life = 3
            killed = 0
            lost = 0
            num_fire = 0
            rel_time = False
            for m in monsters:
                m.kill()
            for b in bullets:
                b.kill()
            for i in range(5): # Створюємо цикл, в якому створуюємо монстрів для группи
                monster = Enemy("ufo_n.png", randint(0,W-80), randint(-150, -20), 80, 50, randint(2, 4))
                monsters.add(monster)
            for q in asteroids:
                q.kill()
            for i in range(3): # Створюємо цикл, в якому створуюємо монстрів для группи
                asteroid = Asteroid("asteroid_n.png", randint(0,W-80), randint(-500, -150), 80, 50, randint(2, 4))
                asteroids.add(asteroid)

            finish = False
            






    display.update() # Оновлюємо вікно