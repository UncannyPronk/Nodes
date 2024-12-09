import pygame, sys, random, winsound
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

class Object(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = "object"
        self.image = pygame.Surface((16, 16))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.irect = self.rect

#region[rgb(0, 50, 15)]
class Tree(Object):
    def __init__(self, x, y):
        Object.__init__(self)
        self.image = pygame.Surface((64, 32))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.irect = self.rect
        self.sprite = self.Sprite(self)
    
    def update(self, **kwargs):
        self.rect.x = self.irect.x - scroll[0]
        self.rect.y = self.irect.y - scroll[1]

    class Sprite(pygame.sprite.Sprite):
        def __init__(self, Tree):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((128, 224))
            self.rect = self.image.get_rect()
            self.image.fill((255, 0, 0))
            self.spriteimg = pygame.image.load("pixel_trees/pixel_trees/pixel_tree_summer.png")
            self.image.blit(pygame.transform.scale(self.spriteimg, (self.rect.w, self.rect.h)), (0, 0))
            self.image.set_colorkey((255, 0, 0))
            self.outer = Tree
        
        def update(self, **kwargs):
            self.rect.x = self.outer.rect.x - 32 - scroll[0]
            self.rect.bottom = self.outer.rect.bottom - scroll[1]
#endregion

#region[rgb(50, 30, 30)]
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = "npc"
        self.image = pygame.Surface((24, 16))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.irect = self.rect
        self.hostile = False
        self.movement = [0, 0]
        self.hp = 100
        self.sprite = self.Sprite(self)

    def update(self, **kwargs):
        self.rect.x = self.irect.x - scroll[0]
        self.rect.y = self.irect.y - scroll[1]
    
    class Sprite(pygame.sprite.Sprite):
        def __init__(self, Player):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((32, 64))
            self.image.fill((0, 0, 0))
            self.rect = self.image.get_rect()
            self.outer = Player
        
        def update(self, **kwargs):
            self.rect.x = self.outer.rect.x - 4 - scroll[0]
            self.rect.bottom = self.outer.rect.bottom - scroll[1]
#endregion

#region[rgb(20, 40, 60)]
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24, 16))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.irect = self.rect
        self.movement = [0, 0]
        self.hp = 100
        self.detectablebyenemies = 0
        self.sprite = self.Sprite(self)

        #short range weapons
        self.inv1 = ["Sword"]
        self.active1 = -1
        #long range weapons
        self.inv2 = ["Gun"]
        self.active2 = -1
        #long range weapons
        self.inv3 = ["Wind"]
        self.active3 = -1

    def update(self, **kwargs):
        self.rect.x = self.irect.x - scroll[0]
        self.rect.y = self.irect.y - scroll[1]
        # self.rect.x = self.sprite.rect.x + 4
        # self.rect.bottom = self.sprite.rect.bottom
    
    class Sprite(pygame.sprite.Sprite):
        def __init__(self, Player):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((32, 64))
            self.image.fill((0, 0, 0))
            self.animationvar = 0
            self.spritesheet = pygame.image.load("8Direction_TopDown_CharacterAssets_ByBossNelNel/8Direction_TopDown_Character Sprites_ByBossNelNel/SpriteSheet.png")
            self.rect = self.image.get_rect()
            # self.irect = self.rect
            self.outer = Player
        
        def update(self, **kwargs):
            if self.animationvar < 8:
                self.animationvar += 0.2
            else:
                self.animationvar = 0
            self.image.fill((0, 255, 0))
            if self.outer.movement[1] > 0:
                if self.outer.movement[0] > 0:
                    #bottom right
                    self.image.blit(pygame.transform.scale(self.spritesheet, (self.rect.w*9, self.rect.h*9)), (0, 0), (int(self.animationvar)*self.rect.w, self.rect.h, self.rect.w, self.rect.h))
                elif self.outer.movement[0] < 0:
                    #bottom left
                    self.image.blit(pygame.transform.scale(self.spritesheet, (self.rect.w*9, self.rect.h*9)), (0, 0), (int(self.animationvar)*self.rect.w, self.rect.h*7, self.rect.w, self.rect.h))
                else:
                    #bottom
                    self.image.blit(pygame.transform.scale(self.spritesheet, (self.rect.w*9, self.rect.h*9)), (0, 0), (int(self.animationvar)*self.rect.w, 0, self.rect.w, self.rect.h))
            elif self.outer.movement[1] < 0:
                if self.outer.movement[0] > 0:
                    #top right
                    self.image.blit(pygame.transform.scale(self.spritesheet, (self.rect.w*9, self.rect.h*9)), (0, 0), (int(self.animationvar)*self.rect.w, self.rect.h*3, self.rect.w, self.rect.h))
                elif self.outer.movement[0] < 0:
                    #top left
                    self.image.blit(pygame.transform.scale(self.spritesheet, (self.rect.w*9, self.rect.h*9)), (0, 0), (int(self.animationvar)*self.rect.w, self.rect.h*5, self.rect.w, self.rect.h))
                else:
                    #top
                    self.image.blit(pygame.transform.scale(self.spritesheet, (self.rect.w*9, self.rect.h*9)), (0, 0), (int(self.animationvar)*self.rect.w, self.rect.h*4, self.rect.w, self.rect.h))
            else:
                if self.outer.movement[0] > 0:
                    #right
                    self.image.blit(pygame.transform.scale(self.spritesheet, (self.rect.w*9, self.rect.h*9)), (0, 0), (int(self.animationvar)*self.rect.w, self.rect.h*2, self.rect.w, self.rect.h))
                elif self.outer.movement[0] < 0:
                    #left
                    self.image.blit(pygame.transform.scale(self.spritesheet, (self.rect.w*9, self.rect.h*9)), (0, 0), (int(self.animationvar)*self.rect.w, self.rect.h*6, self.rect.w, self.rect.h))
                else:
                    #idle
                    self.image.blit(pygame.transform.scale(self.spritesheet, (self.rect.w*9, self.rect.h*9)), (0, 0), (0, 0, self.rect.w, self.rect.h))
            self.image.set_colorkey((0, 255, 0))
            self.rect.x = self.outer.rect.x - 4
            self.rect.bottom = self.outer.rect.bottom
            # self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

