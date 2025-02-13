import pygame, sys, random, time as t, winsound
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

PlayerGroup = pygame.sprite.Group()
EnemyGroup = pygame.sprite.Group()
ObjectGroup = pygame.sprite.Group()
VillageGroup = pygame.sprite.Group()
SpriteGroup = pygame.sprite.Group()
NPCGroup = pygame.sprite.Group()

name_dict = {}

speech_bool = False
dialogue_list = []
s_entity = None
speech_index = 0
prevkey = pygame.key.get_pressed()
dialoguestr = ""
dialogueindex = 0

dialogue_end = False

ruined_talked = False

# timer = 300
def speech_engine(player, entity, dialogues):
    global speech_bool, dialogue_list, s_entity, speech_index, prevkey, dialogueindex, dialoguestr, dialogue_end
    keypress = True
    if entity.interacted > 0:
        try:
            dialoguelen = len(dialogues[speech_index][1])
            #region
            if dialogueindex < dialoguelen:
                # dialogueindex += 1
                # winsound.Beep(800, 200)
                dialogueindex = round((lambda dialogueindex:dialogueindex + 1)(dialogueindex), 1)
                if dialogueindex == float(int(dialogueindex)):
                    # print(dialogueindex)
                    winsound.Beep(600, 80)
            dialoguestr = ""
            for i in range(int(dialogueindex)):
                dialoguestr += dialogues[speech_index][1][i]
            #endregion
            if not dialogues[speech_index][0] in name_dict.keys():
                name_dict[dialogues[speech_index][0]] = (random.randint(120, 255), random.randint(120, 255), random.randint(120, 255))
            color = name_dict[dialogues[speech_index][0]]

            player.movement = [0, 0]
            if not s_entity == None:
                s_entity.movement = [0, 0]
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, display_rect.w, 100))
            # write(True, dialogues[speech_index][1], (100, 20), color, 50)
            write(True, dialoguestr, (100, 20), color, 50)
            write(True, "Press Enter", (display_rect.w - 100, 60), (255, 255, 255))
            if dialogues[speech_index][0] == "player":
                screen.blit(player.sprite.image, (30, 10))
            else:
                screen.blit(entity.sprite.image, (30, 10))
        except IndexError:
            entity.interacted = 0
            speech_bool = False
            s_entity = None
            dialogue_list = []
            speech_index = 0

        # for ev in pygame.event.get():
        #     if ev.type == KEYDOWN and ev.key == K_RETURN:
        #         speech_index += 1
        if keypress:
            keyspressed = pygame.key.get_pressed()
            if keyspressed[K_RETURN] and not prevkey[K_RETURN]:
                if dialogueindex == dialoguelen:
                    speech_index += 1
                    dialogueindex = 0
                    keypress = False
                else:
                    dialogueindex = dialoguelen
                    keypress = False
            # keyspressed = pygame.key.get_pressed()
            if not keyspressed[K_RETURN] and prevkey[K_RETURN]:
                keypress = True
            prevkey = keyspressed

        if speech_index > len(dialogues):
            if entity.interacted > 0:
                entity.interacted -= 1
            if player.rect.centerx < entity.rect.centerx:
                player.rect.right = entity.rect.x - 10
            else:
                player.rect.x = entity.rect.right + 10
            speech_bool = False
            s_entity = None
            dialogue_list = []
            speech_index = 0
            dialogue_end = True

