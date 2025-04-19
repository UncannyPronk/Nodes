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

def reset():
    global speech_bool, dialogue_list, s_entity, speech_index, dialoguestr, dialogueindex, dialogue_end, ruined_talked, name_dict, remaining_missions, finished_missions, PlayerGroup, EnemyGroup, ObjectGroup, VillageGroup, SpriteGroup, NPCGroup, ArenaGroup
    PlayerGroup = pygame.sprite.Group()
    EnemyGroup = pygame.sprite.Group()
    ObjectGroup = pygame.sprite.Group()
    VillageGroup = pygame.sprite.Group()
    SpriteGroup = pygame.sprite.Group()
    NPCGroup = pygame.sprite.Group()
    ArenaGroup = pygame.sprite.Group()

    name_dict = {}

    speech_bool = False
    dialogue_list = []
    s_entity = None
    speech_index = 0
    dialoguestr = ""
    dialogueindex = 0

    dialogue_end = False

    ruined_talked = False

    remaining_missions = ["attack nearby country"]
    finished_missions = []

reset()

pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    prevkey = pygame.joystick.Joystick(0).get_button(0)
else:
    prevkey = pygame.key.get_pressed()

def speech_engine(player, entity, dialogues):
    global speech_bool, dialogue_list, s_entity, speech_index, prevkey, dialogueindex, dialoguestr, dialogue_end, phase
    keypress = True
    if entity.interacted > 0:
        try:
            dialoguelen = len(dialogues[speech_index][1])
            if dialogueindex < dialoguelen:
                dialogueindex = round((lambda dialogueindex:dialogueindex + 1)(dialogueindex), 1)
                if dialogueindex == float(int(dialogueindex)):
                    winsound.Beep(600, 80)
            dialoguestr = ""
            for i in range(int(dialogueindex)):
                dialoguestr += dialogues[speech_index][1][i]
            if not dialogues[speech_index][0] in name_dict.keys():
                name_dict[dialogues[speech_index][0]] = (random.randint(120, 255), random.randint(120, 255), random.randint(120, 255))
            color = name_dict[dialogues[speech_index][0]]

            player.movement = [0, 0]
            if not s_entity == None:
                s_entity.movement = [0, 0]
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, display_rect.w, 100))
            write(True, dialoguestr, (100, 20), color, 42)
            write(True, "Press Enter", (display_rect.w - 150, 60), (255, 255, 255))
            if dialogues[speech_index][0] == "player":
                screen.blit(player.sprite.image, (30, 10))
            else:
                screen.blit(entity.sprite.image, (30, 10))
        except IndexError:
            if entity.id != "country":
                entity.interacted = 0
            speech_bool = False
            s_entity = None
            dialogue_list = []
            speech_index = 0

        if keypress:
            if controller_connected:
                joybtnpressed = joysticks[0].get_button(0)
                if joybtnpressed and not prevkey:
                    if dialogueindex == dialoguelen:
                        speech_index += 1
                        dialogueindex = 0
                        keypress = False
                    else:
                        dialogueindex = dialoguelen
                        keypress = False
                if not joybtnpressed and prevkey:
                    keypress = True
                prevkey = joybtnpressed
            else:
                keyspressed = pygame.key.get_pressed()
                if keyspressed[K_RETURN] and not prevkey[K_RETURN]:
                    if dialogueindex == dialoguelen:
                        speech_index += 1
                        dialogueindex = 0
                        keypress = False
                    else:
                        dialogueindex = dialoguelen
                        keypress = False
                if not keyspressed[K_RETURN] and prevkey[K_RETURN]:
                    keypress = True
                prevkey = keyspressed

        if speech_index >= len(dialogues):
            speech_bool = False
            if entity.interacted > 0:
                if entity.id != "country":
                    entity.interacted -= 1
            if entity.id == "country" and ruined_talked:
                try:
                    new_mission(remaining_missions[0])
                except IndexError:
                    pass
            if entity.id == "guide1" and level == 0:
                phase += 1
            if player.rect.centerx < entity.rect.centerx:
                player.rect.right = entity.rect.x - 12
            else:
                player.rect.x = entity.rect.right + 12
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
    elif entity.id == "guide1":
        dialogue_list = [["guide1", "You appear to be lost."], ["player", "I'm not exactly lost..."], ["player", "but I am low on resources."], ["guide1", "Follow your sense of justice."], ["guide1", "Salvation is nearing us..."], ["player", "What?"], ["guide1", "Nothing. Keep going forward."]]

    return dialogue_list

