from pygame import *
from random import randint

mixer.init()
mixer_music.load('ggg.mp3')
mixer_music.play(-1)  # Play music in a loop
fire_sound = mixer.Sound('fire.mp3')

font.init()
font1 = font.Font(None, 80)
win = font1.render("YOU WIN!", True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (100, 0, 0))
font2 = font.Font(None, 36)

img_back = "galaxy.jpg"
img_V1 = "img_V1.png"  # Default skin
img_V2 = "img_V2.png"  # Skin 2
img_V3 = "img_V3.png"  # Skin 3
img_bullet = "img_bullet.png"
img_enemy = "ufo.png"
explosion_images = ["explosion1.png", "explosion2.png", "explosion3.png", "explosion4.png"]  # List of explosion frames

score = 0
goal = 100
lost = 0
max_lost = 3
coins = 0  # Currency system for purchasing skins
current_skin = img_V1  # The skin the player is currently using

enemy_speed = 1 # Default speed
enemy_count = 5 # Default number of enemies

# Function to load saved coins from file
def load_coins():
    global coins
    try:
        with open("coins.txt", "r") as file:
            coins = int(file.read())  # Read the coin value from the file
    except FileNotFoundError:
        coins = 0  # If no file exists, start with 0 coins
    except ValueError:
        coins = 0  # If the file contains invalid data, start with 0 coins

# Function to save the current coin count to a file
def save_coins():
    with open("coins.txt", "w") as file:
        file.write(str(coins))  # Write the coin count to the file

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
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 20, 25, -5 )
        bullets.add(bullet)

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
        # Update animation frames
        if time.get_ticks() - self.last_update > 100:  # Change frame every 100 ms
            self.last_update = time.get_ticks()
            self.current_frame += 1
            if self.current_frame >= len(self.frames):  # End animation after the last frame
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
explosions = sprite.Group()  # Group to hold explosions

def create_monsters():
    monsters.empty()
    for i in range(enemy_count):
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(enemy_speed, enemy_speed + 3))
        monsters.add(monster)

# Game loop
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

        if not finish:
            window.blit(background, (0, 0))

            text = font2.render("Score: " + str(score), 1, (255, 255, 255))
            window.blit(text, (10, 20))
            text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
            window.blit(text_lose, (10, 50))
            text_goal = font2.render("Goal: " + str(goal), 1, (255, 255, 255))
            window.blit(text_goal, (10, 80))

            ship.update()
            bullets.update()
            monsters.update()
            explosions.update()  # Update explosions

            ship.reset()
            monsters.draw(window)
            bullets.draw(window)
            explosions.draw(window)  # Draw explosions

            collides = sprite.groupcollide(monsters, bullets, True, True)
            for c in collides:
                score += 1
                coins += 5  # Earn coins for shooting enemies
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(enemy_speed, enemy_speed + 3))
                monsters.add(monster)

                # Create an explosion at the enemy's position
                explosion = Explosion(c.rect.x, c.rect.y)
                explosions.add(explosion)

            if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
                finish = True
                window.blit(lose, (200, 200))
                break  

            if score >= goal:
                finish = True
                window.blit(win, (200, 200))
                break

            display.update()
        time.delay(30)

    save_coins()  # Save coins when the game ends

# Start the game
load_coins()  # Load the saved coin value when the game starts
game_loop()  # Start the game directly after loading coins
 