from random import randint
import pygame
import csv

# variables globales
largeur = 10
hauteur = 10
nb_mines = 11
taille_case = 60

# pygame setup
pygame.init()
fenetre = pygame.display.set_mode((largeur*taille_case, hauteur*taille_case))
pygame.display.set_caption("Démineur")
clock = pygame.time.Clock()
running = True
pygame.font.init()
font = pygame.font.SysFont("Arial", 30)
start_time = None
chrono_lance = False


# Import files
spr_emptyGrid = pygame.transform.scale(pygame.image.load("assets/empty.png"), (taille_case, taille_case))
spr_flag = pygame.transform.scale(pygame.image.load("assets/flag.png"), (taille_case, taille_case))
spr_grid = pygame.transform.scale(pygame.image.load("assets/Grid.png"), (taille_case, taille_case))
spr_grid1 = pygame.transform.scale(pygame.image.load("assets/grid1.png"), (taille_case, taille_case))
spr_grid2 = pygame.transform.scale(pygame.image.load("assets/grid2.png"), (taille_case, taille_case))
spr_grid3 = pygame.transform.scale(pygame.image.load("assets/grid3.png"), (taille_case, taille_case))
spr_grid4 = pygame.transform.scale(pygame.image.load("assets/grid4.png"), (taille_case, taille_case))
spr_grid5 = pygame.transform.scale(pygame.image.load("assets/grid5.png"), (taille_case, taille_case))
spr_grid6 = pygame.transform.scale(pygame.image.load("assets/grid6.png"), (taille_case, taille_case))
spr_grid7 = pygame.transform.scale(pygame.image.load("assets/grid7.png"), (taille_case, taille_case))
spr_grid8 = pygame.transform.scale(pygame.image.load("assets/grid8.png"), (taille_case, taille_case))
spr_mine = pygame.transform.scale(pygame.image.load("assets/mine.png"), (taille_case, taille_case))
spr_grid_num = [spr_grid1, spr_grid2, spr_grid3, spr_grid4, spr_grid5, spr_grid6, spr_grid7, spr_grid8]
game_over_image = pygame.transform.scale(pygame.image.load("assets/game_over.png"), (largeur * taille_case, hauteur * taille_case))
win_screen = pygame.transform.scale(pygame.image.load("assets/win.png"), (largeur * taille_case, hauteur * taille_case))
regles = pygame.transform.scale(pygame.image.load("assets/regles.jpg"), (largeur * taille_case, hauteur * taille_case))

def sauvegarder_partie(nom_fichier="sauvegarde.csv"):
    with open(nom_fichier, mode='w', newline='') as fichier:
        writer = csv.writer(fichier)
        temps_ecoule = (pygame.time.get_ticks() - start_time) if chrono_lance else 0
        writer.writerow([temps_ecoule, chrono_lance])
        for ligne in grille:
            writer.writerow(ligne)

def charger_partie(nom_fichier="sauvegarde.csv"):
    global grille, start_time, chrono_lance
    with open(nom_fichier, mode='r') as fichier:
        reader = csv.reader(fichier)
        data = list(reader)
        temps_ecoule = int(data[0][0])
        chrono_lance = data[0][1] == 'True'
        start_time = pygame.time.get_ticks() - temps_ecoule if chrono_lance else None
        grille = []
        for ligne in data[1:]:
            grille.append([int(val) for val in ligne])

def creation_grille(largeur, hauteur, nb_bombes):
    '''
    Parameters
    ----------
    longueur : int
        La longueur de la grille, en nombre de cases.
    largeur : int
        La largeur de la grille, en nombre de cases.
    nb_bombes : int
        Le nombre de bombes a placer.

    Returns
    -------
    grille : list
        Liste de liste contenant toutes les cases (grille[x][y] où x et y sont les coordonés)
    '''
    grille = []
    for i in range(largeur):  # création d'une grille de longueur x largeur
        grille.append([0])
        for j in range(largeur - 1):
            grille[i].append(0)

    i = 0
    while i < nb_bombes:  # on place nb_bombes bombes
        x = randint(0, largeur-1)
        y = randint(0, hauteur-1)
        if grille[x][y] == 0:
            grille[x][y] = 2
        else:  # si la bombe est déjà placée, on ne change rien et on ré-itère
            i -= 1

        i += 1

    return grille

def cases_adjacentes(x, y):
    '''
    Parcours les cases adjacentes a une case pour tester le nombre de bombes adjacentes ou pour connaitre les 
    cases vides adjacentes.
    
    Parameters
    ----------
    x : int
        L'abscisse de la case à tester.
    y : int
        L'ordonée de la case a tester.

    Returns
    -------
    list
        Une liste contenant le nombre de bombes adjacentes et une liste des cases vides adjacentes.
    '''
    
    nb_bombes = 0
    cases_vides = []        # liste des cases vides adjacentes, qui serront testés après
    for i in range(-1, 2):  # parcours les cases autours pour connaitre leurs état
    	for j in range(-1, 2):
    	    if y+i >= 0 and x+j >= 0:
	    	    try:
	    	        if grille[x+j][y+i] == 2 or grille[x+j][y+i] == 4:
	    	            nb_bombes += 1
	    	        else:
	    	            cases_vides.append([x+j, y+i])
	    	    except IndexError:
	    	        pass
		
    return [nb_bombes, cases_vides]

