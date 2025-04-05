import pygame, sys
from pygame.locals import *
from scripts.char_obj import Village, LoreVillage, player, PlayerGroup, EnemyGroup, ObjectGroup, VillageGroup, SpriteGroup, NPCGroup, bg, display_rect, screen, controller_connected, joysticks

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
    global speech_bool, dialogue_list, s_entity, speech_index, dialoguestr, dialogueindex, dialogue_end, ruined_talked, name_dict, remaining_missions, finished_missions, PlayerGroup, EnemyGroup, ObjectGroup, VillageGroup, SpriteGroup, NPCGroup
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
    dialoguestr = ""
    dialogueindex = 0

    dialogue_end = False

    ruined_talked = False

    remaining_missions = ["attack nearby country"]
    finished_missions = []

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

def menu1joy(joystick):
    if bg.get_alpha() < 200:
        bg.set_alpha(bg.get_alpha() + 20)

    screen.blit(bg, (0, 0))
    if player.active1 > -1:
        for i in range(len(player.inv1)):
            if player.active1 == i:
                pygame.draw.line(screen, (180, 180, 180), (500, 600), (150 + 300*i, 200), 8)
    if joystick.get_button(3):
        player.active1 = -1
    for ev in pygame.event.get():
        if ev.type == pygame.JOYAXISMOTION:
            if joystick.get_axis(2) > 0:
                if player.active1 < len(player.inv1) - 1:
                    player.active1 += 1
                else:
                    player.active1 = 0
            if joystick.get_axis(2) < 0:
                if player.active1 > 0:
                    player.active1 -= 1
                else:
                    player.active1 = len(player.inv1) - 1
            print(player.active1)
    for i in range(len(player.inv1)):
        pygame.draw.rect(screen, (140, 100, 100), (50 + 300*i, 200, 200, 100))
        if player.active1 == i:
            write(text=player.inv1[i], position=(75 + 300*i, 210), fontsize=60, color=(255, 255, 255))
        else:
            write(text=player.inv1[i], position=(75 + 300*i, 210), fontsize=60)

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
def menu2joy(joystick):
    if bg.get_alpha() < 200:
        bg.set_alpha(bg.get_alpha() + 20)

    screen.blit(bg, (0, 0))
    if player.active2 > -1:
        for i in range(len(player.inv2)):
            if player.active2 == i:
                pygame.draw.line(screen, (180, 180, 180), (500, 600), (150 + 300*i, 200), 8)
    if joystick.get_button(3):
        player.active2 = -1
    for ev in pygame.event.get():
        if ev.type == pygame.JOYAXISMOTION:
            if joystick.get_axis(2) > 0:
                if player.active2 < len(player.inv2) - 1:
                    player.active2 += 1
                else:
                    player.active2 = 0
            if joystick.get_axis(2) < 0:
                if player.active2 > 0:
                    player.active2 -= 1
                else:
                    player.active1 = len(player.inv2) - 1
            print(player.active2)
    for i in range(len(player.inv2)):
        pygame.draw.rect(screen, (140, 100, 100), (50 + 300*i, 200, 200, 100))
        if player.active2 == i:
            write(text=player.inv2[i], position=(75 + 300*i, 210), fontsize=60, color=(255, 255, 255))
        else:
            write(text=player.inv2[i], position=(75 + 300*i, 210), fontsize=60)
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
def menu3joy(joystick):
    if bg.get_alpha() < 200:
        bg.set_alpha(bg.get_alpha() + 20)

    screen.blit(bg, (0, 0))
    if player.active3 > -1:
        for i in range(len(player.inv3)):
            if player.active3 == i:
                pygame.draw.line(screen, (180, 180, 180), (500, 600), (150 + 300*i, 200), 8)
    # if joystick.get_button(3):
    #     player.active3 = -1
    for ev in pygame.event.get():
        if ev.type == pygame.JOYAXISMOTION:
            if joystick.get_axis(2) > 0:
                if player.active3 < len(player.inv3) - 1:
                    player.active3 += 1
                else:
                    player.active3 = 0
            elif joystick.get_axis(2) < 0:
                if player.active3 > 0:
                    player.active3 -= 1
                else:
                    player.active3 = len(player.inv3) - 1
            else:
                player.active3 = -1
            for i in range(420):
                print("")
            # print(player.active3)
    for i in range(len(player.inv3)):
        pygame.draw.rect(screen, (140, 100, 100), (50 + 300*i, 200, 200, 100))
        if player.active3 == i:
            write(text=player.inv3[i], position=(75 + 300*i, 210), fontsize=60, color=(255, 255, 255))
        else:
            write(text=player.inv3[i], position=(75 + 300*i, 210), fontsize=60)
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