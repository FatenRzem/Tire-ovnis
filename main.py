# Importation de pygame
import random

import pygame
from pygame import mixer
# Initialisation de pygame (PG)
pygame.init()

# Créer une fenétre pour afficher le jeu
window = pygame.display.set_mode((800, 600))
# Modifier le titre et l'icone
pygame.display.set_caption("Tutoriel Pygame")
windowIcon = pygame.image.load("alien.png")
pygame.display.set_icon(windowIcon)

# On charge l'image du joueur
player = pygame.image.load("player.png")
playerRect = player.get_rect()
# Position du joueur à l'écran
posX = 350
posY = 480
# Image de background
bg = pygame.image.load("bg.png")
playerSpeed = 5

# Le laser
laser = pygame.image.load("laser.png")
laserRect = laser.get_rect()
laserSpeed = 4
poslaserX = 0
poslaserY = -100
canShoot = True

# L'OVNI
ovni = [] # Images
ovniRect = [] # Rect
pos0vniX =[] # pos X
posOvniY = [] # pos Y
ovniSpeed= [] # Tableau des vitesses
nbOvni = 4

# Texte
score = 0
font = pygame.font.Font("future.ttf", 36)
txtPos = 10

# Musique
# mixer.music.load("maMusique.wav")
# mixer.music.play(-1)

# Boucle de génération des monstres
for i in range(nbOvni):
    ovni.append(pygame.image.load("ufo.png"))
    ovniRect.append(ovni[i].get_rect())
    pos0vniX.append(random.randint(1,750))
    posOvniY.append(random.randint(0, 300))
    ovniSpeed.append(3)

# Fonction de détection de collision
def collision(rectA, rectB):
    if rectB.right < rectA.left:
        # rectB est à gauche
        return False
    if rectB.bottom < rectA.top:
        # rectB est au-dessus
        return False
    if rectB.left > rectA.right:
        # rectB est à droite
        return False
    if rectB.top > rectA.bottom:
        # rectB est au dessous
        return False
    # Dans tous les autres cas il y a collision
    return True

# Pour définir les FPS
clock = pygame.time.Clock()
# la boucle de jeu
running = True
while running:
    # Couleur de l'écran
    window.fill((0,0,0))
    window.blit(bg, (0, 0))
    # Je check tous les évenements (clavier/ souris)
    for event in pygame.event.get():
        # Est-ce-que l'utilisateur appuie sur une touche?
        pressed = pygame.key.get_pressed()
        # on teste si l'utiisateur appuie sur la croix de la fenetre
        if event.type == pygame.QUIT:
             # On quitte le jeu
             running = False
        # Détection barre d'espace pour tirer le laser
        if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE and canShoot:
                  laserSfx = mixer.Sound("sfx_laser.ogg")
                  laserSfx.play()
                  canshoot = False
                  poslaserX = posX + 45
                  poslaserY = posY - 50
   # Gestion du déplacement du joueur à l'écran
    if pressed[pygame.K_LEFT] and  posX > 0:
        posX -= playerSpeed
    if pressed[pygame.K_RIGHT] and posX < 700:
        posX += playerSpeed

    # Affichage joueur
    # On applique cette position au rectangle
    playerRect.topleft = (posX, posY)
    # On affiche l'image du joueur dans la fenetre
    window.blit(player, playerRect)

    # Gestion du laser
    poslaserY -= laserSpeed
    laserRect.topleft = (poslaserX, poslaserY)
    window.blit(laser, laserRect)
    if poslaserY < -40:
        canShoot = True

    # Gestion des OVNI
    for i in range(nbOvni):
        pos0vniX[i] -= ovniSpeed[i]
        ovniRect[i].topleft = (pos0vniX[i], posOvniY[i])
        window.blit(ovni[i], ovniRect[i])
        if pos0vniX[i] < 0 or pos0vniX[i] > 750:
           ovniSpeed[i] = -ovniSpeed[i]
           posOvniY[i] += 5

        # Y a til colllision entre le laser et lovni ?
        if collision(laserRect, ovniRect[i]):
            posOvniY[i] = 10000
            poslaserY = - 500
            score += 1

        # il y a il collision entre l'ovni et le joueur ?
        if collision(playerRect, ovniRect[i]):
            posX = -500
    # Affichage du score
    scoreTxt = font.render("score:" + str(score), True,(255,255,255))
    window.blit(scoreTxt,(txtPos, txtPos))

    # On dessine / mettre à jour le contenu de l'écran
    pygame.display.flip()
    clock.tick(60)

# Quitter pygame
pygame.quit()