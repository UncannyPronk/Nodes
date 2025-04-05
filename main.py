import pygame, sys, random
from pygame import *
from pygame.locals import *

from scripts.global_vars import display_rect, PlayerGroup, SpriteGroup, VillageGroup, NPCGroup, EnemyGroup, ObjectGroup, bg
from scripts.funcs import write, blit, reset, status, menu1, menu2, menu3
from scripts.speech import speech_engine, npc_dialogues

pygame.init()

pygame.display.set_caption("Nodes")
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

display_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())

reset()

# # GAMEPAD CONTROLS INIT
pygame.joystick.init()

def gameloop(loadgame=0):
    #region
    global scroll, player, controller_connected
    global speech_bool, dialogue_list, s_entity

    while running:
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
            if ev.type == pygame.JOYBUTTONDOWN:
                # print("Joystick button pressed.")
                if ev.button == 1:
                    joystick = joysticks[ev.instance_id]
                    joystick.rumble(0, 0.5, 150)
                        # print(f"Rumble effect played on joystick {ev.instance_id}")
            # if ev.type == pygame.JOYBUTTONUP:
                # print("Joystick button released.")
            if ev.type == pygame.JOYDEVICEADDED:
                pygame.mouse.set_visible(False)
                controller_connected = True
                joy = pygame.joystick.Joystick(ev.device_index)
                joysticks[joy.get_instance_id()] = joy
                # print(f"Joystick {joy.get_instance_id()} connencted")
            if ev.type == pygame.JOYDEVICEREMOVED:
                pygame.mouse.set_visible(True)
                controller_connected = False
                del joysticks[ev.instance_id]
                # print(f"Joystick {ev.instance_id} disconnected")
    
        screen.fill((0, 255, 120))
        blit(SpriteGroup)
        ObjectGroup.update()
        EnemyGroup.update()
        PlayerGroup.update()
        VillageGroup.update()
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
            
            else:
                for joystick in joysticks.values():
                    if joystick.get_button(7):
                        reset()
                        running = False
                    # axes = joystick.get_numaxes()
                    # for i in range(axes):
                    xaxis = joystick.get_axis(0)
                    player.movement[0] = xaxis*2
                    if xaxis == 0:
                        player.movement[0] = 0
                    yaxis = joystick.get_axis(1)
                    player.movement[1] = yaxis*2
                    if yaxis == -3.0517578125e-05:
                        yaxis = 0
                    if yaxis == 0:
                        player.movement[1] = 0
                    if xaxis == 0 and yaxis == 0:
                        player.movement = [0, 0]
                    
                    player.sprint = False
                    joy_btn_sprint = joystick.get_button(1)
                    if joy_btn_sprint and player.stamina > 0 and not player.poisoning:
                        player.sprint = True
                        player.stamina -= 1
                        player.detectablebyenemies = 100
                        player.movement[0] *= 4
                        player.movement[1] *= 4
                    
                    # joy_btn_menu1 = joystick.get_button(4)
                    # if joy_btn_menu1:
                    #     in_menu = True
                    #     menu1joy(joystick)
                    joy_btn_menu3 = joystick.get_axis(4)
                    joy_btn_status = joystick.get_button(4)
                    if joy_btn_menu3 > 0:
                        in_menu = True
                        player.nodegraph.show(joystick)
                    elif joy_btn_status:
                        in_menu = True
                        status()

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
                        if coll.interacted > 0:
                            speech_bool = True
                        s_entity = coll
                        dialogue_list = [["player", "Haha eat this!"], ["enemy", "Ouch! you will pay for this."], ["player", "Let's see about that"], ["enemy", "Grrrrrr..."]]

                        # coll.movement[0] = -coll.movement[0]
                        # coll.movement[1] = -coll.mov  ement[1]
                    else:
                        player.hp -= 1
                        # speech_engine(player, coll, [["player", "Ouch!"], ["enemy", "Get lost!"], ["player", "I'll come back for you."], ["enemy", "..."]])
                        if coll.interacted > 0:
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

        for enemy in EnemyGroup:
            if player.attackrect.colliderect(enemy.rect):
                if controller_connected:
                    pass

                    """
        ecoll = pygame.sprite.spritecollide(player, EnemyGroup, False)
        for coll in ecoll:
            if coll.type == "npc":
                if coll.hostile:

                    # print("enemy detected")     
                    # if (pcollside["front"] and player.movement[1] < 0) or (pcollside["back"] and player.movement[1] > 0) or(pcollside["left"] and player.movement[0] < 0) or (pcollside["right"] and player.movement[0] > 0):
                    if player.active1 > -1:
                        coll.hp -= 1
                        # speech_engine(player, coll, [["player", "Haha eat this!"], ["enemy", "Ouch! you will pay for this."], ["player", "Let's see about that"], ["enemy", "Grrrrrr..."]])
                        if coll.interacted > 0:
                            speech_bool = True
                        s_entity = coll
                        dialogue_list = [["player", "Haha eat this!"], ["enemy", "Ouch! you will pay for this."], ["player", "Let's see about that"], ["enemy", "Grrrrrr..."]]

                        # coll.movement[0] = -coll.movement[0]
                        # coll.movement[1] = -coll.movement[1]
                    else:
                        player.hp -= 1
                        # speech_engine(player, coll, [["player", "Ouch!"], ["enemy", "Get lost!"], ["player", "I'll come back for you."], ["enemy", "..."]])
                        if coll.interacted > 0:
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
                    """
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

        #endregion

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
                pygame.mouse.set_visible(False)
                controller_connected = True
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                joystick = joysticks[0]
                # print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                pygame.mouse.set_visible(True)
                controller_connected = False
                del joysticks[event.instance_id]
                # print(f"Joystick {event.instance_id} disconnected")
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
