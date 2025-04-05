import pygame
from scripts.global_vars import screen, scroll
from scripts.funcs import write

class Node():
    def __init__(self, name, type, id, desc):
        self.name = name
        self.type = type
        self.description = desc
        self.sprite = None
        self.id = id
    def show(self, x, y):
        self.sprite = pygame.Surface((64, 64))
        self.sprite.fill((255, 255, 255))
        self.sprite.set_alpha(200)
        screen.blit(self.sprite, (x, y))
        write(True, self.name, (x + 10, y + 10), (0, 0, 0), 20)
        write(True, self.description, (x + 10, y + 40), (0, 0, 0), 15)

class Object(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = "object"
        self.image = pygame.Surface((16, 16))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.irect = self.rect

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
            self.collidable = True
            self.rect = self.image.get_rect()
            self.image.fill((255, 0, 0))
            self.spriteimg = pygame.image.load("pixel_trees/pixel_trees/pixel_tree_summer.png")
            self.image.blit(pygame.transform.scale(self.spriteimg, (self.rect.w, self.rect.h)), (0, 0))
            self.image.set_colorkey((255, 0, 0))
            self.outer = Tree
        
        def update(self, **kwargs):
            self.rect.x = self.outer.rect.x - 32 - scroll[0]
            self.rect.bottom = self.outer.rect.bottom - scroll[1]