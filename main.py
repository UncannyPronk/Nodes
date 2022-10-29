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
        self.input = None
        self.inputno = 3
        self.output = None
        self.anchor = False
        self.selected = False
        self.editedname = False
        self.namespace = pygame.Surface(self.rect.size)
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
        return result

node1 = Node()

def node_graph():
    running = True
    hover = False
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
            if event.type == MOUSEBUTTONDOWN:
                if hover:
                    node1.anchor = True
                    node1.selected = not node1.selected
                else:
                    node1.selected = False
            if event.type == MOUSEBUTTONUP:
                node1.anchor = False
        if node1.selected:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[K_BACKSPACE] and len(node1.name) > 0:
                key_time += 0.1
                if key_time > 3:
                    node1.name = node1.name[:-1]
            else:
                key_time = 0

        screen.fill((0, 25, 20))

        hover = node1.display()
        if node1.anchor:
            node1.rect.centerx, node1.rect.centery = pygame.mouse.get_pos()

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