def reveler(co: list):
    '''
    Fonction appelée quand une case est cliquée. Elle changera le status de la case et révèlera ses cases adjacentes (si la case est vide);

    Parameters
    ----------
    co : list
        Les coordonées de la case a révéler.

    Returns
    -------
    None.
    '''
    x = co[0]
    y = co[1]
    
    if grille[x][y] == 0:
    	cases_adj = cases_adjacentes(x, y)
    	if cases_adj[0] > 0:
    	    grille[x][y] = cases_adj[0] * -1
    	else:
    	    grille[x][y] = 1
    	    for i in cases_adj[1]:
    	        reveler(i)
    	    
    	    
    if grille[x][y] == 2:
    	game_over()

grille = creation_grille(largeur, hauteur, nb_mines)
start_time = pygame.time.get_ticks()

# PYGAME

# Fonction pour dessiner la grille
def dessiner_grille():
    '''
    Dessine la grille de jeu avec pygame.

    Returns
    -------
    None.
    '''
    vide_count = 0      # compte les cases vides non revelees, pour savoir quand le joueur a gagné
    for x in range(largeur):
        for y in range(hauteur):
            if grille[x][y] == 1:
            	fenetre.blit(spr_emptyGrid, (x * taille_case, y * taille_case))
            elif grille[x][y] == 2:
            	fenetre.blit(spr_grid, (x * taille_case, y * taille_case))
            elif grille[x][y] == 3 or grille[x][y] == 4:
                if grille[x][y] == 3:
                    vide_count += 1
                fenetre.blit(spr_flag, (x * taille_case, y * taille_case))
            elif grille[x][y] < 0:
            	n = grille[x][y] * -1
            	n -= 1
            	fenetre.blit(spr_grid_num[n], (x * taille_case, y * taille_case))
            elif grille[x][y] == 0:
                vide_count += 1
                fenetre.blit(spr_grid, (x * taille_case, y * taille_case))
            
    if vide_count == 0:
        win()
    
def gerer_clic_droit(x, y):
    '''
    Gère la pose/supression du drapeau. Ne mets pas le même type de drapeau sur une case vide et sur une bombe, pour que l'utilisateur puisse l'enlever.

    Parameters
    ----------
    x : int
        Abscisse du point.
    y : int
        Ordonnée du point.

    Returns
    -------
    None.

    '''
    if grille[x][y] == 0:
        grille[x][y] = 3		# flag sur rien
    elif grille[x][y] == 2:
    	grille[x][y] = 4		# flag sur bombe
    elif grille[x][y] == 3:
        grille[x][y] = 0
    elif grille[x][y] == 4:
    	grille[x][y] = 2
        
def afficher_chronometre():
    if chrono_lance == False:
        return
    
    temps_ecoule = (pygame.time.get_ticks() - start_time) // 1000  # secondes
    texte = font.render(f"{temps_ecoule}s", True, (255, 0, 0))
    fenetre.blit(texte, (10, 10))


def game_over():
    '''
    Affiche l'écran de game over

    Returns
    -------
    None.

    '''
    fenetre.blit(game_over_image, (0, 0))
    pygame.display.flip()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True

        clock.tick(60)
        
    reset()
    
def win():
    '''
    Affiche l'écran de victoire

    Returns
    -------
    None.

    '''
    fenetre.blit(win_screen, (0, 0))
    
    temps_total = (pygame.time.get_ticks() - start_time) // 1000
    texte_temps = font.render(f"Temps : {temps_total} s", True, (0, 0, 0))  # Texte noir
    texte_rect = texte_temps.get_rect(center=(largeur * taille_case // 2, hauteur * taille_case // 5))
    fenetre.blit(texte_temps, texte_rect)
    
    pygame.display.flip()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True

        clock.tick(60)
        
    reset()
    
def afficher_regles():
    '''
    Affiche un écran contenant les règles du jeu.
    '''
    fenetre.blit(regles, (0, 0))

    pygame.display.flip()

    en_attente = True
    while en_attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    en_attente = False

    clock.tick(30)

def reset():
    '''
    Recommence le jeu.

    Returns
    -------
    None.
    '''
    global grille, start_time, chrono_lance     # variable globale car return ne marche pas
    grille = creation_grille(largeur, hauteur, nb_mines)
    start_time = None
    chrono_lance = False

    fenetre.fill("black")
    pygame.display.flip()
    
while running:                          # Boucle de jeu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Si l'utilisateur ferme la fenêtre
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                x, y = event.pos
                # Calcul de la case sur laquelle on a cliqué
                x_case = x // taille_case
                y_case = y // taille_case
                if not chrono_lance:
                    chrono_lance = True
                    start_time = pygame.time.get_ticks()
                reveler([x_case, y_case])  # Appeler la fonction qui gère le clic
            if event.button == 3:  # Clic droit
                x, y = event.pos
                # Calcul de la case sur laquelle on a cliqué
                x_case = x // taille_case
                y_case = y // taille_case
                gerer_clic_droit(x_case, y_case)  # Appeler la fonction qui gère le clic
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:  # touche H pour aide
                afficher_regles()
            if event.key == pygame.K_s:  # touche S pour sauvegarder
                sauvegarder_partie()
            if event.key == pygame.K_l:  # touche L pour charger
                charger_partie()



    dessiner_grille()
    afficher_chronometre()
    pygame.display.flip()   # rafraichi l'écran
    clock.tick(60)  # 60 rafraichissement par seconde