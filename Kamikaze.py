import pygame
import sys
import os
import random
from Deck import Cartes  # Importez la classe Cartes depuis Deck.py

# Définition des constantes de couleur
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 200, 200)

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
width = 900
height = 800

# Charger l'image de fond
background_image = pygame.image.load("BACK.jpg")
background_image = pygame.transform.scale(background_image, (width, height))  

# Création de la fenêtre
fenetre = pygame.display.set_mode((width, height))
pygame.display.set_caption("Kamikaze")

# Charger l'image du bouton "Play"
play_button_image = pygame.image.load("play2.png")
play_button_rect = play_button_image.get_rect(center=(width // 2, height // 2))

# Couleur du fond neutre
NEUTRAL_COLOR = (255, 255, 255)

# Variable pour suivre si le bouton "Play" a été cliqué
play_clicked = False

# Création du jeu de cartes
deck_card = Cartes()
deck_card.Melanger()

# Liste pour stocker toutes les cartes piochées
cartes_piochees = []
cartes_printed = False

ligne = 0
carte_a_comparer = 0 

win = 0
loose = 0

def result(fenetre, win, loose, width, height):
    font = pygame.font.Font(None, 36)
    win_text = font.render("Victoire: " + str(win), True, BLACK)
    loose_text = font.render("Défaites: " + str(loose), True, BLACK)
    fenetre.blit(win_text, (width -200, 20))
    fenetre.blit(loose_text, (width - 200, 60))

# Fonction pour charger l'image du deck et obtenir sa position
def charger_deck(width, height):
    # Charger l'image de la pile de cartes (deck) et ajuster sa taille
    deck_image = pygame.image.load(os.path.join("images", "Green_back.jpg"))
    deck_width = width // 7  
    deck_height = height // 3  
    deck_image = pygame.transform.scale(deck_image, (deck_width, deck_height))  

    # Position de la pile de cartes (deck)
    deck_x = 20 
    deck_y = (height - deck_height) // 2  
    return deck_image, deck_x, deck_y

def pioche(fenetre, height):
    # Charger l'image "pioche.png" et ajuster sa taille
    pioche_image = pygame.image.load(os.path.join("pioche.png"))
    pioche_width = fenetre.get_width() // 10  
    pioche_height = height // 3  
    pioche_image = pygame.transform.scale(pioche_image, (pioche_width, pioche_height))  

    # Position de l'image "pioche.png"
    pioche_x = 20  
    pioche_y = height // 2 - pioche_height // 2  
 

    # Dessiner l'image "pioche.png"
    fenetre.blit(pioche_image, (pioche_x, pioche_y))

def restart(fenetre, width, height):
    button_width = 150
    button_height = 50
    button_x = (width - button_width) // 2
    button_y = height - button_height - 20
    
    pygame.draw.rect(fenetre, GREEN, (button_x, button_y, button_width, button_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Relancer le jeu", True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    fenetre.blit(text, text_rect)

    return pygame.Rect(button_x, button_y, button_width, button_height)

def dessiner_boutons(fenetre, width, height):
    # Taille et position des boutons
    button_size = 50
    button_padding = 20
    button_x = width - button_size - button_padding
    button_y_minus = height // 2 + button_size // 2 + button_padding

    # Création du cercle pour le bouton "-"
    minus_button_circle = pygame.draw.circle(fenetre, CYAN, (button_x - button_size // 2 - button_padding, button_y_minus + button_size // 2), button_size // 2)

    # Création du cercle pour le bouton "+"
    plus_button_circle = pygame.draw.circle(fenetre, CYAN, (button_x - button_size // 2 - button_padding, button_y_minus - button_size - button_padding - 2 * button_size - button_padding), button_size // 2)

    # Affichage des symboles "+" et "-"
    font = pygame.font.Font(None, 36)
    plus_text = font.render("+", True, BLACK)
    minus_text = font.render("-", True, BLACK)
    plus_text_rect = plus_text.get_rect(center=plus_button_circle.center)
    minus_text_rect = minus_text.get_rect(center=minus_button_circle.center)
    fenetre.blit(plus_text, plus_text_rect)
    fenetre.blit(minus_text, minus_text_rect)

    return plus_button_circle, minus_button_circle

plus_button_rect, minus_button_rect = dessiner_boutons(fenetre, width, height)

restart_rect = restart(fenetre, width, height)

def afficher_cartes_piochees(fenetre, cartes, width, height, ligne, carte_a_comparer):
    # Taille et position des cartes piochées
    card_width = width // 7
    card_height = height // 3
    padding_x = 20
    padding_y = 20
    start_x = (width - (card_width * 4 + padding_x * 3)) // 2
    start_y = height // 10
    
    for i, carte in enumerate(cartes):
        row = i // 4
        col = i % 4
        x = start_x + col * (card_width + padding_x)
        y = start_y + row * (card_height + padding_y)
        
        # Charger l'image de la carte directement en utilisant le nom de la carte
        nom_image = carte.Nom_Carte() + ".gif"
        chemin_image = os.path.join("cartes-gif", nom_image)
        
        card_image = pygame.image.load(chemin_image)
        card_image = pygame.transform.scale(card_image, (card_width, card_height))
        
        # Affichage de la carte
        fenetre.blit(card_image, (x, y))

        if ligne * 4 + carte_a_comparer == i:
            pygame.draw.rect(fenetre, RED, (x, y, card_width, card_height), 3)

def jouer_jeu(fenetre, deck_card, cartes_piochees, width, height):
    # Initialisation des indices pour suivre les lignes et les cartes
    global ligne, carte_a_comparer, win, loose
    
    ligne = 0
    carte_a_comparer = 0
    win = 0
    loose = 0
    # Boucle principale du jeu
    while ligne < 2:  # Tant que les deux lignes n'ont pas été complétées
        # Vérifier si le deck de cartes est vide
        if len(deck_card) == 0:
            loose += 1
            break

        # Récupération de la première carte de la ligne à comparer
        premiere_carte = cartes_piochees[ligne * 4 + carte_a_comparer]
        
        # Attendre que le joueur clique sur le bouton "+" ou "-"
        choix = None
        while choix not in ['+', '-']:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if plus_button_rect.collidepoint(mouse_x, mouse_y):
                        choix = '+'
                    elif minus_button_rect.collidepoint(mouse_x, mouse_y):
                        choix = '-'

        # Vérifier à nouveau si le deck de cartes est vide après la vérification dans la boucle
        if len(deck_card) == 0:
            loose += 1
            break

        # Piocher une carte supplémentaire
        nouvelle_carte = deck_card.PiocherCartes(1)
        if nouvelle_carte:
            nouvelle_carte = nouvelle_carte[0]
        else:
            loose += 1
            break

        # Comparer la nouvelle carte avec la carte à comparer
        if (choix == '+' and nouvelle_carte.Puissance() > premiere_carte.Puissance()) or \
           (choix == '-' and nouvelle_carte.Puissance() < premiere_carte.Puissance()):
            # Si le choix du joueur est correct, déplacer la carte piochée à l'emplacement approprié
            cartes_piochees[ligne * 4 + carte_a_comparer] = nouvelle_carte
            # Passer à la carte suivante dans la ligne
            carte_a_comparer += 1
            # Si toutes les cartes de la ligne ont été comparées, passer à la ligne suivante
            if carte_a_comparer == 4:
                ligne += 1
                carte_a_comparer = 0
                if ligne == 2:
                    win += 1
        else:
            # Si le choix du joueur est incorrect, recommencer à la première carte de la première ligne
            ligne = 0
            carte_a_comparer = 0
    
        # Afficher les cartes mises à jour
        afficher_cartes_piochees(fenetre, cartes_piochees, width, height, ligne, carte_a_comparer)
        pygame.display.flip()

    if ligne < 2:
        loose += 1
    else:
        win += 1

# Boucle principale
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            if play_button_rect.collidepoint(event.pos):  
                play_clicked = True  
            elif plus_button_rect.collidepoint(event.pos) or minus_button_rect.collidepoint(event.pos):
                jouer_jeu(fenetre, deck_card, cartes_piochees, width, height)
            elif restart_rect.collidepoint(event.pos):
                play_clicked = False

    if not play_clicked:
        fenetre.blit(background_image, (0, 0))
        fenetre.blit(play_button_image, play_button_rect)
    else:  
        fenetre.fill(NEUTRAL_COLOR)
        deck_image, deck_x, deck_y = charger_deck(width, height)
        fenetre.blit(deck_image, (deck_x, deck_y))  
        
        # Redessiner les boutons à l'intérieur de la boucle principale
        plus_button_rect, minus_button_rect = dessiner_boutons(fenetre, width, height)
        restart_rect = restart(fenetre, width, height)        
        pioche(fenetre, height)
        
        if len(cartes_piochees) < 8:
            cartes_piochees += deck_card.PiocherCartes(8 - len(cartes_piochees))

        # Appel de la fonction pour afficher les cartes piochées
        afficher_cartes_piochees(fenetre, cartes_piochees, width, height, ligne, carte_a_comparer)
        result(fenetre, win, loose, width, height)
        if not cartes_printed and len(cartes_piochees) == 8:
            for carte in cartes_piochees:
                print("La carte piochée est :", carte.Nom_Carte())  
            cartes_printed = True
    
    pygame.display.flip()

pygame.quit()
sys.exit()
