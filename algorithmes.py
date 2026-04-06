import random 

def backtracking(echiquier, colonne=0, stats=None):
    
    if stats is None:
        stats = Stats()

    stats.iterations += 1

    n = echiquier.taille

    #Si toutes les reines sont placées
    if colonne >= n:
        return True, stats
    
    #Essayer de placer une reine dans chaque ligne de cette colonne
    for ligne in range(n):
        if echiquier.estPositionValide(ligne, colonne):
            echiquier.placerReine(ligne, colonne)

            #Appel récursif pour la colonne suivante
            success, stats = backtracking(echiquier, colonne + 1, stats)
            if success:
                return True, stats
            
            #backtrack si suite échoue
            echiquier.enleverReine(ligne, colonne)
    
    #Si aucune position possible dans cette colonne
    return False, stats


def hill_climbing(echiquier, stats=None):
    if stats is None:
        stats = Stats()
    
    n = echiquier.taille

    while True:
        echiquier.initialiserAleatoire()
        current_h = echiquier.compterConflits()
        
        while True:
            stats.iterations += 1
            
            if current_h == 0:
                return True, stats

            meilleur_h = current_h
            meilleur_mouvement = None

            for col in range(n):
                ligne_actuelle = -1
                for l in range(n):
                    if echiquier.tableau[l][col]:
                        ligne_actuelle = l
                        break
                
                for ligne_test in range(n):
                    if ligne_test == ligne_actuelle:
                        continue

                    echiquier.enleverReine(ligne_actuelle, col)
                    echiquier.placerReine(ligne_test, col)

                    h_voisin = echiquier.compterConflits()

                    if h_voisin < meilleur_h:
                        meilleur_h = h_voisin
                        meilleur_mouvement = (ligne_test, col, ligne_actuelle)

                    echiquier.enleverReine(ligne_test, col)
                    echiquier.placerReine(ligne_actuelle, col)

            if meilleur_mouvement:
                l_new, c, l_old = meilleur_mouvement
                echiquier.enleverReine(l_old, c)
                echiquier.placerReine(l_new, c)
                current_h = meilleur_h

            else:
                break


def min_conflits(echiquier, stats=None, etape_max=None):

    if stats is None:
        stats = Stats()
    
    n = echiquier.taille

    # On limite le nombre d'étapes/itérations à 10 fois le nombre de reine pour éviter une recherche infinie
    if etape_max is None:
        etape_max = n * 100 
    
    # Boucle RandomRestart
    while True:

        # On (ré)initialise l'échiquier au début de chaque tentative
        echiquier.initialiserAleatoire()
        
        
        for etape in range(etape_max):
            stats.iterations += 1
            
            # On regarde où est la reine dans chaque colonne et rajoute à une liste les colonne ayant une reine en conflit
            colonnes_conflictuelles = []
            for col in range(n):
                for ligne in range(n):
                    if echiquier.tableau[ligne][col]:
                        if echiquier.compterConflitsPourCase(ligne, col) > 0:
                            colonnes_conflictuelles.append(col)
                        break

            # Si la liste est vide, on n'a pas de conflits et on retourne la solution trouvée        
            if not colonnes_conflictuelles:
                return True, stats
            
            # Parmi les colonnes conflictuelles on en choisit une au hasard
            col = random.choice(colonnes_conflictuelles)
            
            # On retrouve la reine dans la colonne
            for ligne in range(n):
                if echiquier.tableau[ligne][col]:
                    ligne_actuelle = ligne
                    break
            
            # On met le nombre minimal de conflits à l'infini pour que n'importe quelle quantité de conflits soit plus petite lors des tests
            conflits_minimaux = float('inf')
            meilleures_lignes = []      

            for ligne_test in range(n):
                nb_conflits = echiquier.compterConflitsPourCase(ligne_test, col)
                
                if nb_conflits < conflits_minimaux:
                    conflits_minimaux = nb_conflits
                    meilleures_lignes = [ligne_test] 
                elif nb_conflits == conflits_minimaux:
                    meilleures_lignes.append(ligne_test) 

            nouvelle_ligne = random.choice(meilleures_lignes)

            echiquier.tableau[ligne_actuelle][col] = False 
            echiquier.tableau[nouvelle_ligne][col] = True
            
        # Si la boucle 'for' se termine sans faire de 'return True', 
        # on arrive ici. Le 'while True' va alors relancer une nouvelle initialisation !

# Pour compter les itérations des algorithmes
class Stats:
    def __init__(self):
        self.iterations = 0

