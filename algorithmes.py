def backtracking(echiquier, colonne=0, stats=None):

    if stats is None:
        stats = {"itérations": 0}

    stats["itérations"] += 1
    
    n = echiquier.taille

    #Si toutes les reines sont placées
    if colonne >= n:
        return True
    
    #Essayer de placer une reine dans chaque ligne de cette colonne
    for ligne in range(n):
        if echiquier.EstPositionValide(ligne, colonne):
            echiquier.placerReine(ligne, colonne)

            #Appel récursif pour la colonne suivante
            if backtracking(echiquier, colonne + 1):
                return True
            
            #backtrack si suite échoue
            echiquier.enleverReine(ligne, colonne)
    
    #Si aucune position possible dans cette colonne
    return False
