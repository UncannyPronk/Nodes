import pygame
import sys
from pygame import *
from pygame.locals import *
from pygame import mixer
from random import randint as rd
import json

pygame.init()
sw, sh = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((sw, sh), pygame.FULLSCREEN)
clock = pygame.time.Clock()
display = pygame.Surface([1000, 600])
display_rect = Rect(0, 0, 1000, 600)

prev_state = "idle"

with open("tilemap.json", 'r') as tilemap_file:
    tilemap = json.load(tilemap_file)

tilemap_img = pygame.image.load("tilesetimage.png")

def write(blit=True, text='sample text', position=(0, 0), color=(0, 0, 0), fontsize=20, font='arial'):
    font = pygame.font.SysFont(font, fontsize)
    text = font.render(text, True, color)
    if blit:
        screen.blit(text, position)
    else:
        return text, position

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.spritesheet = pygame.image.load("player_img.png")
        self.spritesheet = pygame.transform.scale(
            self.spritesheet, (512, 3*64))
        self.image = pygame.Surface([64, 64])
        self.image.blit(self.spritesheet, (0, 0), (0, 0, 64, 64))
        self.image.set_colorkey((0, 255, 0))
        self.actual_rect = pygame.Rect(300, 220, 64, 64)
        self.rect = pygame.Rect(300, 220, 64, 64)
        self.animationvar = 0
        self.attributes = []
        self.state = "idle"
        self.controller = False
        self.direction = "right"
        self.movement = [0, 0]
        self.evade = False
        self.grav = 0
        self.on_ground = False
        self.prev_state = self.state
        self.hp = 100
        self.attackpower = 10
        self.jumpable = False

    def reset(self):
        self.evade = False
        self.state = "idle"
        self.direction = "right"
        self.hp = 100
        self.grav = 0
        self.rect = pygame.Rect(300, 220, 64, 64)
        self.actual_rect = pygame.Rect(300, 220, 64, 64)
        self.attributes = []
        self.jumpable = False
        self.controller = False

    def move(self, tiles):
        collision_types = {"right": False,
                           "left": False, "top": False, "bottom": False}
        if self.state != "idle":
            if self.on_ground:
                self.actual_rect.x += self.movement[0]
            else:
                self.actual_rect.x += self.movement[0]/2
        hit_list = []
        for tile in tiles:
            if self.actual_rect.colliderect(tile):
                hit_list.append(tile)
        for tile in hit_list:
            if self.movement[0] > 0:
                collision_types["right"] = True
                self.actual_rect.right = tile.left - 2
                # self.direction = "left"
                if self.jumpable and self.on_ground:
                    self.grav = -6
            elif self.movement[0] < 0:
                collision_types["left"] = True
                self.actual_rect.left = tile.right + 2
                # self.direction = "right"
        self.actual_rect.y += self.movement[1]
        hit_list = []
        for tile in tiles:
            if self.actual_rect.colliderect(tile):
                hit_list.append(tile)
        self.on_ground = False
        for tile in hit_list:
            if self.movement[1] > 0:
                collision_types["bottom"] = True
                self.actual_rect.bottom = tile.top
                self.grav = 0
                self.on_ground = True
            elif self.movement[1] < 0:
                collision_types["top"] = True
                self.actual_rect.top = tile.bottom
        return collision_types

    def update(self):
        self.rect.x = self.actual_rect.x - scroll[0]
        self.rect.y = self.actual_rect.y - scroll[1]
        self.animationvar += 0.2
        if self.animationvar >= 8:
            self.animationvar = 0
            if self.state == "sword":
                self.state = self.prev_state
        self.grav += 0.2
        self.image.fill((0, 255, 0))
        if self.state == "idle":
            if self.evade:
                for enemy in enemylist:
                    if self.actual_rect.x < enemy.actual_rect.x:
                        if player.actual_rect.right > enemy.actual_rect.x - 180:
                            self.image.blit(self.spritesheet, (0, 0), (int(
                                self.animationvar)*64, 1*64, 64, 64))
                            self.direction = "left"
                        else:
                            self.image.blit(self.spritesheet, (0, 0), (int(
                                self.animationvar)*64, 0*64, 64, 64))
                    else:
                        self.image.blit(self.spritesheet, (0, 0), (int(
                            self.animationvar)*64, 0*64, 64, 64))
            else:
                self.image.blit(self.spritesheet, (0, 0),
                                (int(self.animationvar)*64, 0*64, 64, 64))
        if self.state == "walk":
            if self.evade:
                for enemy in enemylist:
                    if self.actual_rect.x < enemy.actual_rect.x and (player.actual_rect.y < enemy.actual_rect.bottom and player.actual_rect.bottom > enemy.actual_rect.y):
                        if player.actual_rect.right > enemy.actual_rect.x - 200 and player.actual_rect.right < enemy.actual_rect.x - 180:
                            self.image.blit(self.spritesheet, (0, 0), (int(
                                self.animationvar)*64, 0*64, 64, 64))
                            self.actual_rect.x -= 2
                            self.direction = "left"
                        elif player.actual_rect.right > enemy.actual_rect.x - 180:
                            self.image.blit(self.spritesheet, (0, 0), ((
                                (8 - int(self.animationvar)) - 1)*64, 1*64, 64, 64))
                            self.direction = "left"
                        else:
                            self.image.blit(self.spritesheet, (0, 0), (int(
                                self.animationvar)*64, 1*64, 64, 64))
                            self.direction = "right"
                    else:
                        self.image.blit(self.spritesheet, (0, 0), (int(
                            self.animationvar)*64, 1*64, 64, 64))
                        self.direction = "right"
            else:
                if not self.controller:
                    if self.grav < 1:
                        self.image.blit(self.spritesheet, (0, 0),
                                        (int(self.animationvar)*64, 1*64, 64, 64))
                    else:
                        self.image.blit(self.spritesheet, (0, 0),
                                        (int(self.animationvar)*64, 0*64, 64, 64))
                else:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_w] and self.grav < 0.5:
                        self.grav = -4
                    if keys_pressed[K_d]:
                        self.direction = "right"
                        self.image.blit(self.spritesheet, (0, 0), (int(
                            self.animationvar)*64, 1*64, 64, 64))
                    elif keys_pressed[K_a]:
                        self.direction = "left"
                        self.image.blit(pygame.transform.flip(
                            self.spritesheet, 1, 0), (0, 0), (int(self.animationvar)*64, 1*64, 64, 64))
                    else:
                        self.image.blit(self.spritesheet, (0, 0), (int(
                            self.animationvar)*64, 0*64, 64, 64))
        if self.state == "sword":
            self.image.blit(self.spritesheet, (0, 0),
                            (int(self.animationvar)*64, 2*64, 64, 64))
        self.image.set_colorkey((0, 255, 0))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
        super(Enemy, self).__init__()
        self.spritesheet = pygame.image.load("enemy_img.png")
        self.spritesheet = pygame.transform.scale(
            self.spritesheet, (512, 3*64))
        self.image = pygame.Surface([64, 64])
        self.image.blit(self.spritesheet, (0, 0), (0, 0, 64, 64))
        self.image.set_colorkey((0, 255, 0))
        self.orig_pos = xpos, ypos
        self.rect = pygame.Rect(xpos, ypos, 64, 64)
        self.actual_rect = self.rect
        self.animationvar = 0
        self.state = "walk"
        self.direction = "left"
        self.prev_state = self.state
        self.grav = 0
        self.attackpower = 5
        self.hp = 50
        self.movement = [0, 0]

    def reset(self):
        self.rect = pygame.Rect(self.orig_pos[0], self.orig_pos[1], 64, 64)
        self.actual_rect = pygame.Rect(
            self.orig_pos[0], self.orig_pos[1], 64, 64)
        self.state = "walk"
        self.direction = "left"
        self.grav = 0

    def move(self, tiles):
        collision_types = {"right": False,
                           "left": False, "top": False, "bottom": False}
        if self.state != "idle":
            self.actual_rect.x += self.movement[0]
        hit_list = []
        for tile in tiles:
            if self.actual_rect.colliderect(tile):
                hit_list.append(tile)
        for tile in hit_list:
            if self.movement[0] > 0:
                collision_types["right"] = True
                self.actual_rect.right = tile.left
                self.direction = "left"
            elif self.movement[0] < 0:
                collision_types["left"] = True
                self.actual_rect.left = tile.right
                self.direction = "right"
        self.actual_rect.y += self.movement[1]
        hit_list = []
        for tile in tiles:
            if self.actual_rect.colliderect(tile):
                hit_list.append(tile)
        for tile in hit_list:
            if self.movement[1] > 0:
                collision_types["bottom"] = True
                self.actual_rect.bottom = tile.top
                self.grav = 0
            elif self.movement[1] < 0:
                collision_types["top"] = True
                self.actual_rect.top = tile.bottom
        return collision_types

    def update(self):
        self.rect.x = self.actual_rect.x - scroll[0]
        self.rect.y = self.actual_rect.y - scroll[1]
        self.animationvar += 0.2
        if self.animationvar >= 8:
            self.animationvar = 0
            if self.state == "sword":
                self.state = self.prev_state
        self.grav += 0.2
        self.image.fill((0, 255, 0))
        if self.state == "idle":
            self.image.blit(self.spritesheet, (0, 0),
                            (int(self.animationvar)*64, 0*64, 64, 64))
        if self.state == "walk":
            if self.direction == "left":
                self.image.blit(self.spritesheet, (0, 0),
                                (int(self.animationvar)*64, 1*64, 64, 64))
                self.movement[0] = -2
            elif self.direction == "right":
                self.image.blit(pygame.transform.flip(
                    self.spritesheet, 1, 0), (0, 0), (((8 - int(self.animationvar)) - 1)*64, 1*64, 64, 64))
                self.movement[0] = 2
        if self.state == "sword":
            self.image.blit(self.spritesheet, (0, 0),
                            (int(self.animationvar)*64, 2*64, 64, 64))
        self.image.set_colorkey((0, 255, 0))

