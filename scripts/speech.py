import winsound, random, pygame
from pygame.locals import *
from scripts.global_vars import display_rect, screen, controller_connected, joysticks, name_dict, ruined_talked, remaining_missions, new_mission
from scripts.funcs import write


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
            write(True, dialoguestr, (100, 20), color, 42)
            write(True, "Press Enter", (display_rect.w - 150, 60), (255, 255, 255))
            if dialogues[speech_index][0] == "player":
                screen.blit(player.sprite.image, (30, 10))
            else:
                screen.blit(entity.sprite.image, (30, 10))
        except IndexError:
            # print("IndexError - An error has been triggered")
            if entity.id != "country":
                entity.interacted = 0
            speech_bool = False
            s_entity = None
            dialogue_list = []
            speech_index = 0

        # for ev in pygame.event.get():
        #     if ev.type == KEYDOWN and ev.key == K_RETURN:
        #         speech_index += 1
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
                # for event in pygame.event.get():
                #     if event.type == pygame.JOYBUTTONDOWN:
                #         if event.button == 0:
                #             if dialogueindex == dialoguelen:
                #                 speech_index += 1
                #                 dialogueindex = 0
                #                 keypress = False
                #             else:
                #                 dialogueindex = dialoguelen
                #                 keypress = False
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
        dialogue_list = [["guide1", "You appear to be lost."], ["player", "I'm not exactly lost..."], ["player", "but I am low on resources."], ["guide1", "Keep heading EAST till you find a village."], ["guide1", "Salvation is nearing us..."], ["player", "What?"], ["guide1", "Nothing. Keep heading EAST."]]

    return dialogue_list
