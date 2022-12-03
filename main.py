import pygame, sys
from pygame import * 
from pygame.locals import *
from pygame import mixer
from random import randint as rd

pygame.init()
sw, sy = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((sw,sy))
clock = pygame.time.Clock()

def write(blit=True, text='sample text', position=(0, 0), color=(0, 0, 0), fontsize=20, font='arial'):
    font = pygame.font.SysFont(font, fontsize)
    text = font.render(text, True, color)
    if blit:
        screen.blit(text, position)
    else:
        return text, position

class Node:
    def __init__(self):
        self.rect = Rect(0, 0, 200, 100)
        self.name = "New Node"
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

node1 = Node()
node2 = Node()
connections = []

def node_graph():
    running = True
    hover1 = False
    key_time = 0
    while running:
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
                if node1.selected:
                    if not node1.editedname:
                        node1.name = ""
                        node1.editedname = True
                    if event.key == K_DELETE:
                        node1.name = ""
                    if event.key == K_BACKSPACE:
                        node1.name = node1.name[:-1]
                    elif event.key == K_MINUS:
                        node1.name += "_"
                    elif event.key == K_SPACE:
                        node1.name += " "
                    elif len(node1.name) < 12:
                        node1.name += event.unicode
                if node2.selected:
                    if not node2.editedname:
                        node2.name = ""
                        node2.editedname = True
                    if event.key == K_DELETE:
                        node2.name = ""
                    if event.key == K_BACKSPACE:
                        node2.name = node2.name[:-1]
                    elif event.key == K_MINUS:
                        node2.name += "_"
                    elif event.key == K_SPACE:
                        node2.name += " "
                    elif len(node2.name) < 12:
                        node2.name += event.unicode
            if event.type == MOUSEBUTTONDOWN:
                if hover1:
                    node1.anchor = True
                    node1.selected = not node1.selected
                else:
                    node1.selected = False
                if hover2:
                    node2.anchor = True
                    node2.selected = not node2.selected
                else:
                    node2.selected = False
            if event.type == MOUSEBUTTONUP:
                node1.anchor = False
                node2.anchor = False
                print(0)
                if node1.outrect[1]:
                    print(1)
                    for rect in node2.inrects:
                        print(rect[0].x, rect[0].y)
                        if rect[0].collidepoint(pygame.mouse.get_pos()):
                            print(2)
                            connections.append([node1.outrect[0], rect[0]])
                            rect[1] = 1
                if node2.outrect[1]:
                    print(1.1)
                    for rect in node1.inrects:
                        print(rect[0].x, rect[0].y)
                        if rect[0].collidepoint(pygame.mouse.get_pos()):
                            print(2.1)
                            connections.append([node2.outrect[0], rect[0]])
                            rect[1] = 1

        # Edit the node name
        if node1.selected:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[K_BACKSPACE] and len(node1.name) > 0:
                key_time += 0.1
                if key_time > 3:
                    node1.name = node1.name[:-1]
            else:
                key_time = 0

        if node2.selected:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[K_BACKSPACE] and len(node2.name) > 0:
                key_time += 0.1
                if key_time > 3:
                    node2.name = node2.name[:-1]
            else:
                key_time = 0

        screen.fill((0, 25, 20))

        # Node follows mouse when selected
        hover1 = node1.display()
        hover2 = node2.display()
        if node1.anchor:
            node1.rect.centerx, node1.rect.centery = pygame.mouse.get_pos()
        elif node2.anchor:
            node2.rect.centerx, node2.rect.centery = pygame.mouse.get_pos()
        
        for node in connections:
            pygame.draw.line(screen, (255, 255, 255), node[0].center, node[1].center, 3)
            
        pygame.display.update()
        clock.tick(60)

def gameloop():
    running = True
    while running:
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


            screen.fill((0, 25, 20))

            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    node_graph()