bg = pygame.Surface((display_rect.w, display_rect.h))
bg.fill((0, 0, 0))
bg.set_alpha(0)

graphcooldown = 0

level = 0
phase = 0

def new_mission(mission=None):
    wait = 0
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

            if wait > 500:
                if controller_connected:
                    joybtnpressed = joysticks[0].get_button(0)
                    if joybtnpressed:
                        running = False
                else:
                    keyspressed = pygame.key.get_pressed()
                    if keyspressed[K_RETURN]:
                        running = False
            else:
                wait += 1

            screen.blit(bg, (0, 0))
            pygame.draw.rect(screen, (255, 255, 0), (display_rect.centerx - 300, display_rect.centery - 200, 600, 400))
            write(True, "New Mission", (display_rect.centerx - 100, display_rect.centery - 150), (0, 0, 0), 50)
            write(True, mission, (display_rect.centerx - 100, display_rect.centery - 100), (0, 0, 0), 40)
            pygame.display.flip()
        finished_missions.append(mission)
        remaining_missions.remove(mission)

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
            self.spriteimg = pygame.image.load("Assets/Images/pixel_trees/pixel_trees/pixel_tree_summer.png")
            self.image.blit(pygame.transform.scale(self.spriteimg, (self.rect.w, self.rect.h)), (0, 0))
            self.image.set_colorkey((255, 0, 0))
            self.outer = Tree
        
        def update(self, **kwargs):
            self.rect.x = self.outer.rect.x - 32 - scroll[0]
            self.rect.bottom = self.outer.rect.bottom - scroll[1]

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
        self.irect.x += self.movement[0]
        self.irect.y += self.movement[1]
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

            vcollside = {"front": False, "back": False, "left": False, "right": False}
            villager.irect.x += villager.movement[0]
            
            vcoll = []
            for house in self.houses:
                if villager.rect.colliderect(house.rect):
                    vcoll.append(house)
                if villager.rect.colliderect(player.rect):
                    vcoll.append(player)
                    
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
            
            vcoll = []
            for house in self.houses:
                if villager.rect.colliderect(house.rect):
                    vcoll.append(house)
                if villager.rect.colliderect(player.rect):
                    vcoll.append(player)
            for coll in vcoll:
                if villager.movement[1] > 0:
                    vcollside["back"] = True
                    villager.rect.bottom = coll.rect.y
                    villager.movement[1] = -1
                elif villager.movement[1] < 0:
                    vcollside["front"] = True
                    villager.rect.y = coll.rect.bottom
                    villager.movement[1] = 1

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

        class Sprite(pygame.sprite.Sprite):
            def __init__(self, House):
                pygame.sprite.Sprite.__init__(self)
                self.outer = House
                self.image = pygame.Surface((256, 384))
                self.rect = self.image.get_rect()
                self.spriteimg = pygame.image.load("Assets/Images/house.png")
                self.image.blit(pygame.transform.scale(self.spriteimg, (self.rect.w, self.rect.h)), (0, 0))
                key = self.spriteimg.get_at((0, 0))
                self.image.set_colorkey(key)

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
        with open("Assets/Maps/village_map1.txt", "r") as mapfile:
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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24, 16))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.irect = self.rect
        self.detectrect = Rect(self.rect.x - 12, self.rect.y - 12, self.rect.width + 24, self.rect.height + 24)
        self.attackrect = Rect(self.rect.x - 32, self.rect.y - 32, self.rect.width + 64, self.rect.height + 64)
        self.movement = [0, 0]
        self.hp = 100
        self.detectablebyenemies = 1
        self.stamina = 300
        self.poisoning = False
        self.paralysis = False
        self.paralysis_time = 300
        self.burning = False
        self.sleep = False ### implement later  
        self.sprite = self.Sprite(self)

        self.connections = [[None, []], [None, []], [None, []], [None, []]]

        self.inv = [["Blade", True], ["Bow", True], ["Flame", True], ["Tamas", True], ["Dash", True], ["Ripple", True], ["Frost", True], ["Poison", True], ["Thunder", True], ["Shield", True], ["Teleport", True], ["Kaal", True]]
        self.invactive = -1

    def update(self, **kwargs):
        self.rect.x = self.irect.x - scroll[0]
        self.rect.y = self.irect.y - scroll[1]
        self.detectrect.x = self.rect.x - 8
        self.detectrect.y = self.rect.y - 8
        self.attackrect.x = self.rect.x - 32
        self.attackrect.y = self.rect.y - 32
        if self.movement == [0, 0] and self.stamina < 300:
            self.stamina += 1
        
        self.stamina = 300 #remove after production

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
            self.spritesheet = pygame.image.load("Assets/Images/8Direction_TopDown_CharacterAssets_ByBossNelNel/8Direction_TopDown_Character Sprites_ByBossNelNel/SpriteSheet.png")
            self.rect = self.image.get_rect()
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