class Node:
    def __init__(self, x, y, no=3, name="New Node"):
        self.rect = Rect(x*300 + 20, y*200 + 80, 200, 100)
        self.name = name
        self.inputno = no

        if self.inputno > 3:
            self.inputno = 3

        self.anchor = False
        self.activated = True
        self.selected = False
        self.editedname = False
        self.namespace = pygame.Surface(self.rect.size)
        self.outrect = [Rect(0, 0, 10, 20), 0]
        self.inrects = []

        for i in range(self.inputno):
            self.inrects.append(
                [Rect(self.rect.x - 10, self.rect.y - 20 + 30*(i+1), 10, 20), 0])

    def display(self):
        result = False

        mx, my = pygame.mouse.get_pos()
        if not self.rect.collidepoint(mx, my):
            pygame.draw.rect(self.namespace, (10, 10, 10),
                             (0, 0, self.rect.width, self.rect.height))
        else:
            pygame.draw.rect(self.namespace, (30, 30, 30),
                             (0, 0, self.rect.width, self.rect.height))
            result = True

        if self.selected:
            pygame.draw.rect(self.namespace, (100, 30, 30),
                             (0, 0, self.rect.width, self.rect.height))

        text, textpos = write(False, self.name, (20, 30), (0, 255, 100), 40)

        self.namespace.blit(text, textpos)
        pygame.draw.rect(self.namespace, (255, 255, 255),
                         (0, 0, self.rect.width, self.rect.height), 3)
        screen.blit(self.namespace, self.rect.topleft)

        for i in range(self.inputno):
            pygame.draw.rect(screen, (30, 100, 255),
                             (self.rect.x - 10, self.rect.y - 20 + 30*(i+1), 10, 20))
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.rect.right, self.rect.centery - 10, 10, 20))

        self.outrect[0].x, self.outrect[0].y = self.rect.right, self.rect.centery - 10

        if pygame.mouse.get_pressed()[0]:
            if self.outrect[1]:
                pygame.draw.line(screen, (255, 255, 255),
                                 (mx, my), (self.outrect[0].center), 3)
            elif self.outrect[0].collidepoint(mx, my):
                self.outrect[1] = 1
        else:
            self.outrect[1] = 0

        for i in range(len(self.inrects)):
            self.inrects[i][0].x = self.rect.x - 10
            self.inrects[i][0].y = self.rect.y - 20 + 30*(i+1)

        return result

