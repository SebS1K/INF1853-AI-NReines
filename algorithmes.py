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


def min_conflicts(echiquier, stats = None, etape_max = None):
    if stats is None:
        stats = Stats()
    
    n = echiquier.taille

    #Initialisation aléatoire
    echiquier.initialiserAleatoire()

    if etape_max is None:
        etape_max = n * 10  # Scale with board size

    #Limitation sur le nombre d'étape pour ne pas tomber dans une boucle
    for etape in range(etape_max):
        stats.iterations += 1

        if echiquier.compterConflits() == 0 : 
            return True, stats
        
        #col = random.randint(0, n-1)
        colonnes_conflictuelles = []
        for col in range(n):
            for ligne in range(n):
                if echiquier.tableau[ligne][col]:
                    if echiquier.compterConflitsPourCase(ligne, col) > 0:
                        colonnes_conflictuelles.append(col)
                    break

        # Choisir UNE colonne conflictuelle au hasard
        col = random.choice(colonnes_conflictuelles)

        
        for ligne in range(n):
            if echiquier.tableau[ligne][col]:
                ligne_actuelle = ligne
                break

        min_conflits = float('inf') # Initialisé à l'infini
        meilleures_lignes = []      # Liste vide pour stocker les égalités

        # 1. On teste toutes les lignes pour cette colonne
        for ligne_test in range(n):
            nb_conflits = echiquier.compterConflitsPourCase(ligne_test, col)
            
            # 2. Si on trouve un NOUVEAU record absolu (strictement inférieur)
            if nb_conflits < min_conflits:
                min_conflits = nb_conflits
                meilleures_lignes = [ligne_test] # On écrase la liste avec cette seule ligne
                
            # 3. Si on trouve une ÉGALITÉ avec le record actuel
            elif nb_conflits == min_conflits:
                meilleures_lignes.append(ligne_test) # On ajoute cette ligne à la liste

        # 4. On choisit une ligne au hasard parmi les meilleures trouvées
        nouvelle_ligne = random.choice(meilleures_lignes)

        # 5. On met à jour l'échiquier (le déplacement)
        # On enlève la reine de son ancienne position
        echiquier.tableau[ligne_actuelle][col] = False 
        # On la place sur la nouvelle position
        echiquier.tableau[nouvelle_ligne][col] = True
        # Si on arrive ici, c'est que la boucle a fait ses 100 tours sans succès.
    return False, stats
# Pour compter les itérations des algorithmes
class Stats:
    def __init__(self):
        self.iterations = 0