class Arena(Object):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2000, 2000))
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
        def __init__(self, Arena):
            pygame.sprite.Sprite.__init__(self)
            self.outer = Arena
            self.collidable = False
            self.image = pygame.Surface((2000, 2200))
            self.rect = self.image.get_rect()
            self.image.fill((0, 180, 80))
            pygame.draw.rect(self.image, (100, 40, 0), (0, self.rect.bottom - 200, self.rect.width, 200))
        
        def update(self, **kwargs):
            self.rect.x = self.outer.rect.x - scroll[0]
            self.rect.y = self.outer.rect.y - scroll[1]

# def drawbg(x, y):
#     maplist = []
#     trees = []
#     with open("Assets/Maps/area_1.txt") as mapfile:
#         text = mapfile.readlines()
#         for i in range(len(text)):
#             linelist = []
#             for j in range(len(text[i])):
#                 if text[i][j] != "\n":
#                     linelist.append(int(text[i][j]))
#                 if text[i][j] == "1":
#                     if i%2 == 0 and j%2 == 0:
#                         trees.append(Tree(j*64 + x, i*32 + y))
#                     else:
#                         trees.append(Tree(j*64 + x + random.randint(-2, 2)*8, i*32 + y + random.randint(-1, 1)*4))
#                     ObjectGroup.add(trees[-1])
#                     SpriteGroup.add(trees[-1].sprite)
#             maplist.append(linelist)
#     return maplist

