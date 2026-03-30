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




# Pour compter les itérations des algorithmes
class Stats:
    def __init__(self):
        self.iterations = 0