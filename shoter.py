from pygame import *
from random import randint

mixer.init()
mixer_music.load('ggg.mp3')
mixer_music.play(-1)
fire_sound = mixer.Sound('fire.mp3')

font.init()
font1 = font.Font(None, 80)
win_message = font1.render("YOU WIN!", True, (255, 255, 255))
lose_message = font1.render("YOU LOSE!", True, (100, 0, 0))
font2 = font.Font(None, 36)

img_back = "galaxy.jpg"
img_V1 = "img_V1.png"
img_V2 = "img_V2.png"
img_V3 = "img_V3.png"
img_bullet = "img_bullet.png"
img_enemy = "ufo.png"
explosion_images = ["explosion1.png", "explosion2.png", "explosion3.png", "explosion4.png"]

score = 0
goal = 100
lost = 0
max_lost = 3
coins = 0
current_skin = img_V1

enemy_speed = 1
enemy_count = 5

def load_coins():
    global coins
    try:
        with open("coins.txt", "r") as file:
            coins = int(file.read())
    except FileNotFoundError:
        coins = 0
    except ValueError:
        coins = 0

def save_coins():
    with open("coins.txt", "w") as file:
        file.write(str(coins))

class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Gamesprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.ammo = 10
        self.reload_time = 2000
        self.last_reload = 0

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        if self.ammo > 0:
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 20, 25, -5)
            bullets.add(bullet)
            self.ammo -= 1
            fire_sound.play()

    def reload(self):
        now = time.get_ticks()
        if now - self.last_reload > self.reload_time:
            self.ammo = 10
            self.last_reload = now

class Enemy(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40
            lost += 1

class Bullet(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Explosion(Gamesprite):
    def __init__(self, x, y):
        super().__init__(explosion_images[0], x, y, 50, 50, 0)
        self.frames = [transform.scale(image.load(img), (50, 50)) for img in explosion_images]
        self.current_frame = 1
        self.last_update = time.get_ticks()

    def update(self):
        if time.get_ticks() - self.last_update > 250:
            self.last_update = time.get_ticks()
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.current_frame]

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

bullets = sprite.Group()
ship = Player(current_skin, 5, win_height - 110, 88, 110, 11)

monsters = sprite.Group()
explosions = sprite.Group()

def create_monsters():
    monsters.empty()
    for i in range(enemy_count):
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, enemy_speed)
        monsters.add(monster)

def game_loop():
    global score, lost, finish, goal, coins
    score = 0
    lost = 0
    finish = False
    run = True
    create_monsters()

    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    fire_sound.play()
                    ship.fire()
                elif e.key == K_r:
                    ship.reload()

        if not finish:
            window.blit(background, (0, 0))

            text = font2.render("Score: " + str(score), 1, (255, 255, 255))
            window.blit(text, (10, 20))
            text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
            window.blit(text_lose, (10, 50))
            text_goal = font2.render("Goal: " + str(goal), 1, (255, 255, 255))
            window.blit(text_goal, (10, 80))

            ammo_text = font2.render(f"Ammo: {ship.ammo}/10", 1, (255, 255, 255))
            window.blit(ammo_text, (win_width - 150, 20))

            ship.update()
            bullets.update()
            monsters.update()
            explosions.update()

            ship.reset()
            monsters.draw(window)
            bullets.draw(window)
            explosions.draw(window)

            collides = sprite.groupcollide(monsters, bullets, True, True)
            for c in collides:
                score += 1
                coins += 5
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, enemy_speed)
                monsters.add(monster)

                explosion = Explosion(c.rect.x, c.rect.y)
                explosions.add(explosion)

            if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
                finish = True
                window.blit(lose_message, (200, 200))
                display.update()
                time.delay(5000)  # Затримка 5 секунд
                break  

            if score >= goal:
                finish = True
                window.blit(win_message, (200, 200))
                display.update()
                time.delay(5000)  # Затримка 5 секунд
                break

            display.update()

        time.delay(16)

    save_coins()
    quit()  # Закриваємо гру після 5 секундної затримки

load_coins()
game_loop()