def npc_dialogues(entity):
    global ruined_talked
    if entity.id == None:
        dialogue_list = [["player", "Hello there!"], ["npc", "Hello to you too!"]]
    elif entity.id == "ruined":
        ruined_talked = True
        dialogue_list = [["ruined", "The war has been really tough for all of us."], ["player", "What's wrong, old man?"], ["player", "Anything I can help with?"], ["ruined", "What is a kid like you"], ["ruined", "gonna do to stop a war?"]]
    elif entity.id == "country":
        if ruined_talked:
            dialogue_list = [["country", "Someone needs to stop this war."], ["player", "Yeah? How is that gonna happen?"], ["country", "For starters, one of us can go mess up"], ["country", "the country we are fighting... from inside."], ["player", "Right. Got it."]]
        else:
            dialogue_list = [["country", "I'm too old to fight."], ["player", "You can take a back seat."], ["player", "I'll handle this."], ["country", "You're just a kid..."], ["country", "Talk to that other guy in that back"], ["country", "He will tell you that this"], ["country", "ain't no child's game."]]
            entity.interacted = 1
            player.rect.x += 10
    elif entity.id == "guide1":
        dialogue_list = [["guide1", "You appear to be lost."], ["player", "I'm not exactly lost..."], ["player", "but I am low on resources."], ["guide1", "Keep heading EAST till you find a village."], ["guide1", "Salvation is nearing us..."], ["player", "What?"], ["guide1", "Nothing. Keep heading EAST."]]

    return dialogue_list

bg = pygame.Surface((display_rect.w, display_rect.h))
bg.fill((0, 0, 0))
bg.set_alpha(0)
remaining_missions = ["attack nearby country"]
finished_missions = []
def new_mission(mission=None):
    if not mission in finished_missions:
        if bg.get_alpha() < 255:
            bg.set_alpha(bg.get_alpha() + 5)
        running = True
        while running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    running = False
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RETURN:
                        running = False

            screen.blit(bg, (0, 0))
            pygame.draw.rect(screen, (255, 255, 0), (display_rect.centerx - 300, display_rect.centery - 200, 600, 400))
            pygame.display.flip()
        finished_missions.append(mission)
        remaining_missions.remove(mission)

#region[rgba(0, 0, 0, 0.6)]
class Object(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = "object"
        self.image = pygame.Surface((16, 16))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.irect = self.rect
#endregion

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
#endregion

#region[rgba(100, 100, 0, 0.4)]
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
                self.image.fill((0, 80, 255))
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
            # for house in self.outer.houses:
            #     pygame.draw.rect(self.image, (255, 0, 0), house.sprite.rect)
            # for villager in self.outer.villagers:
            #     pygame.draw.rect(self.image, (0, 0, 20), villager.sprite.rect)



#endregion

#region[rgb(20, 40, 60)]
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24, 16))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.irect = self.rect
        self.detectrect = Rect(self.rect.x - 8, self.rect.y - 8, self.rect.width + 16, self.rect.height + 16)
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

#endregion