class Trigger(pygame.sprite.Sprite):
    def __init__(self):
        super(Trigger, self).__init__()
        self.rect = Rect(0, 0, 64, 16)
        self.actual_rect = self.rect
        self.image = pygame.Surface([60, 10])
        self.image.fill((255, 0, 0))

    def triggerzone(self, entity):
        if self.actual_rect.colliderect(entity.actual_rect):
            return True
        else:
            return False

player = Player()
playergrp = pygame.sprite.Group()
playergrp.add(player)

level = 1

enemylist = []
enemygrp = pygame.sprite.Group()
enemylist.append(Enemy(700, 260))
enemylist.append(Enemy(2100, 550))
for enemy in enemylist:
    enemygrp.add(enemy)

nodes = []
nodes.append(Node(3, 2, 3, "Player"))
nodes.append(Node(1, 2, 1, "Walk"))
nodes.append(Node(2, 3, 1, "Sword"))
nodes.append(Node(1, 1, 1, "Jump"))
nodes.append(Node(0, 0, 0, "Evade"))
nodes.append(Node(0, 3, 0, "WASD"))

nodes_avail = []
nodes_avail.append(nodes[0])
nodes_avail.append(nodes[1])
# nodes_avail.append(nodes[2])
# nodes_avail.append(nodes[3])
# nodes_avail.append(nodes[4])

