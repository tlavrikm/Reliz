from pygame import *
from random import randint

mixer.init()
mixer_music.load('ggg.mp3')
mixer_music.play()
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

score = 0
goal = 1000
lost = 0
max_lost = 3
coins = 0  # Currency system for purchasing skins
current_skin = img_V1  # The skin the player is currently using

enemy_speed = 3  # Default speed, will be modified based on difficulty
enemy_count = 5  # Default number of enemies

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
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
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

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

bullets = sprite.Group()
ship = Player(current_skin, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()

def create_monsters():
    monsters.empty()
    for i in range(enemy_count):
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(enemy_speed, enemy_speed + 3))
        monsters.add(monster)

# Main menu
def main_menu():
    global enemy_speed, enemy_count, current_skin, coins
    menu_running = True
    while menu_running:
        window.fill((0, 0, 0))
        title = font1.render("SHOOTER GAME", True, (255, 255, 255))
        window.blit(title, (200, 100))

        easy_button = font2.render("Easy", True, (255, 255, 255))
        medium_button = font2.render("Medium", True, (255, 255, 255))
        hard_button = font2.render("Hard", True, (255, 255, 255))

        window.blit(easy_button, (300, 200))
        window.blit(medium_button, (300, 250))
        window.blit(hard_button, (300, 300))

        # Enemy count buttons
        enemy_5_button = font2.render("5 Enemies", True, (255, 255, 255))
        enemy_10_button = font2.render("10 Enemies", True, (255, 255, 255))
        enemy_15_button = font2.render("15 Enemies", True, (255, 255, 255))

        window.blit(enemy_5_button, (300, 350))
        window.blit(enemy_10_button, (300, 400))
        window.blit(enemy_15_button, (300, 450))

        # Skin selection buttons
        skin1_button = font2.render(f"Skin 1 - 0 Coins", True, (255, 255, 255))
        skin2_button = font2.render(f"Skin 2 - 10 Coins", True, (255, 255, 255))
        skin3_button = font2.render(f"Skin 3 - 20 Coins", True, (255, 255, 255))

        window.blit(skin1_button, (500, 200))
        window.blit(skin2_button, (500, 250))
        window.blit(skin3_button, (500, 300))

        # Show the current coins the player has
        coins_text = font2.render(f"Coins: {coins}", True, (255, 255, 255))
        window.blit(coins_text, (500, 400))

        for e in event.get():
            if e.type == QUIT:
                quit()
            if e.type == MOUSEBUTTONDOWN:
                if 300 <= e.pos[0] <= 400:
                    if 200 <= e.pos[1] <= 240:  # Easy
                        enemy_speed = 2
                    elif 250 <= e.pos[1] <= 290:  # Medium
                        enemy_speed = 3
                    elif 300 <= e.pos[1] <= 340:  # Hard
                        enemy_speed = 4
                if 300 <= e.pos[0] <= 400:
                    if 350 <= e.pos[1] <= 390:  # 5 Enemies
                        enemy_count = 5
                    elif 400 <= e.pos[1] <= 440:  # 10 Enemies
                        enemy_count = 10
                    elif 450 <= e.pos[1] <= 490:  # 15 Enemies
                        enemy_count = 15
                # Skin selection and currency check
                if 500 <= e.pos[0] <= 600:
                    if 200 <= e.pos[1] <= 240:  # Skin 1
                        current_skin = img_V1
                    elif 250 <= e.pos[1] <= 290:  # Skin 2
                        if coins >= 10:
                            current_skin = img_V2
                            coins -= 10  # Deduct coins for purchasing
                    elif 300 <= e.pos[1] <= 340:  # Skin 3
                        if coins >= 20:
                            current_skin = img_V3
                            coins -= 20  # Deduct coins for purchasing

                menu_running = False

        display.update()

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

            ship.reset()
            monsters.draw(window)
            bullets.draw(window)

            collides = sprite.groupcollide(monsters, bullets, True, True)
            for c in collides:
                score += 1
                coins += 5  # Earn coins for shooting enemies
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(enemy_speed, enemy_speed + 3))
                monsters.add(monster)

            if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
                finish = True
                window.blit(lose, (200, 200))
                break  

            if score >= goal:
                finish = True
                window.blit(win, (200, 200))
                break

            display.update()
        time.delay(40)

    save_coins()  # Save coins when the game ends

# Start the game
load_coins()  # Load the saved coin value when the game starts
main_menu()  # Show the main menu first
game_loop()  # Start the game after difficulty and enemy count selection

