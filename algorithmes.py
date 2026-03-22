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


# Pour compter les itérations des algorithmes
class Stats:
    def __init__(self):
        self.iterations = 0