connections = []

def save():
    with open("savefile.json", "w") as savefile:
        json.dump(level, savefile)
    while True:
        pygame.display.update()
        screen.fill((10, 10, 10))
        write(True, "Level 2 coming soon!", (sw/3, sh/2), (255, 255, 255), 60)
        for ev in pygame.event.get():
            if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
# save()

def load():
    with open("savefile.json", "r") as savefile:
        global level
        level = json.load(savefile)

class Checkpoint(Trigger):
    def __init__(self, x, y):
        super(Checkpoint, self).__init__()
        self.actual_rect = Rect(x, y, 64, 16)
        self.animationvar = 0
        self.spritesheet = pygame.image.load("checkpoint_flag.png")
        self.spritesheet = pygame.transform.scale(
            self.spritesheet, (64*8, 64))
        self.image = pygame.Surface([64, 64])
        self.image.blit(self.spritesheet, (0, 0), (0, 0, 64, 64))
        self.image.set_colorkey((0, 255, 0))

    def update(self):
        global scroll
        self.rect.x = self.actual_rect.x - scroll[0]
        self.rect.y = self.actual_rect.y - scroll[1]
        self.animationvar += 0.2
        if self.animationvar > 8:
            self.animationvar = 0
        self.image.fill((0, 255, 0))
        self.image.blit(self.spritesheet, (0, 0),
                        (int(self.animationvar)*64, 0, 64, 64))
        self.image.set_colorkey((0, 255, 0))
        self.rect.x, self.rect.y = self.actual_rect.x - \
            scroll[0], self.actual_rect.y - scroll[1]
        if self.triggerzone(player):
            save()

triggerlist = []
triggergrp = pygame.sprite.Group()
for i in range(1):
    triggerlist.append(Checkpoint(2558, 771))
for trigger in triggerlist:
    triggergrp.add(trigger)

def node_graph():
    running = True
    key_time = 0
    while running:
        screen.fill((0, 25, 20))

        write(True, "Node Graph", (550, 30), (0, 120, 80), 100)

        # Node follows mouse when selected
        hover = []
        for node in nodes_avail:
            hover.append(node.display())
            if node.anchor:
                node.rect.centerx, node.rect.centery = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
                # for node in nodes_avail:
                #     if node.selected:
                #         if not node.editedname:
                #             node.name = ""
                #             node.editedname = True
                #         if event.key == K_DELETE:
                #             node.name = ""
                #         if event.key == K_BACKSPACE:
                #             node.name = node.name[:-1]
                #         elif event.key == K_MINUS:
                #             node.name += "_"
                #         elif event.key == K_SPACE:
                #             node.name += " "
                #         elif len(node.name) < 12:
                #             node.name += event.unicode
            if event.type == MOUSEBUTTONDOWN:
                if Rect(sw - 100, 30, 40, 40).collidepoint(event.pos):
                    gameloop()
                else:
                    for i in range(len(nodes_avail)):
                        if hover[i]:
                            nodes_avail[i].anchor = True
                            nodes_avail[i].selected = not nodes_avail[i].selected
                        else:
                            nodes_avail[i].selected = False
                    for connection in connections:
                        for node1 in nodes_avail:
                            if node1.name == connection[1][0]:
                                for node2 in nodes_avail:
                                    if node1 != node2:
                                        if node2.name == connection[1][1]:
                                            for rect in node2.inrects:
                                                if rect[0].collidepoint(event.pos) and connection[0][1].colliderect(rect[0]):
                                                    connections.remove(
                                                        connection)
                                                    rect[1] = 0
            if event.type == MOUSEBUTTONUP:
                if len(nodes_avail) > 1:
                    for node1 in nodes_avail:
                        for node2 in nodes_avail:
                            if node1 != node2:
                                node1.anchor = False
                                if node1.outrect[1]:
                                    for rect in node2.inrects:
                                        if rect[0].collidepoint(pygame.mouse.get_pos()) and rect[1] == 0:
                                            connections.append(
                                                [[node1.outrect[0], rect[0]], [node1.name, node2.name, node1.activated]])
                                            rect[1] = 1
                                            for connection1 in connections:
                                                for connection2 in connections:
                                                    if not connection1 == connection2:
                                                        if connection1[1][0] == connection2[1][0] and connection1[1][1] == connection2[1][1]:
                                                            connections.pop()
                                                            rect[1] = 0
                else:
                    nodes_avail[0].anchor = False
            if event.type == KEYDOWN:
                if (event.key == K_LCTRL or event.key == K_RCTRL) and event.key == K_l:
                    load()

        # Edit the node name
        for node in nodes_avail:
            if node.selected:
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[K_BACKSPACE] and len(node.name) > 0:
                    key_time += 0.1
                    if key_time > 3:
                        node.name = node.name[:-1]
                else:
                    key_time = 0

        for node in connections:
            pygame.draw.line(screen, (255, 255, 255),
                             node[0][0].center, node[0][1].center, 3)

        pygame.draw.polygon(screen, (10, 255, 100), ((
            sw - 100, 30), (sw - 60, 50), (sw - 100, 70)))

        pygame.display.update()
        clock.tick(30)