#region[rgb(30, 30, 30)]
def gameloop(loadgame=0):
    #region
    global scroll, player
    global speech_bool, dialogue_list, s_entity

    player = Player()
    player.add(PlayerGroup)
    player.sprite.add(SpriteGroup)
    # player.hitbox.add(HitBoxGroup)
    player.sprite.rect.center = 500, 400
    pygame.mouse.set_pos(500, 400)

    lore1v = LoreVillage(3000, -800)
    lore1v.add(VillageGroup)
    lore1v.sprite.add(SpriteGroup)
    lore1v.villagers[1].id = "ruined"
    lore1v.villagers[3].id = "country"
    lore1v.villagers[3].id = "country"

    guide1 = Character(100, 0)
    guide1.add(NPCGroup)
    guide1.sprite.add(SpriteGroup)
    guide1.sprite.image.fill((255, 255, 0))
    guide1.id = "guide1"

    # for houses in village.houses:
    #     houses.sprite.add(SpriteGroup)
    # for villager in village.villagers:
    #     villager.sprite.add(SpriteGroup)


    enemylist = []
    for i in range(4):
        x = random.randint(-800, 800)
        y = random.randint(-800, 800)
        for village in VillageGroup:
            while village.rect.colliderect(Rect(x, y, 32, 64)):
                x = random.randint(-800, 800)
                y = random.randint(-800, 800)
        enemylist.append(Character(x, y))

    for enemy in enemylist:
        enemy.hostile = True
        enemy.id = "enemy"
        enemy.add(EnemyGroup)
        enemy.sprite.add(SpriteGroup)

    trees = []
    for i in range(8):
        x = random.randint(-800, 800)
        y = random.randint(-800, 800)
        for village in VillageGroup:
            while village.rect.colliderect(Rect(x, y, 128, 244)):
                x = random.randint(-800, 800)
                y = random.randint(-800, 800)
        trees.append(Tree(x, y))

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
            # print(type(item.outer))
            if type(item.outer) == Village or type(item.outer) == LoreVillage:
                for house in item.outer.houses:
                    order.append(house.sprite)
                for villager in item.outer.villagers:
                    order.append(villager.sprite)
            # else:
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
                    pygame.draw.line(screen, (180, 180, 180), (500, 600), (150 + 300*i, 200), 8)
        pygame.draw.rect(screen, (100, 100, 100), (400, 600, 200, 100))
        if Rect(400, 600, 200, 100).collidepoint(pygame.mouse.get_pos()) and player.active1 != -1:
            write(text="Player", position=(425, 610), fontsize=60, color=(255, 255, 255))
            if pygame.mouse.get_pressed()[0]:
                player.active1 = -1
        else:
            write(text="Player", position=(425, 610), fontsize=60)

        for i in range(len(player.inv1)):
            pygame.draw.rect(screen, (140, 100, 100), (50 + 300*i, 200, 200, 100))
            if Rect(50 + 100*i, 200, 200, 100).collidepoint(pygame.mouse.get_pos()):
                write(text=player.inv1[i], position=(75 + 300*i, 210), fontsize=60, color=(255, 255, 255))
                if pygame.mouse.get_pressed()[0]:
                    player.active1 = i
            else:
                write(text=player.inv1[i], position=(75 + 300*i, 210), fontsize=60)
        pygame.draw.line(screen, (255, 255, 255), (500, 600), pygame.mouse.get_pos(), 3)
    def menu2():
        if bg.get_alpha() < 200:
            bg.set_alpha(bg.get_alpha() + 20)

        screen.blit(bg, (0, 0))
        if player.active2 > -1:
            for i in range(len(player.inv2)):
                if player.active2 == i:
                    pygame.draw.line(screen, (180, 180, 180), (500, 600), (150 + 300*i, 200), 8)
        pygame.draw.rect(screen, (100, 100, 100), (400, 600, 200, 100))
        if Rect(400, 600, 200, 100).collidepoint(pygame.mouse.get_pos()) and player.active2 != -1:
            write(text="Player", position=(425, 610), fontsize=60, color=(255, 255, 255))
            if pygame.mouse.get_pressed()[0]:
                player.active2 = -1
        else:
            write(text="Player", position=(425, 610), fontsize=60)

        for i in range(len(player.inv2)):
            pygame.draw.rect(screen, (140, 100, 100), (50 + 300*i, 200, 200, 100))
            if Rect(50 + 100*i, 200, 200, 100).collidepoint(pygame.mouse.get_pos()):
                write(text=player.inv2[i], position=(75 + 300*i, 210), fontsize=60, color=(255, 255, 255))
                if pygame.mouse.get_pressed()[0]:
                    player.active2 = i
            else:
                write(text=player.inv2[i], position=(75 + 300*i, 210), fontsize=60)
        pygame.draw.line(screen, (255, 255, 255), (500, 600), pygame.mouse.get_pos(), 3)
    def menu3():
        if bg.get_alpha() < 200:
            bg.set_alpha(bg.get_alpha() + 20)

        screen.blit(bg, (0, 0))
        if player.active3 > -1:
            for i in range(len(player.inv3)):
                if player.active3 == i:
                    pygame.draw.line(screen, (180, 180, 180), (500, 600), (150 + 300*i, 200), 8)
        pygame.draw.rect(screen, (100, 100, 100), (400, 600, 200, 100))
        if Rect(400, 600, 200, 100).collidepoint(pygame.mouse.get_pos()) and player.active3 != -1:
            write(text="Player", position=(425, 610), fontsize=60, color=(255, 255, 255))
            if pygame.mouse.get_pressed()[0]:
                player.active3 = -1
        else:
            write(text="Player", position=(425, 610), fontsize=60)

        for i in range(len(player.inv3)):
            pygame.draw.rect(screen, (140, 100, 100), (50 + 300*i, 200, 200, 100))
            if Rect(50 + 300*i, 200, 200, 100).collidepoint(pygame.mouse.get_pos()):
                write(text=player.inv3[i], position=(75 + 300*i, 210), fontsize=60, color=(255, 255, 255))
                if pygame.mouse.get_pressed()[0]:
                    player.active3 = i
            else:
                write(text=player.inv3[i], position=(75 + 300*i, 210), fontsize=60)
        pygame.draw.line(screen, (255, 255, 255), (500, 600), pygame.mouse.get_pos(), 3)
    def status():
        if bg.get_alpha() < 200:
            bg.set_alpha(bg.get_alpha() + 20)
        screen.blit(bg, (0, 0))
        #region
        #hp
        pygame.draw.rect(screen, (0, 0, 0), (100, 350, 800, 100), 1)
        pygame.draw.rect(screen, (100-player.hp, player.hp, int(player.hp/5)), (100, 350, player.hp*8, 100))
        #endregion

        #region
        #stamina
        pygame.draw.rect(screen, (0, 0, 0), (100, 500, 300, 30), 1)
        if player.stamina/300*100 > 20:
            pygame.draw.rect(screen, (255, 255, 0), (100, 500, player.stamina, 30))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (100, 500, player.stamina, 30))
        #endregion

        #region
        #status effects
        if player.paralysis:
            pygame.draw.rect(screen, (255, 160, 0), (450, 500, 75, 50))
        else:
            pygame.draw.rect(screen, (60, 40, 0), (450, 500, 75, 50))
        write(True, "Par", (465, 505), fontsize=32)

        if player.poisoning:
            pygame.draw.rect(screen, (255, 0, 160), (575, 500, 75, 50))
        else:
            pygame.draw.rect(screen, (60, 0, 40), (575, 500, 75, 50))
        write(True, "Psg", (590, 505), fontsize=32)
        
        if player.burning:
            pygame.draw.rect(screen, (255, 80, 0), (700, 500, 75, 50))
        else:
            pygame.draw.rect(screen, (60, 20, 0), (700, 500, 75, 50))
        write(True, "Brn", (715, 505), fontsize=32)

        if player.sleep:
            pygame.draw.rect(screen, (160, 160, 160), (825, 500, 75, 50))
        else:
            pygame.draw.rect(screen, (40, 40, 40), (825, 500, 75, 50))
        write(True, "Slp", (840, 505), fontsize=32)
        #endregion

        #also show stamina bar and status effects
    #endregion
    while running:
        if player.detectablebyenemies > 0:
            player.detectablebyenemies -= 0.2
        # for enemy in EnemyGroup:
        #     if enemy.hostile:
        #         p_distance = math.sqrt((enemy.rect.x - player.rect.x)**2 + (enemy.rect.y - player.rect.y)**2)
        #         if p_distance < 10:
        #             if enemy.rect.centerx < player.rect.centerx:
        #                 enemy.rect.x += 1
        #             elif enemy.rect.centerx > player.rect.centerx:
        #                 enemy.rect.x -= 1
        #             if enemy.rect.centery < player.rect.centery:
        #                 enemy.rect.y += 1
        #             elif enemy.rect.centery > player.rect.centery:
        #                 enemy.rect.y -= 1
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
        VillageGroup.update()
        SpriteGroup.update()
        NPCGroup.update()
        
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
        if keys_pressed[K_LSHIFT] and player.stamina > 0 and not player.poisoning:
            player.sprint = True
            player.stamina -= 1
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
                        # speech_engine(player, coll, [["player", "Haha eat this!"], ["enemy", "Ouch! you will pay for this."], ["player", "Let's see about that"], ["enemy", "Grrrrrr..."]])
                        speech_bool = True
                        s_entity = coll
                        dialogue_list = [["player", "Haha eat this!"], ["enemy", "Ouch! you will pay for this."], ["player", "Let's see about that"], ["enemy", "Grrrrrr..."]]

                        # coll.movement[0] = -coll.movement[0]
                        # coll.movement[1] = -coll.mov  ement[1]
                    else:
                        player.hp -= 1
                        # speech_engine(player, coll, [["player", "Ouch!"], ["enemy", "Get lost!"], ["player", "I'll come back for you."], ["enemy", "..."]])
                        speech_bool = True
                        s_entity = coll
                        dialogue_list = [["player", "Ouch!"], ["enemy", "Get lost!"], ["player", "I'll come back for you."], ["enemy", "..."]]

                        # player.paralysis = True
                        # player.poisoning = True
                        # player.burning = True

                        # if player.rect.x > coll.rect.x:
                        #     coll.rect.x += 2
                        # elif player.rect.x < coll.rect.x:
                        #     coll.rect.x -= 2

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
        for village in VillageGroup:
            for house in village.houses:
                if house.rect.colliderect(player.rect):
                    pcoll.append(house)
            for villager in village.villagers:
                if villager.rect.colliderect(player.rect):
                    pcoll.append(villager)
                if villager.rect.colliderect(player.detectrect):
                    # speech_engine(player, villager, [["player", "Hello there!"], ["villager", "Hello to you too!"]])
                    speech_bool = True
                    s_entity = villager
                    dialogue_list = npc_dialogues(villager)
        for npc in NPCGroup:
            if npc.rect.colliderect(player.rect):
                pcoll.append(npc)
            if npc.rect.colliderect(player.detectrect):
                speech_bool = True
                s_entity = npc
                dialogue_list = npc_dialogues(npc)
                
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
                        # speech_engine(player, coll, [["player", "Haha eat this!"], ["enemy", "Ouch! you will pay for this."], ["player", "Let's see about that"], ["enemy", "Grrrrrr..."]])
                        speech_bool = True
                        s_entity = coll
                        dialogue_list = [["player", "Haha eat this!"], ["enemy", "Ouch! you will pay for this."], ["player", "Let's see about that"], ["enemy", "Grrrrrr..."]]

                        # coll.movement[0] = -coll.movement[0]
                        # coll.movement[1] = -coll.movement[1]
                    else:
                        player.hp -= 1
                        # speech_engine(player, coll, [["player", "Ouch!"], ["enemy", "Get lost!"], ["player", "I'll come back for you."], ["enemy", "..."]])
                        speech_bool = True
                        s_entity = coll
                        dialogue_list = [["player", "Ouch!"], ["enemy", "Get lost!"], ["player", "I'll come back for you."], ["enemy", "..."]]

                        # player.paralysis = True
                        # player.poisoning = True
                        # player.burning = True

                        # if player.rect.y > coll.rect.y:
                        #     coll.rect.y += 2
                        # elif player.rect.y < coll.rect.y:
                        #     coll.rect.y -= 2

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
        for village in VillageGroup:
            for house in village.houses:
                if house.rect.colliderect(player.rect):
                    pcoll.append(house)
            for villager in village.villagers:
                if villager.rect.colliderect(player.rect):
                    pcoll.append(villager)
                if villager.rect.colliderect(player.detectrect):
                    # speech_engine(player, villager, [["player", "Hello there!"], ["villager", "Hello to you too!"]])
                    speech_bool = True
                    s_entity = villager
                    dialogue_list = npc_dialogues(villager)
        for npc in NPCGroup:
            if npc.rect.colliderect(player.rect):
                pcoll.append(npc)
            if npc.rect.colliderect(player.detectrect):
                speech_bool = True
                s_entity = npc
                dialogue_list = npc_dialogues(npc)
        # print(pcoll)
        for coll in pcoll:
            if player.movement[1] > 0:
                pcollside["back"] = True
                player.rect.bottom = coll.rect.y
            elif player.movement[1] < 0:
                pcollside["front"] = True
                player.rect.y = coll.rect.bottom
        if speech_bool:
            global dialogue_end
            speech_engine(player, s_entity, dialogue_list)
            if dialogue_end:
                try:
                    if s_entity.id == "country":
                        try:
                            new_mission(remaining_missions[0])
                        except IndexError:
                            pass
                except AttributeError:
                    speech_bool = False
                dialogue_end = False   # debug this in the next stream.

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
