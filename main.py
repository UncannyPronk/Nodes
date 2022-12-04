import pygame, sys
from pygame import * 
from pygame.locals import *
from pygame import mixer
from random import randint as rd

pygame.init()
sw, sh = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((sw, sh))
clock = pygame.time.Clock()
display = pygame.Surface([1000, 600])

def write(blit=True, text='sample text', position=(0, 0), color=(0, 0, 0), fontsize=20, font='arial'):
    font = pygame.font.SysFont(font, fontsize)
    text = font.render(text, True, color)
    if blit:
        screen.blit(text, position)
    else:
        return text, position

class Player(pygame.sprite.Sprite):
    def __init__(self, attributes=[]):
        super(Player, self).__init__()
        self.spritesheet = pygame.image.load("player_img.png")
        self.spritesheet = pygame.transform.scale(self.spritesheet, (512, 128))
        self.image = pygame.Surface([64, 64])
        self.image.blit(self.spritesheet, (0, 0), (0, 0, 64, 64))
        self.image.set_colorkey((0, 255, 0))
        self.rect = pygame.Rect(300, 336, 64, 64)
        self.animationvar = 0
        self.attributes = attributes
        self.state = "walk"
    def reset(self):
        self.state = "idle"
    def update(self):
        self.animationvar += 0.2
        if self.animationvar >= 8:
            self.animationvar = 0
        self.image.fill((0, 255, 0))
        if self.state == "idle":
            self.image.blit(self.spritesheet, (0, 0), (int(self.animationvar)*64, 0, 64, 64))
        if self.state == "walk":
            self.image.blit(self.spritesheet, (0, 0), (int(self.animationvar)*64, 64, 64, 64))
        self.image.set_colorkey((0, 255, 0))

class Node:
    def __init__(self, x, no=3, name="New Node"):
        self.rect = Rect(x*300 + 20, 200, 200, 100)
        self.name = name
        self.inputno = no

        if self.inputno > 3:
            self.inputno = 3

        self.anchor = False
        self.selected = False
        self.editedname = False
        self.namespace = pygame.Surface(self.rect.size)
        self.outrect = [Rect(0, 0, 10, 20), 0]
        self.inrects = []
        
        for i in range(self.inputno):
            self.inrects.append([Rect(self.rect.x - 10, self.rect.y - 20 + 30*(i+1), 10, 20), 0])

    def display(self):
        result = False

        mx, my = pygame.mouse.get_pos()
        if not self.rect.collidepoint(mx, my):
            pygame.draw.rect(self.namespace, (10, 10, 10), (0, 0, self.rect.width, self.rect.height))
        else:
            pygame.draw.rect(self.namespace, (30, 30, 30), (0, 0, self.rect.width, self.rect.height))
            result = True

        if self.selected:
            pygame.draw.rect(self.namespace, (100, 30, 30), (0, 0, self.rect.width, self.rect.height))

        text, textpos = write(False, self.name, (20, 30), (0, 255, 100), 40)
        
        self.namespace.blit(text, textpos)
        pygame.draw.rect(self.namespace, (255, 255, 255), (0, 0, self.rect.width, self.rect.height), 3)
        screen.blit(self.namespace, self.rect.topleft)

        for i in range(self.inputno):
            pygame.draw.rect(screen, (30, 100, 255), (self.rect.x - 10, self.rect.y - 20 + 30*(i+1), 10, 20))
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.right, self.rect.centery - 10, 10, 20))

        self.outrect[0].x, self.outrect[0].y = self.rect.right, self.rect.centery - 10
        
        if pygame.mouse.get_pressed()[0]:
            if self.outrect[1]:
                pygame.draw.line(screen, (255, 255, 255), (mx, my), (self.outrect[0].center), 3)
            elif self.outrect[0].collidepoint(mx, my):
                self.outrect[1] = 1
        else:
            self.outrect[1] = 0

        for i in range(len(self.inrects)):
            self.inrects[i][0].x = self.rect.x - 10
            self.inrects[i][0].y = self.rect.y - 20 + 30*(i+1)

        return result

nodes = []
nodes.append(Node(3, 1, "Player"))
nodes.append(Node(0, 0, "Walk"))
connections = []

player = Player()
playergrp = pygame.sprite.Group()
playergrp.add(player)

def node_graph():
    running = True
    key_time = 0
    while running:
        screen.fill((0, 25, 20))

        write(True, "Node Graph", (550, 30), (0, 80, 30), 100)

        # Node follows mouse when selected
        hover = []
        for node in nodes:
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
                # for node in nodes:
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
                    for i in range(len(nodes)):
                        if hover[i]:
                            nodes[i].anchor = True
                            nodes[i].selected = not nodes[i].selected
                        else:
                            nodes[i].selected = False
                    for connection in connections:
                        for node1 in nodes:
                            if node1.name == connection[1][0]:
                                for node2 in nodes:
                                    if node1 != node2:
                                        if node2.name == connection[1][1]:
                                            for rect in node2.inrects:
                                                if rect[0].collidepoint(event.pos):
                                                    connections.remove(connection)
            if event.type == MOUSEBUTTONUP:
                if len(nodes) > 1:
                    for node1 in nodes:
                        for node2 in nodes:
                            if node1 != node2:
                                node1.anchor = False
                                if node1.outrect[1]:
                                    for rect in node2.inrects:
                                        if rect[0].collidepoint(pygame.mouse.get_pos()):
                                            connections.append([[node1.outrect[0], rect[0]], [node1.name, node2.name]])
                                            rect[1] = 1
                        
                else:
                    nodes[0].anchor = False

        # Edit the node name
        for node in nodes:
            if node.selected:
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[K_BACKSPACE] and len(node.name) > 0:
                    key_time += 0.1
                    if key_time > 3:
                        node.name = node.name[:-1]
                else:
                    key_time = 0
        
        for node in connections:
            pygame.draw.line(screen, (255, 255, 255), node[0][0].center, node[0][1].center, 3)
            
        pygame.draw.polygon(screen, (10, 255, 100), ((sw - 100, 30), (sw - 60, 50), (sw - 100, 70)))

        pygame.display.update()
        clock.tick(60)

def nodes_init(connections):
    for c in connections:
        if c[1][1] == "Player":
            if c[1][0] == "Walk":
                player.state = "walk"

def gameloop():
    running = True
    player.reset()
    nodes_init(connections)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[K_SPACE]:
                pass

        display.fill((10, 55, 120))
        pygame.draw.rect(display, (140, 100, 20), (0, 400, 1000, 200))
        playergrp.draw(display)
        playergrp.update()

        screen.blit(pygame.transform.scale(display, (sw, sh)), (0, 0))
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    #main menu
    node_graph()
