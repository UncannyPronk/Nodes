import pygame, random
from pygame.locals import *
from scripts.global_vars import display_rect, PlayerGroup, SpriteGroup, VillageGroup, NPCGroup, EnemyGroup, ObjectGroup
from scripts.char_obj import Player, Character
from scripts.place_obj import LoreVillage
from scripts.etc_obj import Tree

if pygame.joystick.get_count() > 0:
    prevkey = pygame.joystick.Joystick(0).get_button(0)
else:
    prevkey = pygame.key.get_pressed()
    
bg = pygame.Surface((display_rect.w, display_rect.h))
bg.fill((0, 0, 0))
bg.set_alpha(0)

player = Player()
player.add(PlayerGroup)
player.sprite.add(SpriteGroup)
# player.hitbox.add(HitBoxGroup)
player.sprite.rect.center = 500, 400
pygame.mouse.set_pos(500, 400)

lore1v = LoreVillage(3000, -800)
lore1v.add(VillageGroup)
lore1v.sprite.add(SpriteGroup)
lore1v.villagers[0].id = "ruined"
lore1v.villagers[0].sprite.color = (255, 0, 255)
lore1v.villagers[1].id = "country"
lore1v.villagers[1].sprite.color = (10, 255, 10)

guide1 = Character(100, 0)
guide1.add(NPCGroup)
guide1.sprite.add(SpriteGroup)
guide1.sprite.image.fill((255, 255, 0))
guide1.id = "guide1"

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