def gameloop(loadgame=0):
    global scroll, player, controller_connected
    global speech_bool, dialogue_list, s_entity

    player = Player()
    player.add(PlayerGroup)
    player.sprite.add(SpriteGroup)

    arena = Arena(-1000, -1000)
    ArenaGroup.add(arena)
    SpriteGroup.add(arena.sprite)

    for i in range(60):
        x = random.randint(arena.rect.x + 80, arena.rect.right - 80)
        y = random.randint(arena.rect.y + 80, arena.rect.bottom - 80)
        while player.rect.colliderect(Rect(x, y, 32, 64)):
            x = random.randint(arena.rect.x + 80, arena.rect.right - 80)
            y = random.randint(arena.rect.y + 80, arena.rect.bottom - 80)
        tree = Tree(x, y)
        ObjectGroup.add(tree)
        SpriteGroup.add(tree.sprite)

    pygame.mouse.set_pos(500, 400)

    # lore1v = LoreVillage(3000, -800)
    # lore1v.add(VillageGroup)
    # lore1v.sprite.add(SpriteGroup)
    # lore1v.villagers[0].id = "ruined"
    # lore1v.villagers[0].sprite.color = (255, 0, 255)
    # lore1v.villagers[1].id = "country"
    # lore1v.villagers[1].sprite.color = (10, 255, 10)

    # enemylist = []
    # for i in range(4):
    #     x = random.randint(-800, 800)
    #     y = random.randint(-800, 800)
    #     for village in VillageGroup:
    #         while village.rect.colliderect(Rect(x, y, 32, 64)):
    #             x = random.randint(-800, 800)
    #             y = random.randint(-800, 800)
    #     enemylist.append(Character(x, y))

    # for enemy in enemylist:
    #     enemy.hostile = True
    #     enemy.id = "enemy"
    #     enemy.add(EnemyGroup)
    #     enemy.sprite.add(SpriteGroup)

    running = True

    scroll = [0, 0]
    
    in_menu = False

    bg = pygame.Surface((display_rect.w, display_rect.h))
    bg.fill((0, 0, 0))
    bg.set_alpha(200)

    # drawbg(-400, -80)

    def blit(group):
        order = []
        for item in group:
            if type(item.outer) == Village or type(item.outer) == LoreVillage:
                for house in item.outer.houses:
                    order.append(house.sprite)
                for villager in item.outer.villagers:
                    order.append(villager.sprite)
            order.append(item)
        n = len(order)
        for i in range(n):
            for j in range(0, n-i-1):
                if order[j].outer.rect.y > order[j+1].outer.rect.y:
                    order[j], order[j+1] = order[j+1], order[j]
        for i in range(n):
            screen.blit(order[i].image, order[i].rect)

    #region

    def graph(joystick):
        global graphcooldown
        screen.blit(bg, (0, 0))
        if graphcooldown == 0:
            if round(joystick.get_axis(0)) > 0:
                if player.invactive < len(player.inv) - 1 and ((player.invactive%8) != 7 or player.invactive == -1):
                    player.invactive += 1
                    graphcooldown = 12
            elif round(joystick.get_axis(0)) < 0:
                if player.invactive > 0 and (player.invactive%8) != 0:
                    player.invactive -= 1
                    graphcooldown = 12
            if round(joystick.get_axis(1)) > 0:
                if player.invactive < (len(player.inv)//8)*8:
                    player.invactive += 8
                    if player.invactive > len(player.inv) - 1:
                        player.invactive = len(player.inv) - 1
                    graphcooldown = 12
            elif round(joystick.get_axis(1)) < 0:
                if player.invactive > 7:
                    player.invactive -= 8
                    graphcooldown = 12
        else:
            graphcooldown -= 1

        for i in range(len(player.inv)):
            pygame.draw.rect(screen, (100, 50, 50), (30 + 120*(i%8), 50 + 70*(i//8), 110, 60))
            if player.invactive == i:
                if not player.inv[i][1]:
                    write(text=player.inv[i][0], position=(40 + 120*(i%8), 60 + 70*(i//8)), fontsize=26, color=(255, 120, 120))
                else:
                    write(text=player.inv[i][0], position=(40 + 120*(i%8), 60 + 70*(i//8)), fontsize=26, color=(255, 255, 255))
            elif not player.inv[i][1]:
                write(text=player.inv[i][0], position=(40 + 120*(i%8), 60 + 70*(i//8)), fontsize=25, color=(255, 0, 0))
            else:
                write(text=player.inv[i][0], position=(40 + 120*(i%8), 60 + 70*(i//8)), fontsize=25)
        

        #graph
        if player.invactive != -1:
            if joystick.get_button(0) and graphcooldown == 0:
                for conn in range(len(player.connections)):
                    if player.connections[conn][0] == None:
                        if player.inv[player.invactive][1]:
                            player.connections[conn][0] = player.inv[player.invactive][0]
                            player.inv[player.invactive][1] = False
                            joystick.rumble(0.8, 0.8, 120)
                            graphcooldown = 12
                            break
                    elif player.connections[conn][0] == player.inv[player.invactive][0]:
                        player.connections[conn][0] = None
                        for i in range(len(player.inv)):
                            try:
                                if player.inv[i][0] == player.connections[conn][1][0] or player.inv[i][0] == player.connections[conn][1][1]:
                                    player.inv[i][1] = True
                            except IndexError:
                                pass
                        player.connections[conn][1] = []
                        player.inv[player.invactive][1] = True
                        joystick.rumble(0.5, 0.5, 60)
                        graphcooldown = 15
                        break

            rj = round(joystick.get_axis(2)), round(joystick.get_axis(3))
            if graphcooldown == 0:
                if rj[1] > 0:
                    if player.connections[0][0] != None:
                        if player.inv[player.invactive][1]:
                            if not player.inv[player.invactive][0] in player.connections[0][1] and player.inv[player.invactive][0] != player.connections[0][0] and len(player.connections[0][1]) < 2:
                                player.connections[0][1].append(player.inv[player.invactive][0])
                                player.inv[player.invactive][1] = False
                                graphcooldown = 12
                        else:
                            if player.inv[player.invactive][0] in player.connections[0][1]:
                                player.connections[0][1].remove(player.inv[player.invactive][0])
                                player.inv[player.invactive][1] = True
                                graphcooldown = 12
                elif rj[0] > 0:
                    if player.connections[1][0] != None:
                        if player.inv[player.invactive][1]:
                            if not player.inv[player.invactive][0] in player.connections[1][1] and player.inv[player.invactive][0] != player.connections[1][0] and len(player.connections[1][1]) < 2:
                                player.connections[1][1].append(player.inv[player.invactive][0])
                                player.inv[player.invactive][1] = False
                                graphcooldown = 12
                        else:
                            if player.inv[player.invactive][0] in player.connections[1][1]:
                                player.connections[1][1].remove(player.inv[player.invactive][0])
                                player.inv[player.invactive][1] = True
                                graphcooldown = 12
                if rj[0] < 0:
                    if player.connections[2][0] != None:
                        if player.inv[player.invactive][1]:
                            if not player.inv[player.invactive][0] in player.connections[2][1] and player.inv[player.invactive][0] != player.connections[2][0] and len(player.connections[2][1]) < 2:
                                player.connections[2][1].append(player.inv[player.invactive][0])
                                player.inv[player.invactive][1] = False
                                graphcooldown = 12
                        else:
                            if player.inv[player.invactive][0] in player.connections[2][1]:
                                player.connections[2][1].remove(player.inv[player.invactive][0])
                                player.inv[player.invactive][1] = True
                                graphcooldown = 12
                elif rj[1] < 0:
                    if player.connections[3][0] != None:
                        if player.inv[player.invactive][1]:
                            if not player.inv[player.invactive][0] in player.connections[3][1] and player.inv[player.invactive][0] != player.connections[3][0] and len(player.connections[3][1]) < 2:
                                player.connections[3][1].append(player.inv[player.invactive][0])
                                player.inv[player.invactive][1] = False
                                graphcooldown = 12
                        else:
                            if player.inv[player.invactive][0] in player.connections[3][1]:
                                player.connections[3][1].remove(player.inv[player.invactive][0])
                                player.inv[player.invactive][1] = True
                                graphcooldown = 12
            
        pygame.draw.rect(screen, (255, 255, 255), (display_rect.centerx - 100, display_rect.centery + 50, 50, 50), 1)
        pygame.draw.rect(screen, (255, 255, 255), (display_rect.centerx + 50, display_rect.centery + 50, 50, 50), 1)
        pygame.draw.rect(screen, (255, 255, 255), (display_rect.centerx - 25, display_rect.centery - 25, 50, 50), 1)
        pygame.draw.rect(screen, (255, 255, 255), (display_rect.centerx - 25, display_rect.centery + 130, 50, 50), 1)

        if player.connections[0][0] != None:
            write(text=player.connections[0][0], position=(display_rect.centerx - 25, display_rect.centery + 130), fontsize=30, color=(255, 255, 255))

            pygame.draw.rect(screen, (255, 255, 255), (display_rect.centerx - 100, display_rect.centery + 200, 50, 50), 1)
            pygame.draw.line(screen, (255, 255, 255), (display_rect.centerx - 75, display_rect.centery + 200), (display_rect.centerx - 25, display_rect.centery + 150), 1)

            pygame.draw.rect(screen, (255, 255, 255), (display_rect.centerx + 50, display_rect.centery + 200, 50, 50), 1)
            pygame.draw.line(screen, (255, 255, 255), (display_rect.centerx + 75, display_rect.centery + 200), (display_rect.centerx + 25, display_rect.centery + 150), 1)

            for conn in range(len(player.connections[0][1])):
                write(text=player.connections[0][1][conn], position=((display_rect.centerx - 100) + conn*150, display_rect.centery + 210), fontsize=30, color=(255, 255, 255))
        if player.connections[1][0] != None:
            write(text=player.connections[1][0], position=(display_rect.centerx + 50, display_rect.centery + 50), fontsize=30, color=(255, 255, 255))

            pygame.draw.rect(screen, (255, 255, 255), (display_rect.centerx + 150, display_rect.centery, 50, 50), 1)
            pygame.draw.line(screen, (255, 255, 255), (display_rect.centerx + 150, display_rect.centery + 25), (display_rect.centerx + 100, display_rect.centery + 75), 1)

            pygame.draw.rect(screen, (255, 255, 255), (display_rect.centerx + 150, display_rect.centery + 100, 50, 50), 1)
            pygame.draw.line(screen, (255, 255, 255), (display_rect.centerx + 150, display_rect.centery + 125), (display_rect.centerx + 100, display_rect.centery + 75), 1)

            for conn in range(len(player.connections[1][1])):
                write(text=player.connections[1][1][conn], position=(display_rect.centerx + 150, (display_rect.centery + 10) + conn*100), fontsize=30, color=(255, 255, 255))
        if player.connections[2][0] != None:
            write(text=player.connections[2][0], position=(display_rect.centerx - 100, display_rect.centery + 50), fontsize=30, color=(255, 255, 255))
            
            pygame.draw.rect(screen, (255, 255, 255), (display_rect.centerx - 200, display_rect.centery, 50, 50), 1)
            pygame.draw.line(screen, (255, 255, 255), (display_rect.centerx - 150, display_rect.centery + 25), (display_rect.centerx - 100, display_rect.centery + 75), 1)

            pygame.draw.rect(screen, (255, 255, 255), (display_rect.centerx - 200, display_rect.centery + 100, 50, 50), 1)
            pygame.draw.line(screen, (255, 255, 255), (display_rect.centerx - 150, display_rect.centery + 125), (display_rect.centerx - 100, display_rect.centery  + 75), 1)

            for conn in range(len(player.connections[2][1])):
                write(text=player.connections[2][1][conn], position=(display_rect.centerx - 200, (display_rect.centery + 10) + conn*100), fontsize=30, color=(255, 255, 255))
        if player.connections[3][0] != None:
            write(text=player.connections[3][0], position=(display_rect.centerx - 25, display_rect.centery - 25), fontsize=30, color=(255, 255, 255))

            pygame.draw.rect(screen, (255, 255, 255), (display_rect.centerx - 100, display_rect.centery - 100, 50, 50), 1)
            pygame.draw.line(screen, (255, 255, 255), (display_rect.centerx - 75, display_rect.centery - 50), (display_rect.centerx - 25, display_rect.centery), 1)

            pygame.draw.rect(screen, (255, 255, 255), (display_rect.centerx + 50, display_rect.centery - 100, 50, 50), 1)
            pygame.draw.line(screen, (255, 255, 255), (display_rect.centerx + 75, display_rect.centery - 50), (display_rect.centerx + 25, display_rect.centery), 1)

            for conn in range(len(player.connections[3][1])):
                write(text=player.connections[3][1][conn], position=((display_rect.centerx - 100) + conn*150, display_rect.centery - 90), fontsize=30, color=(255, 255, 255))

    def status():
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

    x_seek, y_seek = 0, 0
    guide1 = None

    while running:                                                          ### GAMELOOP START ###
        scroll[0] += ((player.irect.x - scroll[0] - (500-player.irect.w/2)) + (x_seek))
        scroll[1] += ((player.irect.y - scroll[1] - (400-player.irect.h/2)) + (y_seek))

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
            # if ev.type == pygame.JOYBUTTONDOWN:
            #     if ev.button == 1:
            #         joystick = joysticks[ev.instance_id]
            #         joystick.rumble(0, 0.5, 150)
            if ev.type == pygame.JOYDEVICEADDED:
                controller_connected = True
                joy = pygame.joystick.Joystick(ev.device_index)
                joysticks[joy.get_instance_id()] = joy
            if ev.type == pygame.JOYDEVICEREMOVED:
                controller_connected = False
                del joysticks[ev.instance_id]

        # Level 0, Phase 0
        if not guide1 in NPCGroup:
            if level == 0 and phase == 0:
                guide1 = Character(100, 0)
                guide1.add(NPCGroup)
                guide1.sprite.add(SpriteGroup)
                guide1.sprite.image.fill((255, 255, 0))
                guide1.id = "guide1"
        try:
            if not (level == 0 and phase == 0):
                SpriteGroup.remove(guide1.sprite)
                NPCGroup.remove(guide1)
                guide1 = None
        except AttributeError:
            pass

        # Level 0, Phase 1
        if len(EnemyGroup) == 0:
            if level == 0 and phase == 1:
                for i in range(20):
                    x = random.randint(arena.rect.x + 80, arena.rect.right - 80)
                    y = random.randint(arena.rect.y + 80, arena.rect.bottom - 80)
                    for enemy in EnemyGroup:
                        while enemy.rect.colliderect(Rect(x, y, 32, 64)):
                            x = random.randint(arena.rect.x + 80, arena.rect.right - 80)
                            y = random.randint(arena.rect.y + 80, arena.rect.bottom - 80)
                    for obj in ObjectGroup:
                        while obj.rect.colliderect(Rect(x, y, 32, 64)):
                            x = random.randint(arena.rect.x + 80, arena.rect.right - 80)
                            y = random.randint(arena.rect.y + 80, arena.rect.bottom - 80)
                    enemy = Character(x, y)
                    enemy.hostile = True
                    enemy.id = "enemy"
                    enemy.add(EnemyGroup)
                    enemy.sprite.add(SpriteGroup)
        try:
            if not (level == 0 and phase == 1):
                for enemy in EnemyGroup:
                    SpriteGroup.remove(enemy.sprite)
                    EnemyGroup.remove(enemy)
        except AttributeError:
            pass

        # Level 0, Phase 2
        # Collection Phase
        #   Make Rt trigger button allow the user to crouch and sneak
    
        screen.fill((0, 0, 0))
        blit(SpriteGroup)
        ArenaGroup.update()
        ObjectGroup.update()
        EnemyGroup.update()
        PlayerGroup.update()
        SpriteGroup.update()
        NPCGroup.update()
                
        if not speech_bool:
            if not controller_connected:
                mx, my = pygame.mouse.get_pos()
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[K_SPACE]:
                    in_menu = True
                    status()
                elif keys_pressed[K_a]:
                    in_menu = True
                    graph()
                else:
                    in_menu = False
                    bg.set_alpha(0)

                x_seek = round(mx - player.irect.center[0])
                y_seek = round(my - player.irect.center[1])

                player.sprint = False
                if keys_pressed[K_LSHIFT] and player.stamina > 0 and not player.poisoning:
                    player.sprint = True
                    player.stamina -= 1
                    # player.detectablebyenemies = 100

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
                    elif player.irect.x > mx:
                        if player.movement[0] > -2:
                            player.movement[0] -= (player.irect.center[0] - mx)/800
                        if player.sprint:
                            if player.movement[0] > -6:
                                player.movement[0] -= (player.irect.center[0] - mx)/800
                        else:
                            if player.movement[0] < -2:
                                player.movement[0] += 0.5
                    else:
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
                    elif player.irect.y > my:
                        if player.movement[1] > -2:
                            player.movement[1] -= (player.irect.center[1] - my)/800
                        if player.sprint:
                            if player.movement[1] > -6:
                                player.movement[1] -= (player.irect.center[1] - my)/800
                        else:
                            if player.movement[1] < -2:
                                player.movement[1] += 0.5
                    else:
                        if 2 > player.movement[1] > 0:
                            player.movement[1] -= 0.5
                        if -2 < player.movement[1] < 0:
                            player.movement[1] += 0.5
                        if player.movement[1] < 0.5 or player.movement[1] > -0.5:
                            player.movement[1] = 0
                else:
                    player.movement = [0, 0]
            
            else:
                for joystick in joysticks.values():
                    if joystick.get_button(7):
                        reset()
                        running = False

                    if not in_menu and player.movement == [0, 0]:
                        # x_seek = round(joystick.get_axis(2), 2)*80
                        # y_seek = round(joystick.get_axis(3), 2)*80
                        if x_seek < round(joystick.get_axis(2))*100:
                            x_seek += 10
                        elif x_seek > round(joystick.get_axis(2))*100:
                            x_seek -= 10
                        if y_seek < round(joystick.get_axis(3))*100:
                            y_seek += 10
                        elif y_seek > round(joystick.get_axis(3))*100:
                            y_seek -= 10
                    else:
                        x_seek = 0
                        y_seek = 0

                    if not in_menu:
                        xaxis = round(joystick.get_axis(0))
                        if arena.rect.x + 10 < player.rect.x and xaxis < 0:
                            player.movement[0] = xaxis*2
                        elif arena.rect.right - 10 > player.rect.right and xaxis > 0:
                            player.movement[0] = xaxis*2
                        else:
                            player.movement[0] = 0
                        yaxis = round(joystick.get_axis(1))
                        if arena.rect.y + 15 < player.rect.y and yaxis < 0:
                            player.movement[1] = yaxis*2
                        elif arena.rect.bottom - 15 > player.rect.bottom and yaxis > 0:
                            player.movement[1] = yaxis*2
                        else:
                            player.movement[1] = 0
                        
                    player.sprint = False
                    joy_btn_sprint = joystick.get_button(5)
                    if joy_btn_sprint and player.stamina > 0 and not player.poisoning:
                        player.sprint = True
                        player.stamina -= 1
                        # player.detectablebyenemies = 100
                        player.movement[0] *= 4
                        player.movement[1] *= 4
                    
                    joy_btn_menu1 = joystick.get_button(4)
                    joy_btn_status = joystick.get_axis(4)
                    if joy_btn_menu1:
                        in_menu = True
                        graph(joystick)
                    elif joy_btn_status > 0:
                        in_menu = True
                        status()
                    else:
                        in_menu = False
                    
                    if in_menu:
                        player.movement = [0, 0]
                    
                    if not joy_btn_menu1:
                        player.invactive = -1

        #region
        pcollside = {"front": False, "back": False, "left": False, "right": False}
        player.irect.x += player.movement[0]
        #region[rgb(72, 0, 0)]
        ecoll = []
        for coll in EnemyGroup:
            if coll.rect.colliderect(player.attackrect):
                ecoll.append(coll)
        for coll in ecoll:
            if coll.type == "npc":
                if coll.hostile:
                    for conn in range(len(player.connections)):
                        if player.connections[conn][0] == "Blade":
                            if controller_connected:
                                if joystick.get_button(conn):
                                    coll.hp -= 5
                                    s_entity = coll
                                    break
                    else:
                        player.hp -= 1
                        s_entity = coll

                        # player.paralysis = True
                        # player.poisoning = True
                        # player.burning = True
                    if coll.hp <= 0:
                        if len(EnemyGroup) == 1:
                            phase += 1
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
                    if villager.interacted > 0:
                        speech_bool = True
                    s_entity = villager
                    dialogue_list = npc_dialogues(villager)
        for npc in NPCGroup:
            if npc.rect.colliderect(player.rect):
                pcoll.append(npc)
            if npc.rect.colliderect(player.detectrect):
                if npc.interacted > 0:
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
        ecoll = []
        for coll in EnemyGroup:
            if coll.rect.colliderect(player.attackrect):
                ecoll.append(coll)
        for coll in ecoll:
            if coll.type == "npc":
                if coll.hostile:
                    for conn in range(len(player.connections)):
                        if player.connections[conn][0] == "Blade":
                            if controller_connected:
                                if joystick.get_button(conn):
                                    coll.hp -= 5
                                    s_entity = coll
                                    break
                    else:
                        player.hp -= 1
                        s_entity = coll

                        # player.paralysis = True
                        # player.poisoning = True
                        # player.burning = True
                    if coll.hp <= 0:
                        if len(EnemyGroup) == 1:
                            phase += 1
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
                    if villager.interacted > 0:
                        speech_bool = True
                    s_entity = villager
                    dialogue_list = npc_dialogues(villager)
        for npc in NPCGroup:
            if npc.rect.colliderect(player.rect):
                pcoll.append(npc)
            if npc.rect.colliderect(player.detectrect):
                if npc.interacted > 0:
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
            dialogue_end = False

        if player.detectablebyenemies > 0:
            for enemy in EnemyGroup:
                if enemy.rect.colliderect(display_rect):
                    if player.rect.x > enemy.rect.right:
                        enemy.movement[0] = 1
                    if player.rect.right < enemy.rect.x:
                        enemy.movement[0] = -1
                    if player.rect.y > enemy.rect.bottom:
                        enemy.movement[1] = 1
                    if player.rect.bottom < enemy.rect.y:
                        enemy.movement[1] = -1

                for enemy2 in EnemyGroup:
                    if enemy != enemy2:
                        if enemy.rect.colliderect(enemy2.rect):
                            enemy.movement[0] = -enemy.movement[0]
                            enemy.movement[1] = -enemy.movement[1]
                            enemy2.movement[0] = -enemy2.movement[0]
                            enemy2.movement[1] = -enemy2.movement[1]

        #endregion
        if player.hp <= 0:
            # player.hp = 1
            reset()
            running = False
            break

#endregion
        
def mainloop():
    running = True
    global joysticks, controller_connected
    controller_connected = False
    joysticks = {}
    selection = 0
    while running:
        pygame.display.update(); clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    joystick = joysticks[event.instance_id]
                    joystick.rumble(0, 0.7, 500)

            if event.type == pygame.JOYDEVICEADDED:
                controller_connected = True
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                joystick = joysticks[0]
                pygame.mouse.set_visible(False)

            if event.type == pygame.JOYDEVICEREMOVED:
                controller_connected = False
                del joysticks[event.instance_id]
                pygame.mouse.set_visible(True)
            if event.type == pygame.JOYAXISMOTION:
                jam = round(joystick.get_axis(1))
                if jam > 0 and selection < 3:
                    selection += 1
                elif jam < 0 and selection > 0:
                    selection -= 1
                for i in range(420):
                    print("")
                break
            if event.type == pygame.JOYHATMOTION:
                jam = joystick.get_hat(0)
                if jam[1] == 1 and selection > 0:
                    selection -= 1
                elif jam[1] == -1 and selection < 3:
                    selection += 1
                break
        mx, my = pygame.mouse.get_pos()
        screen.fill((255, 255, 255))
        write(text="NODES", position=(412, 100), fontsize=60)
        pygame.draw.rect(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (500-16, 400-32, 32, 64))
        if controller_connected:
            if selection == 0:
                write(text="Start", position=(50, 550))
                if joystick.get_button(0):
                    gameloop(0)
            else:
                write(text="Start", position=(50, 550), color=(100, 50, 50))
            if selection == 1:
                write(text="Load", position=(50, 600))
                if joystick.get_button(0):
                    gameloop(1)
            else:
                write(text="Load", position=(50, 600), color=(100, 50, 50))
            if selection == 2:
                write(text="Settings", position=(50, 650))
                if joystick.get_button(0):
                    pass
            else:
                write(text="Settings", position=(50, 650), color=(100, 50, 50))
            if selection == 3:
                write(text="Exit", position=(50, 700))
                if joystick.get_button(0):
                    pygame.quit()
                    sys.exit()
                    
            else:
                write(text="Exit", position=(50, 700), color=(100, 50, 50))
        else:
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
