import pygame, sys, random
from pygame import *
from pygame.locals import *

pygame.init()

pygame.display.set_caption("Nodes")
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

display_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())

def write(blit=True, text='sample text', position=(0, 0), color=(0, 0, 0), fontsize=20, font='arial'):
    font = pygame.font.SysFont(font, fontsize)
    text = font.render(text, True, color)
    if blit:
        screen.blit(text, position)
        rect = text.get_rect()
        rect.topleft = position[0], position[1]
        return rect
    else:
        return text, position

class Character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 64))
        self.image.fill((0, 0, 0))
        self.movement = [0, 0]
        self.rect = self.image.get_rect()
        self.irect = self.rect

        self.hp = 100

    def update(self, **kwargs):
        self.irect.x += self.movement[0]
        self.irect.y += self.movement[1]
        self.rect.x = self.irect.x - scroll[0]
        self.rect.y = self.irect.y - scroll[1]
        self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

PlayerGroup = pygame.sprite.Group()

def gameloop(loadgame=0):
    #region
    global scroll

    player = Character()
    player.add(PlayerGroup)
    player.rect.center = 500, 400
    pygame.mouse.set_pos(500, 400)
    running = True

    scroll = [0, 0]
    
    in_menu = False
    def menu1():
        pygame.draw.rect(screen, (100, 100, 100), (400, 350, 200, 100))
    def menu2():
        pygame.draw.rect(screen, (100, 100, 100), (400, 350, 200, 100))
    def menu3():
        pygame.draw.rect(screen, (100, 100, 100), (400, 350, 200, 100))
    def menu4():
        pygame.draw.rect(screen, (100, 100, 100), (400, 350, 200, 100))
    def status():
        pygame.draw.rect(screen, (0, 0, 0), (100, 350, 800, 100), 1)
        pygame.draw.rect(screen, (100-player.hp, player.hp, 0), (100, 350, player.hp*8, 100))
    #endregion
    while running:
        scroll[0] += (player.irect.x - scroll[0] - (500-16))/20
        scroll[1] += (player.irect.y - scroll[1] - (400-32))/20
        display_rect.x, display_rect.y = scroll[0], scroll[1]
        pygame.display.update(); clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_a or ev.key == pygame.K_s or ev.key == pygame.K_d or ev.key == pygame.K_f:
                    pygame.mouse.set_pos(500, 400)
        screen.fill((255, 255, 255))
        PlayerGroup.update(); PlayerGroup.draw(screen)
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_a]:
            in_menu = True
            menu1()
        if keys_pressed[K_s]:
            in_menu = True
            menu2()
        if keys_pressed[K_d]:
            in_menu = True
            menu3()
        if keys_pressed[K_f]:
            in_menu = True
            menu4()
        if keys_pressed[K_SPACE]:
            in_menu = True
            status()
        mx, my = pygame.mouse.get_pos()
        #region
        if not player.irect.collidepoint(mx, my) and not in_menu:
            if player.irect.right < mx:
                if player.movement[0] < 12:
                    player.movement[0] += (mx - player.irect.right)/1000
            elif player.irect.x > mx:
                if player.movement[0] > -12:
                    player.movement[0] -= (player.irect.x - mx)/1000
            if player.irect.x < mx < player.irect.right:
                player.movement[0] -= 10
                if player.movement[0] <= 0.01:
                    player.movement[0] = 0

            if player.irect.bottom < my:
                if player.movement[1] < 12:
                    player.movement[1] += (my - player.irect.bottom)/1000
            elif player.irect.y > my:
                if player.movement[1] > -12:
                    player.movement[1] -= (player.irect.y - my)/1000
            if player.irect.y < my < player.irect.bottom:
                player.movement[1] -= 10
                if player.movement[1] <= 0.01:
                    player.movement[1] = 0
        else:
            if player.movement[0] <= 0.02:
                player.movement[0] = 0
            if player.movement[1] <= 0.02:
                player.movement[1] = 0
        if in_menu:
            player.movement = [0, 0]
        #endregion
        in_menu = False
        
def mainloop():
    running = True
    while running:
        pygame.display.update(); clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        mx, my = pygame.mouse.get_pos()
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (500-16, 400-32, 32, 64))
        selrects = []
        selrects.append(write(text="Start", position=(50, 550)))
        selrects.append(write(text="Load", position=(50, 600)))
        selrects.append(write(text="Settings", position=(50, 650)))
        selrects.append(write(text="Exit", position=(50, 700)))
        for i in range(len(selrects)):
            if selrects[i].collidepoint(mx, my) and pygame.mouse.get_pressed()[0]:
                if i == 0:
                    gameloop(0)
                if i == 1:
                    gameloop(1)
                if i == 2:
                    pass
                if i == 3:
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__':
    mainloop()