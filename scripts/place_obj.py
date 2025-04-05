import pygame
import random
from scripts.global_vars import scroll, player
from scripts.char_obj import Character
from scripts.etc_obj import Object

class Village(Object):
    def __init__(self, x, y):
        Object.__init__(self)
        self.image = pygame.Surface((1570, 1536))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.irect = self.rect
        self.houses = []
        self.villagers = []
        self.sprite = self.Sprite(self)

    def update(self, **kwargs):
        self.rect.x = self.irect.x - scroll[0]
        self.rect.y = self.irect.y - scroll[1]
        for villager in self.villagers:
            villager.mv -= random.randint(1, 10)
            if villager.mv <= 0:
                villager.mv = 400
                villager.movement = [random.randint(-1, 1), random.randint(-1, 1)]
            if villager.rect.x < self.sprite.rect.x + 16:
                villager.rect.x = self.sprite.rect.x + 16
                villager.movement[0] = 1
            elif villager.rect.right > self.sprite.rect.right - 16:
                villager.rect.right = self.sprite.rect.right - 16
                villager.movement[0] = -1
            if villager.rect.y < self.sprite.rect.y + 144:
                villager.rect.y = self.sprite.rect.y + 144
                villager.movement[1] = 1
            elif villager.rect.bottom > self.sprite.rect.bottom - 16:
                villager.rect.bottom = self.sprite.rect.bottom - 16
                villager.movement[1] = -1
            # print(villager.mv, " --- ", villager.movement, " - ", villager.sprite.rect.topleft)

            #region[rgba(180, 40, 0, 0.2)]
            vcollside = {"front": False, "back": False, "left": False, "right": False}
            villager.irect.x += villager.movement[0]
            # vcoll = pygame.sprite.spritecollide(villager, self.houses, False)
            vcoll = []
            for house in self.houses:
                if villager.rect.colliderect(house.rect):
                    vcoll.append(house)
                if villager.rect.colliderect(player.rect):
                    vcoll.append(player)
                    # print(house)
            for coll in vcoll:
                if villager.movement[0] > 0:
                    vcollside["right"] = True
                    villager.rect.right = coll.rect.x
                    villager.movement[0] = -1
                elif villager.movement[0] < 0:
                    vcollside["left"] = True
                    villager.rect.x = coll.rect.right
                    villager.movement[0] = 1

            villager.irect.y += villager.movement[1]
            # vcoll = pygame.sprite.spritecollide(villager, self.houses, False)
            vcoll = []
            for house in self.houses:
                if villager.rect.colliderect(house.rect):
                    vcoll.append(house)
                if villager.rect.colliderect(player.rect):
                    vcoll.append(player)
                    # print(house)
            for coll in vcoll:
                if villager.movement[1] > 0:
                    vcollside["back"] = True
                    villager.rect.bottom = coll.rect.y
                    villager.movement[1] = -1
                elif villager.movement[1] < 0:
                    vcollside["front"] = True
                    villager.rect.y = coll.rect.bottom
                    villager.movement[1] = 1
            #endregion
            # villager.rect.x = villager.irect.x
            # villager.rect.y = villager.irect.y
            # villager.sprite.rect.x = villager.rect.x + 4 + scroll[0]
            # villager.sprite.rect.bottom = villager.rect.bottom + scroll[1]

    class Sprite(pygame.sprite.Sprite):
        def __init__(self, Village):
            pygame.sprite.Sprite.__init__(self)
            self.outer = Village
            self.collidable = False
            self.image = pygame.Surface((1570, 1664))
            self.rect = self.image.get_rect()
            self.image.fill((120, 180, 140))
            for i in range(random.randint(4, 8)):
                self.outer.houses.append(self.outer.House(self.outer, self.outer.rect.x + random.randint(0, 25)//5*256 - 16, self.outer.rect.y + random.randint(0, 25)//5*256 + 16 + 256))
            for i in range(len(self.outer.houses)):
                for j in range(len(self.outer.houses)):
                    if i != j:
                        while self.outer.houses[i].rect.colliderect(self.outer.houses[j].rect):
                            self.outer.houses[i].rect.x = self.outer.rect.x + random.randint(0, 25)//5*256 - 16
                            self.outer.houses[i].rect.y = self.outer.rect.y + random.randint(0, 25)//5*256 + 16 + 256
            for i in range(random.randint(6, 12)):
                self.outer.villagers.append(self.outer.Villager(self.outer, random.randint(self.outer.rect.x + 18, self.outer.rect.right - 18), random.randint(self.outer.rect.y + 18, self.outer.rect.bottom - 18)))
            for villager in self.outer.villagers:
                while villager.rect.collidelist(self.outer.houses):
                        villager.rect.x = random.randint(self.outer.rect.x + 18, self.outer.rect.right - 18)
                        villager.rect.y = random.randint(self.outer.rect.y + 18, self.outer.rect.bottom - 18)
            for i in range(len(self.outer.villagers)):
                for j in range(len(self.outer.villagers)):
                    if i != j:
                        while self.outer.villagers[i].rect.colliderect(self.outer.villagers[j].rect):
                            self.outer.villagers[i].rect.x = random.randint(self.outer.rect.x + 18, self.outer.rect.right - 18)
                            self.outer.villagers[i].rect.y = random.randint(self.outer.rect.y + 18, self.outer.rect.bottom - 18)
            self.image.set_alpha(160)
        
        def update(self, **kwargs):
            self.rect.x = self.outer.rect.x - 32 - scroll[0]
            self.rect.y = self.outer.rect.y + 256 - scroll[1]
            for villager in self.outer.villagers:
                villager.rect.x = villager.irect.x - scroll[0]
                villager.rect.y = villager.irect.y - scroll[1]
                villager.sprite.rect.x = villager.rect.x - 4
                villager.sprite.rect.bottom = villager.rect.bottom
            for house in self.outer.houses:
                house.rect.x = house.irect.x - scroll[0]
                house.rect.y = house.irect.y - scroll[1]
                house.sprite.rect.x = house.rect.x - 16
                house.sprite.rect.bottom = house.rect.bottom
            self.image.fill((120, 180, 140))
            pygame.draw.rect(self.image, (255, 200, 0), (0, 0, self.rect.width, self.rect.height), 16)
            # for house in self.outer.houses:
            #     pygame.draw.rect(self.image, (255, 0, 0), house.sprite.rect)
            # for villager in self.outer.villagers:
            #     pygame.draw.rect(self.image, (0, 0, 20), villager.sprite.rect)

    class House(Object):
        def __init__(self, Village, x, y):
            Object.__init__(self)
            self.village = Village
            self.image = pygame.Surface((224, 256))
            self.image.fill((255, 255, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.irect = self.rect
            self.sprite = self.Sprite(self)
        
        # def update(self, **kwargs):
        #     self.rect.x = self.irect.x - scroll[0]
        #     self.rect.y = self.irect.y - scroll[1]

        class Sprite(pygame.sprite.Sprite):
            def __init__(self, House):
                pygame.sprite.Sprite.__init__(self)
                self.outer = House
                self.image = pygame.Surface((256, 384))
                self.rect = self.image.get_rect()
                # self.rect.x = self.outer.rect.x
                # self.rect.y = self.outer.rect.y
                # self.image.fill((255, 0, 0))
                self.spriteimg = pygame.image.load("house.png")
                self.image.blit(pygame.transform.scale(self.spriteimg, (self.rect.w, self.rect.h)), (0, 0))
                key = self.spriteimg.get_at((0, 0))
                self.image.set_colorkey(key)
            
            # def update(self, **kwargs):
            #     self.rect.x = self.outer.rect.x
            #     self.rect.y = self.outer.rect.bottom - 128
    class Villager(Character):
        def __init__(self, Village, x, y):
            Character.__init__(self, x, y)
            self.village = Village
            self.image = pygame.Surface((24, 16))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.irect = self.rect
            self.movement = [0, 0]
            self.hp = 100
            self.detectablebyenemies = 0
            self.sprite = self.Sprite(self)
            self.mv = 0
            self.id = None

        class Sprite(pygame.sprite.Sprite):
            def __init__(self, Villager):
                pygame.sprite.Sprite.__init__(self)
                self.outer = Villager
                self.image = pygame.Surface((32, 64))
                self.color = (0, 80, 255)
                self.image.fill(self.color)
                self.rect = self.image.get_rect()
                self.rect.x = self.outer.rect.x
                self.rect.y = self.outer.rect.y
            
            # def update(self, **kwargs):
            #     self.rect.x = self.outer.rect.x - 4 - scroll[0]
            #     self.rect.bottom = self.outer.rect.bottom - scroll[1]
#endregion

#region[rgba(60, 40, 0, 1)]
class LoreVillage(Village):
    def __init__(self, x, y):
        Village.__init__(self, x, y)
        self.image = pygame.Surface((1570, 1536))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.blocksize = self.image.get_width()/64, self.image.get_height()/16
        self.irect = self.rect
        self.houses = []
        self.villagers = []
        self.sprite = self.Sprite(self)
        with open("village_map1.txt", "r") as mapfile:
            text = mapfile.readlines()
            self.struct = []
            for line in text:
                linelist = []
                for item in line:
                    if item != "\n":
                        linelist.append(int(item))
                self.struct.append(linelist)
        for y in range(len(self.struct)):
            for x in range(len(self.struct[y])):
                if self.struct[y][x] == 1:
                    pass
                elif self.struct[y][x] == 2:
                    self.houses.append(self.House(self, self.rect.x + (x*self.blocksize[0]), self.rect.y + (y*self.blocksize[1])))
                elif self.struct[y][x] == 3:
                    self.villagers.append(self.Villager(self, self.rect.x + (x*self.blocksize[0]), self.rect.y + (y*self.blocksize[1])))


    class Sprite(pygame.sprite.Sprite):
        def __init__(self, LoreVillage):
            pygame.sprite.Sprite.__init__(self)
            self.outer = LoreVillage
            self.collidable = False
            self.image = pygame.Surface((1570, 1664))
            self.rect = self.image.get_rect()
            self.image.fill((120, 180, 140))
            self.image.set_alpha(160)
        
        def update(self, **kwargs):
            self.rect.x = self.outer.rect.x - 32 - scroll[0]
            self.rect.y = self.outer.rect.y + 256 - scroll[1]
            for villager in self.outer.villagers:
                villager.rect.x = villager.irect.x - scroll[0]
                villager.rect.y = villager.irect.y - scroll[1]
                villager.sprite.rect.x = villager.rect.x - 4
                villager.sprite.rect.bottom = villager.rect.bottom
            for house in self.outer.houses:
                house.rect.x = house.irect.x - scroll[0]
                house.rect.y = house.irect.y - scroll[1]
                house.sprite.rect.x = house.rect.x - 16
                house.sprite.rect.bottom = house.rect.bottom
            self.image.fill((120, 180, 140))
            pygame.draw.rect(self.image, (255, 200, 0), (0, 0, self.rect.width, self.rect.height), 16)