def nodes_init(connections):
    for c in connections:
        if c[1][1] == "Player":
            if c[1][0] == "Walk":
                player.state = "walk"
                for c1 in connections:
                    if c1[1][1] == "Walk" and c1[1][0] == "WASD" and c[1][2] == True:
                        player.controller = True
                # if c[1][2] == True:
                #     player.state = "walk"
                #     for c1 in connections:
                #         if c1[1][1] == "Walk" and c1[1][0] == "WASD" and c[1][2] == True:
                #             player.controller = True
                # else:
                #     player.state = "idle"

            player.evade = player.jumpable = False
            if c[1][0] == "Evade" and c[1][2] == True:
                player.evade = True
            if c[1][0] == "Sword":
                player.attributes.append("Sword")
                # player.state = "sword"
                # if c[1][2] == True:
                #     player.attributes.append("Sword")
                # else:
                #     player.attributes.remove("Sword")
            if c[1][0] == "Jump" and c[1][2] == True:
                player.jumpable = True

scroll = [0, 0]

def gameloop():
    running = True
    count = 0
    global level
    player.reset()
    for enemy in enemylist:
        enemy.reset()
    nodes_init(connections)
    while running:
        activerects = [Rect(0, 0, 0, 0),
                    Rect(0, 0, 0, 0),
                    Rect(0, 0, 0, 0)]
        sw, sh = pygame.display.Info().current_w, pygame.display.Info().current_h
        scroll[0] += (player.actual_rect.x - scroll[0] - 368)/10
        scroll[1] += (player.actual_rect.y - scroll[1] - 268)/10
        display_rect.x, display_rect.y = scroll[0], scroll[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    if 2 <= level <= 3:
                        player.hp = 0
                if event.key == K_x:
                    print(player.actual_rect.topleft)
            if event.type == MOUSEBUTTONDOWN:
                for i in range(len(connections)):
                    if activerects[i].collidepoint(event.pos):
                        # connections[i][1][2] = not connections[i][1][2]
                        pass

        # keys_pressed = pygame.key.get_pressed()
        # if keys_pressed[K_SPACE]:
        #     for att in player.attributes:
        #         if att == "Sword" and not player.state == "sword":
        #             global prev_state
        #             prev_state = player.state
        #             player.state = "sword"
        #             player.animationvar = 0

        for i in range(len(enemylist)):
            if enemylist[i].hp <= 0:
                enemylist[i].kill()
                enemylist.pop(i)
                break

        if player.hp <= 0:
            running = False
            player.reset()
            level += 1
            nodes_avail.append(nodes[level])

        for enemy in enemylist:
            if enemy.actual_rect.colliderect(player.actual_rect):
                # player
                for att in player.attributes:
                    if att == "Sword" and not player.state == "sword":
                        player.prev_state = player.state
                        player.state = "sword"
                        # player.animationvar = 0
                # enemy
                if not enemy.state == "sword":
                    enemy.prev_state = enemy.state
                enemy.state = "sword"
                if enemy.animationvar > 4:
                    player.actual_rect.x -= enemy.attackpower*4
                    player.hp -= enemy.attackpower
                # print("Enemy encountered: " + player.state)
                # print(player.state)
                # print(player.animationvar)
                if player.state == "sword" and player.animationvar > 4:
                    enemy.actual_rect.x += player.attackpower*4
                    enemy.hp -= player.attackpower
            else:
                enemy.state = "walk"

        tilerects = []
        y = 0
        for row in tilemap:
            x = 0
            for tile in row:
                if tile > 0:
                    tilerects.append(Rect(x*64, y*64, 64, 64))
                x += 1
            y += 1

        player.movement = [0, 0]
        if player.direction == "right":
            player.movement[0] = 2
        if player.direction == "left":
            player.movement[0] = -2
        player.movement[1] += player.grav

        for enemy in enemylist:
            enemy.movement[1] = 0
            enemy.movement[1] += enemy.grav
            enemy.move(tilerects)

        player.move(tilerects)

        display.fill((10, 55, 120))
        y = 0
        for row in tilemap:
            x = 0
            for tile in row:
                if tile > 0 and Rect(x*64, y*64, 64, 64).colliderect(display_rect):
                    if tile == 1:
                        display.blit(pygame.transform.scale(
                            tilemap_img, (192, 192)), (x*64 - scroll[0], y*64 - scroll[1]), (0, 0, 64, 64))
                    if tile == 2:
                        display.blit(pygame.transform.scale(
                            tilemap_img, (192, 192)), (x*64 - scroll[0], y*64 - scroll[1]), (64, 0, 64, 64))
                    if tile == 3:
                        display.blit(pygame.transform.scale(
                            tilemap_img, (192, 192)), (x*64 - scroll[0], y*64 - scroll[1]), (128, 0, 64, 64))
                    if tile == 4:
                        display.blit(pygame.transform.scale(
                            tilemap_img, (192, 192)), (x*64 - scroll[0], y*64 - scroll[1]), (0, 64, 64, 64))
                    if tile == 5:
                        display.blit(pygame.transform.scale(
                            tilemap_img, (192, 192)), (x*64 - scroll[0], y*64 - scroll[1]), (64, 64, 64, 64))
                    if tile == 6:
                        display.blit(pygame.transform.scale(
                            tilemap_img, (192, 192)), (x*64 - scroll[0], y*64 - scroll[1]), (128, 64, 64, 64))
                    if tile == 7:
                        display.blit(pygame.transform.scale(
                            tilemap_img, (192, 192)), (x*64 - scroll[0], y*64 - scroll[1]), (0, 128, 64, 64))
                    if tile == 8:
                        display.blit(pygame.transform.scale(
                            tilemap_img, (192, 192)), (x*64 - scroll[0], y*64 - scroll[1]), (64, 128, 64, 64))
                    if tile == 9:
                        display.blit(pygame.transform.scale(
                            tilemap_img, (192, 192)), (x*64 - scroll[0], y*64 - scroll[1]), (128, 128, 64, 64))
                x += 1
            y += 1

        playergrp.draw(display)
        playergrp.update()
        enemygrp.draw(display)
        enemygrp.update()
        triggergrp.draw(display)
        triggergrp.update()

        screen.blit(pygame.transform.scale(display, (sw, sh)), (0, 0))

        for i in range(len(connections)):
            if connections[i][1][2]:
                pygame.draw.rect(screen, (255, 255, 255), ((sw/2 + i*100)-(len(connections)*50 - 25), sh - 200, 50, 50))
            else:
                pygame.draw.rect(screen, (255, 0, 0), ((sw/2 + i*100)-(len(connections)*50 - 25), sh - 200, 50, 50))
            activerects[i] = Rect((sw/2 + i*100)-(len(connections)*50 - 25), sh - 200, 50, 50)

        # for node in nodes:
        #     for i in range(len(connections)):
        #         if node.name == connections[i][1][0]:
        #             node.activated = connections[i][1][2]
        nodes_init(connections)
        # if player.state == "sword":
        #     print("state:"+player.state)
        # print(connections[0][1][2], nodes[1].activated)

        if level == 2:
            count += 1
            if count > 500:
                write(True, "[Press Esc if you are stuck or want to go back to the node graph anytime]", (sw/2 - 520, 120), (255, 255, 255), 40)
        pygame.display.update()
        clock.tick(120)

if __name__ == "__main__":
    # main menu
    node_graph()
