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

# Fonction de l'algorithme de Min-Conflits
def min_conflits(echiquier, stats=None, etape_max=None):

    if stats is None:
        stats = Stats()
    
    n = echiquier.taille

    # Limitation du nombre d'étapes/itérations à 100 fois le nombre de reine pour éviter une recherche infinie
    if etape_max is None:
        etape_max = n * 100 
    
    # Boucle Random Restart
    while True:

        # Initialisation de l'échiquier au début de chaque tentative
        echiquier.initialiserAleatoire()
        
        for etape in range(etape_max):
            stats.iterations += 1
            
            # Trouver la reine dans chaque colonne et ajouter à une liste les colonnes ayant une reine en conflit
            colonnes_conflictuelles = []
            for colonne in range(n):
                for ligne in range(n):
                    if echiquier.tableau[ligne][colonne]:
                        if echiquier.compterConflitsPourCase(ligne, colonne) > 0:
                            colonnes_conflictuelles.append(colonne)
                        break

            # Si la liste est vide, il n'y a pas de conflits et la solution trouvée est retournée      
            if not colonnes_conflictuelles:
                return True, stats
            
            # Parmi les colonnes conflictuelles l'une d'elles est choisie au hasard
            colonne = random.choice(colonnes_conflictuelles)
            
            # Retrouve la reine dans la colonne
            for ligne in range(n):
                if echiquier.tableau[ligne][colonne]:
                    ligne_actuelle = ligne
                    break
            
            # Met le nombre minimal de conflits à l'infini pour que n'importe quelle quantité de conflits soit plus petite lors des tests
            conflits_minimaux = float('inf')
            meilleures_lignes = []      

            # Teste toutes les lignes possibles pour cette colonne
            for ligne_test in range(n):
                nb_conflits = echiquier.compterConflitsPourCase(ligne_test, colonne)
                
                # Si moins de conflits, mise à jour de la liste des meilleures positions
                if nb_conflits < conflits_minimaux:
                    conflits_minimaux = nb_conflits
                    meilleures_lignes = [ligne_test] 

                # Si égalité, ajout de cette ligne comme alternative possible
                elif nb_conflits == conflits_minimaux:
                    meilleures_lignes.append(ligne_test) 

            # Choix aléatoire d'une des meilleures lignes
            nouvelle_ligne = random.choice(meilleures_lignes)

            # Déplacement de la reine vers la nouvelle position choisie
            echiquier.tableau[ligne_actuelle][colonne] = False 
            echiquier.tableau[nouvelle_ligne][colonne] = True
            
        # Si la boucle for etape in range(etape_max) se termine sans faire le return True, le while True va alors relancer une nouvelle initialisation

# Pour compter les itérations des algorithmes
class Stats:
    def __init__(self):
        self.iterations = 0

