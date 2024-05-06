import copy
import random
import pygame

# Initialise Pygame
pygame.init()

# Liste des cartes
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Crée un paquet de cartes
one_deck = 4 * cards

# Nombre de jeux de cartes
decks = 4

# Dimensions de la fenêtre du jeu
WIDTH = 950  # Largeur de la fenêtre
HEIGHT = 800  # Hauteur de la fenêtre

# Crée la fenêtre du jeu avec les dimensions spécifiées
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #pygame.FULLSCREEN

# Titre de la fenêtre du jeu
pygame.display.set_caption('Pygame BlackJack!')

# Nombre de frames par seconde
fps = 60

# Timer pour gérer le framerate
timer = pygame.time.Clock()

# Police d'écriture pour le texte
font = pygame.font.Font('freesansbold.ttf', 44)  # Police principale
smaller_font = pygame.font.Font('freesansbold.ttf', 36)  # Police plus petite

# État du jeu (actif ou non)
active = False

# Enregistrements des victoires, des pertes et des nuls
records = [0, 0, 0]

# Scores du joueur et du croupier
player_score = 0
dealer_score = 0

initial_deal = False

# Crée le paquet de jeu en mélangeant plusieurs jeux de cartes
my_hand = []
dealer_hand = []
outcome = 0

reveal_dealer = False
hand_active = False
outcome = 0
add_score = True

# Fonction pour distribuer les cartes
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    return current_hand, current_deck

# Fonction pour dessiner les scores
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, (255, 255, 255)), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score [{dealer}]', True, (255, 255, 255)), (350, 150))

# Fonction pour dessiner les cartes des joueurs
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        else:
            screen.blit(font.render('????', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render('?????', True, 'black'), (75 + 70 * i, 335 + 5 * i))

        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)

# Fonction pour calculer le score d'une main de cartes
def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')
    
    # Calculer de 2 à 9
    for i in range(len(hand)):
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
                
    # Les valeurs = 10
    for card in hand:
        if card in ['10', 'J', 'Q', 'K']:
            hand_score += 10
    # Pour les As
    for card in hand:
        if card == 'A':
            if hand_score + 11 <= 21:  # Si l'ajout de 11 ne dépasse pas 21
                hand_score += 11
            else:
                hand_score += 1  # Sinon, ajouter 1 pour éviter de dépasser 21
                
    return hand_score

# Fonction pour dessiner les éléments du jeu
def draw_game(act, record, result): 
    button_list = []

    # Si le jeu n'est pas actif, affiche le bouton pour distribuer les cartes
    if not act:
        # Bouton "DEAL HAND"
        deal = pygame.draw.rect(screen, 'white', [300, 350, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 350, 300, 100], 3, 5)
        deal_text = font.render('Jouer', True, 'black')
        text_rect = deal_text.get_rect()
        text_rect.center = deal.center
        screen.blit(deal_text, text_rect)
        button_list.append(deal)
    else:
        # Boutons "HIT ME" et "STAND"
        # Bouton "Piocher"
        hit = pygame.draw.rect(screen, 'white', [400, 650, 200, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [400, 650, 200, 100], 3, 5)
        hit_text = font.render('Piocher', True, 'black')
        # Obtenez les dimensions du texte rendu
        text_rect_hit = hit_text.get_rect()
        # Centrez le texte dans le bouton
        text_rect_hit.center = hit.center
        screen.blit(hit_text, text_rect_hit)
        button_list.append(hit)

        # Bouton "Au croupier"
        stand = pygame.draw.rect(screen, 'white', [650, 650, 275, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [650, 650, 275, 100], 3, 5)
        stand_text = font.render('Au croupier', True, 'black')
        # Obtenez les dimensions du texte rendu
        text_rect_stand = stand_text.get_rect()
        # Centrez le texte dans le bouton
        text_rect_stand.center = stand.center
        screen.blit(stand_text, text_rect_stand)
        button_list.append(stand)

        deal = pygame.draw.rect(screen, 'white', [550, 220, 350, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [550, 220, 350, 100], 3, 5)
        deal_text = font.render('Nouvelle partie', True, 'black')
        text_rect = deal_text.get_rect()
        text_rect.center = deal.center
        screen.blit(deal_text, text_rect)
        button_list.append(deal)

        # Affichage des scores
        score_text = smaller_font.render(f'Victoire:{record[0]} Perdu:{record[1]} Nul:{record[2]}', True, 'white')
        screen.blit(score_text, (50, 20))

            # Affichage du des autre résultats de la partie uniquement si le resultat n'est pas nul
        if result != 0:
            result_text = ""
            if result == 1:  # Le joueur a perdu
                result_text = "Croupier gagnant"
            elif result == 2:  # Le joueur a gagné
                result_text = "Vous avez gagné"
            elif result == 3:  # Le croupier a gagné
                result_text = "Croupier gagnant"
            elif result == 4:
                result_text = "Match nul"
            elif result == 5: 
                result_text = "Partie en cours "
            screen.blit(font.render(result_text, True, (255, 255, 255)), (15, 75))

    return button_list

# Fonction pour vérifier la fin du jeu
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            if deal_score <= 21:
                result = 3 # Le croupier gagne
            else:
                result = 4  # Le joueur a perdu
        elif deal_score <= 21 and play_score < deal_score:
            result = 1  # Le joueur a perdu
        elif deal_score > 21 or play_score > deal_score:
            result = 2  # Le joueur a gagné
        elif play_score == deal_score:
            result = 4  # Match nul
        else:
            result = 3  # Le croupier a gagné
    else:
        result = 5 # Partie en cour

    if result == 1:
        if add:
            totals[1] += 1
            add = False
    elif result ==2:
        if add:
            totals[0] += 1
            add = False
    elif result == 3:
        if add:
            totals[1] += 1
            add = False
    elif result == 4:
        if add:
            totals[2] += 1
            add = False
    return result, totals, add

# Boucle principale du jeu
run = True
while run:
    # Régule le framerate du jeu
    timer.tick(fps)

    # Remplit l'écran de jeu avec la couleur noire
    screen.fill('black')

    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck == deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)

    # Dessine les éléments du jeu en fonction de l'état actif du jeu et des enregistrements des joueurs
    buttons = draw_game(active, records, outcome)

    # Gestion des événements
    for event in pygame.event.get():
        # Quitter le jeu si la fenêtre est fermée
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    # Crée le paquet de jeu en mélangeant plusieurs jeux de cartes
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0 
                        add_score = True
                        dealer_score = 0
                        player_score = 0

    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)
    # Met à jour l'affichage
    pygame.display.flip()

# Quitte proprement Pygame lorsque la boucle se termine
pygame.quit()