#endregion

PlayerGroup = pygame.sprite.Group()
EnemyGroup = pygame.sprite.Group()
ObjectGroup = pygame.sprite.Group()
SpriteGroup = pygame.sprite.Group()

#region[rgb(30, 30, 30)]
def gameloop(loadgame=0):
    #region
    global scroll

    player = Player()
    player.add(PlayerGroup)
    player.sprite.add(SpriteGroup)
    # player.hitbox.add(HitBoxGroup)
    player.sprite.rect.center = 500, 400
    pygame.mouse.set_pos(500, 400)

    enemylist = []
    for i in range(4):
        enemylist.append(Character(random.randint(-800, 800), random.randint(-800, 800)))
    for enemy in enemylist:
        enemy.hostile = True
        enemy.add(EnemyGroup)
        enemy.sprite.add(SpriteGroup)

    trees = []
    for i in range(8):
        trees.append(Tree(random.randint(-800, 800), random.randint(-800, 800)))
    for tree in trees:
        tree.add(ObjectGroup)
        tree.sprite.add(SpriteGroup)
        # print(tree.rect.topleft)

    running = True

    scroll = [0, 0]
    
    in_menu = False

    bg = pygame.Surface((display_rect.w, display_rect.h))
    bg.fill((0, 0, 0))
    bg.set_alpha(0)

    def blit(group):
        order = []
        for item in group:
            order.append(item)
        n = len(order)
        for i in range(n):
            for j in range(0, n-i-1):
                if order[j].outer.rect.y > order[j+1].outer.rect.y:
                    order[j], order[j+1] = order[j+1], order[j]

        for i in range(n):
            screen.blit(order[i].image, order[i].rect)

    #endregion

    #region
    def menu1():
        if bg.get_alpha() < 200:
            bg.set_alpha(bg.get_alpha() + 20)

        screen.blit(bg, (0, 0))
        if player.active1 > -1:
            for i in range(len(player.inv1)):
                if player.active1 == i:
                    pygame.draw.line(screen, (180, 180, 180), (500, 600), (150 + 100*i, 200), 8)
        pygame.draw.rect(screen, (100, 100, 100), (400, 600, 200, 100))
        if Rect(400, 600, 200, 100).collidepoint(pygame.mouse.get_pos()) and player.active1 != -1:
            write(text="Player", position=(425, 610), fontsize=60, color=(255, 255, 255))
            if pygame.mouse.get_pressed()[0]:
                player.active1 = -1
        else:
            write(text="Player", position=(425, 610), fontsize=60)

        for i in range(len(player.inv1)):
            pygame.draw.rect(screen, (140, 100, 100), (50 + 100*i, 200, 200, 100))
            if Rect(50 + 100*i, 200, 200, 100).collidepoint(pygame.mouse.get_pos()):
                write(text=player.inv1[i], position=(75 + 100*i, 210), fontsize=60, color=(255, 255, 255))
                if pygame.mouse.get_pressed()[0]:
                    player.active1 = i
            else:
                write(text=player.inv1[i], position=(75 + 100*i, 210), fontsize=60)
        pygame.draw.line(screen, (255, 255, 255), (500, 600), pygame.mouse.get_pos(), 3)
    def menu2():
        if bg.get_alpha() < 200:
            bg.set_alpha(bg.get_alpha() + 20)

        screen.blit(bg, (0, 0))
        if player.active2 > -1:
            for i in range(len(player.inv2)):
                if player.active2 == i:
                    pygame.draw.line(screen, (180, 180, 180), (500, 600), (150 + 100*i, 200), 8)
        pygame.draw.rect(screen, (100, 100, 100), (400, 600, 200, 100))
        if Rect(400, 600, 200, 100).collidepoint(pygame.mouse.get_pos()) and player.active2 != -1:
            write(text="Player", position=(425, 610), fontsize=60, color=(255, 255, 255))
            if pygame.mouse.get_pressed()[0]:
                player.active2 = -1
        else:
            write(text="Player", position=(425, 610), fontsize=60)

        for i in range(len(player.inv2)):
            pygame.draw.rect(screen, (140, 100, 100), (50 + 100*i, 200, 200, 100))
            if Rect(50 + 100*i, 200, 200, 100).collidepoint(pygame.mouse.get_pos()):
                write(text=player.inv2[i], position=(75 + 100*i, 210), fontsize=60, color=(255, 255, 255))
                if pygame.mouse.get_pressed()[0]:
                    player.active2 = i
            else:
                write(text=player.inv2[i], position=(75 + 100*i, 210), fontsize=60)
        pygame.draw.line(screen, (255, 255, 255), (500, 600), pygame.mouse.get_pos(), 3)
    def menu3():
        if bg.get_alpha() < 200:
            bg.set_alpha(bg.get_alpha() + 20)

        screen.blit(bg, (0, 0))
        if player.active3 > -1:
            for i in range(len(player.inv3)):
                if player.active3 == i:
                    pygame.draw.line(screen, (180, 180, 180), (500, 600), (150 + 100*i, 200), 8)
        pygame.draw.rect(screen, (100, 100, 100), (400, 600, 200, 100))
        if Rect(400, 600, 200, 100).collidepoint(pygame.mouse.get_pos()) and player.active3 != -1:
            write(text="Player", position=(425, 610), fontsize=60, color=(255, 255, 255))
            if pygame.mouse.get_pressed()[0]:
                player.active3 = -1
        else:
            write(text="Player", position=(425, 610), fontsize=60)

        for i in range(len(player.inv3)):
            pygame.draw.rect(screen, (140, 100, 100), (50 + 100*i, 200, 200, 100))
            if Rect(50 + 100*i, 200, 200, 100).collidepoint(pygame.mouse.get_pos()):
                write(text=player.inv3[i], position=(75 + 100*i, 210), fontsize=60, color=(255, 255, 255))
                if pygame.mouse.get_pressed()[0]:
                    player.active3 = i
            else:
                write(text=player.inv3[i], position=(75 + 100*i, 210), fontsize=60)
        pygame.draw.line(screen, (255, 255, 255), (500, 600), pygame.mouse.get_pos(), 3)
    def status():
        if bg.get_alpha() < 200:
            bg.set_alpha(bg.get_alpha() + 20)
        screen.blit(bg, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (100, 350, 800, 100), 1)
        pygame.draw.rect(screen, (100-player.hp, player.hp, int(player.hp/5)), (100, 350, player.hp*8, 100))
        #also show stamina bar and status effects
    #endregion
    while running:
        if player.detectablebyenemies > 0:
            player.detectablebyenemies -= 0.2
        scroll[0] += (player.irect.x - scroll[0] - (500-player.irect.w/2))
        scroll[1] += (player.irect.y - scroll[1] - (400-player.irect.h/2))
        display_rect.x, display_rect.y = scroll[0], scroll[1]
        pygame.display.update(); clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_a or ev.key == pygame.K_s or ev.key == pygame.K_d:
                    pygame.mouse.set_pos(500, 650)
        screen.fill((0, 255, 120))
        blit(SpriteGroup)
        ObjectGroup.update()
        EnemyGroup.update()
        PlayerGroup.update()
        SpriteGroup.update()
        
        mx, my = pygame.mouse.get_pos()
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_SPACE]:
            in_menu = True
            status()
        elif keys_pressed[K_a]:
            in_menu = True
            menu1()
        elif keys_pressed[K_s]:
            in_menu = True
            menu2()
        elif keys_pressed[K_d]:
            in_menu = True
            menu3()
        else:
            in_menu = False
            bg.set_alpha(0)
        player.sprint = False
        if keys_pressed[K_LSHIFT]:
            player.sprint = True
            player.detectablebyenemies = 100
        #region
        if not player.irect.collidepoint(mx, my) and not in_menu:
            if player.irect.right < mx:
                if player.movement[0] < 2:
                    player.movement[0] += (mx - player.irect.center[0])/800
                if player.sprint:
                    if player.movement[0] < 6:
                        player.movement[0] += (mx - player.irect.center[0])/800
                else:
                    if player.movement[0] > 2:
                        player.movement[0] -= 0.5
                # print(mx - player.irect.center[0])
            elif player.irect.x > mx:
                if player.movement[0] > -2:
                    player.movement[0] -= (player.irect.center[0] - mx)/800
                if player.sprint:
                    if player.movement[0] > -6:
                        player.movement[0] -= (player.irect.center[0] - mx)/800
                else:
                    if player.movement[0] < -2:
                        player.movement[0] += 0.5
                # print(player.irect.center[0] - mx)
            else:
                # print(player.movement[0])
                if 2 > player.movement[0] > 0:
                    player.movement[0] -= 0.5
                if -2 < player.movement[0] < 0:
                    player.movement[0] += 0.5
                if player.movement[0] < 0.5 or player.movement[0] > -0.5:
                    player.movement[0] = 0

            if player.irect.bottom < my:
                if player.movement[1] < 2:
                    player.movement[1] += (my - player.irect.center[1])/800
                if player.sprint:
                    if player.movement[1] < 6:
                        player.movement[1] += (my - player.irect.center[1])/800
                else:
                    if player.movement[1] > 2:
                        player.movement[1] -= 0.5
                # print(my - player.irect.center[1])
            elif player.irect.y > my:
                if player.movement[1] > -2:
                    player.movement[1] -= (player.irect.center[1] - my)/800
                if player.sprint:
                    if player.movement[1] > -6:
                        player.movement[1] -= (player.irect.center[1] - my)/800
                else:
                    if player.movement[1] < -2:
                        player.movement[1] += 0.5
                # print(player.irect.center[1] - my)
            else:
                # print(player.movement[1])
                if 2 > player.movement[1] > 0:
                    player.movement[1] -= 0.5
                if -2 < player.movement[1] < 0:
                    player.movement[1] += 0.5
                if player.movement[1] < 0.5 or player.movement[1] > -0.5:
                    player.movement[1] = 0
        else:
            player.movement = [0, 0]
        #endregion
        #region
        pcollside = {"front": False, "back": False, "left": False, "right": False}
        player.irect.x += player.movement[0]
        #region[rgb(72, 0, 0)]
        ecoll = pygame.sprite.spritecollide(player, EnemyGroup, False)
        for coll in ecoll:
            if coll.type == "npc":
                if coll.hostile:
                    # print("enemy detected")
                    # if (pcollside["front"] and player.movement[1] < 0) or (pcollside["back"] and player.movement[1] > 0) or(pcollside["left"] and player.movement[0] < 0) or (pcollside["right"] and player.movement[0] > 0):
                    if player.active1 > -1:
                        coll.hp -= 1
                        # coll.movement[0] = -coll.movement[0]
                        # coll.movement[1] = -coll.mov  ement[1]
                    else:
                        player.hp -= 1
                        # player.movement[0] = -player.movement[0]
                        # player.movement[1] = -player.movement[1]
                    # else:
                    #     player.hp -= 10
                    #     player.movement[0] = -player.movement[0]
                    #     player.movement[1] = -player.movement[1]
                    if coll.hp <= 0:
                        SpriteGroup.remove(coll.sprite)
                        EnemyGroup.remove(coll)
                        break
        #endregion
        pcoll = pygame.sprite.spritecollide(player, ObjectGroup, False)
        for enemy in pygame.sprite.spritecollide(player, EnemyGroup, False):
            pcoll.append(enemy)
        # print(pcoll)
        for coll in pcoll:
            if player.movement[0] > 0:
                pcollside["right"] = True
                player.rect.right = coll.rect.x
            elif player.movement[0] < 0:
                pcollside["left"] = True
                player.rect.x = coll.rect.right

        player.irect.y += player.movement[1]
        #region[rgb(72, 0, 0)]
        ecoll = pygame.sprite.spritecollide(player, EnemyGroup, False)
        for coll in ecoll:
            if coll.type == "npc":
                if coll.hostile:
                    # print("enemy detected")     
                    # if (pcollside["front"] and player.movement[1] < 0) or (pcollside["back"] and player.movement[1] > 0) or(pcollside["left"] and player.movement[0] < 0) or (pcollside["right"] and player.movement[0] > 0):
                    if player.active1 > -1:
                        coll.hp -= 1
                        # coll.movement[0] = -coll.movement[0]
                        # coll.movement[1] = -coll.movement[1]
                    else:
                        player.hp -= 1
                        # player.movement[0] = -player.movement[0]
                        # player.movement[1] = -player.movement[1]
                    # else:
                    #     player.hp -= 10
                    #     player.movement[0] = -player.movement[0]
                    #     player.movement[1] = -player.movement[1]
                    if coll.hp <= 0:
                        SpriteGroup.remove(coll.sprite)
                        EnemyGroup.remove(coll)
                        break
        #endregion
        pcoll = pygame.sprite.spritecollide(player, ObjectGroup, False)
        for enemy in pygame.sprite.spritecollide(player, EnemyGroup, False):
            pcoll.append(enemy)
        # print(pcoll)
        for coll in pcoll:
            if player.movement[1] > 0:
                pcollside["back"] = True
                player.rect.bottom = coll.rect.y
            elif player.movement[1] < 0:
                pcollside["front"] = True
                player.rect.y = coll.rect.bottom
        #endregion

#endregion
        
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
        write(text="NODES", position=(412, 100), fontsize=60)
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
