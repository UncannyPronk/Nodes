import pygame
from pygame.locals import *
from scripts.global_vars import display_rect, screen, scroll
from scripts.etc_obj import Node

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = "npc"
        self.image = pygame.Surface((24, 16))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.attackrect = Rect(self.rect.x - 10, self.rect.y - 10, self.rect.width + 20, self.rect.height + 20)
        self.irect = self.rect
        self.hostile = False
        self.interacted = 1
        self.movement = [0, 0]
        self.hp = 100
        self.id = None
        self.sprite = self.Sprite(self)

    def update(self, **kwargs):
        self.rect.x = self.irect.x - scroll[0]
        self.rect.y = self.irect.y - scroll[1]
    
    class Sprite(pygame.sprite.Sprite):
        def __init__(self, Character):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((32, 64))
            self.collidable = True
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()
            self.outer = Character
        
        def update(self, **kwargs):
            self.rect.x = self.outer.rect.x - 4 - scroll[0]
            self.rect.bottom = self.outer.rect.bottom - scroll[1]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24, 16))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.irect = self.rect
        self.detectrect = Rect(self.rect.x - 8, self.rect.y - 8, self.rect.width + 16, self.rect.height + 16)
        self.attackrect = Rect(self.rect.x - 10, self.rect.y - 10, self.rect.width + 20, self.rect.height + 20)
        self.movement = [0, 0]
        self.hp = 100
        self.detectablebyenemies = 0
        self.stamina = 300
        self.poisoning = False
        self.paralysis = False
        self.paralysis_time = 300
        self.burning = False
        self.sleep = False ### implement later
        self.sprite = self.Sprite(self)

        #short range weapons
        self.inv1 = ["Sword"]
        self.active1 = -1
        #long range weapons
        self.inv2 = ["Gun"]
        self.active2 = -1
        #long range weapons
        self.inv3 = ["Wind", "Build"]
        self.active3 = -1
        self.nodegraph = self.NodeGraph()

    def update(self, **kwargs):
        self.rect.x = self.irect.x - scroll[0]
        self.rect.y = self.irect.y - scroll[1]
        self.detectrect.x = self.rect.x - 8
        self.detectrect.y = self.rect.y - 8
        if self.movement == [0, 0] and self.stamina < 300:
            self.stamina += 1
        
        #region
        self.stamina = 300 #remove after production
        #endregion

        if self.paralysis:
            self.paralysis_time -= 1
            self.movement = [0, 0]
            if self.paralysis_time == 0:
                self.paralysis_time = 300
                self.paralysis = False
        if self.poisoning or self.burning:
            if self.sprite.animationvar == 0:
                self.hp -= 1
    
    class Sprite(pygame.sprite.Sprite):
        def __init__(self, Player):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((32, 64))
            self.collidable = True
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
    class NodeGraph():
        def __init__(self):
            self.nodes = [Node("Sword","w", 0, "A simple sword"), Node("Gun","p", 1, "A simple gun"), Node("Wind","m", 2, "wind magic"), Node("Fire","m", 3, "fire magic")]
            self.nodesobt = [0, 1, 2]
            self.nodeconnections = []
            self.activenodeinner = 0
            self.activenodeouter = 0
            self.innernodes = [Node("Player","", -1, "")]

            self.outerspace = pygame.Surface((display_rect.w, display_rect.h))
            self.outerspace.fill((200, 200, 200))
            self.outerspace.set_alpha(200)

            self.innerspace = pygame.Surface((display_rect.w - 152, display_rect.h - 152))
            self.innerspace.fill((100, 100, 100))
            self.innerspace.set_alpha(180)
        
        def show(self, joystick):
            screen.blit(self.outerspace, (0, 0))
            screen.blit(self.innerspace, (76, 76))
            for i in range(len(self.nodesobt)):
                self.nodes[self.nodesobt[i]].show(6 + 76*i, 6)