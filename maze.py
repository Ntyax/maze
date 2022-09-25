#створи гру "Лабіринт"!
from pygame import *
import pygame_menu

mixer.init()
font.init()
init()



WIDTH = 900
HEIGHT = 600
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Maze")
font1 = font.SysFont("Impact", 50)
result = font1.render("", True, (0, 255, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, image_name, x, y, width, height):
        super().__init__()
        self.img = transform.scale(image.load(image_name), (width, height))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def draw(self):
        window.blit(self.img, self.rect)

class Player(GameSprite):
    def __init__(self):
        super().__init__("hero.png", 100, 100, 75, 75)
        self.speed = 5
        self.hp = 100

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x<WIDTH-self.width:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y>0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y<HEIGHT-self.height:
            self.rect.y += self.speed


class Enemy(GameSprite):
    def __init__(self, x, y):
        super().__init__("cyborg.png", x, y, 75, 75)
        self.speed = 5
        self.direction = "left"

    def update(self):
        if self.rect.x <= 300:
            self.direction = "right"
        if self.rect.x >= 450:
            self.direction = "left"
        
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, x, y, width, height, color = (255, 113, 31)):
        super().__init__()
        self.img = Surface((width, height))
        self.rect = self.img.get_rect()
        self.img.fill(color)
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
    def draw(self):
        window.blit(self.img, self.rect)

class Treasure(GameSprite):
    def __init__(self):
        super().__init__("treasure.png", WIDTH - 120, HEIGHT - 100, 75, 75)



bg = transform.scale(image.load("background.jpg"), (WIDTH, HEIGHT))

player = Player()
cyborg = Enemy(350, 300)
treasure = Treasure()

wall1 = Wall(50, 50, 20, 500)
wall2 = Wall(70, 50, 770, 20)
wall3 = Wall(200, 70, 20, 150)
wall4 = Wall(840, 50, 20, 500)
wall5 = Wall(200, 220, 200, 20)
walls = [wall1, wall2, wall3, wall4, wall5]


mixer.music.load("jungles.ogg")
mixer.music.set_volume(0.5) #гучність фонової музики
mixer.music.play()

win_sound = mixer.Sound("money.ogg")
kick_sound = mixer.Sound("kick.ogg")

run = False
game = False
clock = time.Clock()
FPS = 60
finish = False

def start_game():
    global run
    run = True
    menu.disable()


menu = pygame_menu.Menu("Maze", 400, 300, theme = pygame_menu.themes.THEME_BLUE)
menu.add.button("Play", start_game)
menu.add.button("Exit", pygame_menu.events.EXIT)
menu.mainloop(window)



while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                menu.enable()
                menu.mainloop(window)

    if not finish:
        player.update()
        cyborg.update()

        if sprite.collide_rect(player, treasure):
            result = font1.render("YOU WIN", True, (0, 255, 0))
            finish = True
            win_sound.play()


        window.blit(bg, (0,0))
        player.draw()
        cyborg.draw()
        for wall in walls:
            wall.draw()
        treasure.draw()
    else:
        window.blit(result, (300, 300))
    display.update()
    clock.tick(FPS)



#оброби подію «клік за кнопкою "Закрити вікно"»