import pygame, sys
from pygame import * 
from pygame.locals import *
from pygame import mixer
from random import randint as rd
#oo

pygame.init()
sw, sy = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((sw,sy))
clock = pygame.time.Clock()

def write(text='sample text', position=(0, 0), color=(0, 0, 0), fontsize=20, font='arial'):
    font = pygame.font.SysFont(font, fontsize)
    text = font.render(text, True, color)
    screen.blit(text, position)

class Node:
    def __init__(self):
        self.rect = Rect(0, 0, 400, 200)
        self.name = "New Node"
        self.input = None
        self.output = None
    def display(self):
        mx, my = pygame.mouse.get_pos()
        if not self.rect.collidepoint(mx, my):
            pygame.draw.rect(screen, (10, 10, 10), self.rect)
        else:
            pygame.draw.rect(screen, (30, 30, 30), self.rect)
        write(self.name, self.rect.topleft, (0, 255, 100))
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)

node1 = Node()

def node_graph():
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

            node1.display()

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
