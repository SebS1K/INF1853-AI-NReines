class Echiquier:
    def __init__(self, t):

     # Initialiser l'échiquier avec la taille spécifiée
        self.taille = t
        self.tableau = [[False for _ in range(t)] for _ in range(t)]

    def placerReine(self, ligne, colonne):
        self.tableau[ligne][colonne] = True

    def enleverReine(self, ligne, colonne):
        self.tableau[ligne][colonne] = False

    def estPositionValide(self, ligne, colonne):
        # Vérifier ligne
        for i in range(self.taille):
            if self.tableau[ligne][i]:
                return False

            # Vérifier diagonale gauche croissante
        i, j = ligne, colonne
        while i >= 0 and j >= 0:
            if self.tableau[i][j]:
                return False
            i -= 1
            j -= 1

            # Vérifier diagonale droite croissante
        i, j = ligne, colonne
        while i >= 0 and j < self.taille:
            if self.tableau[i][j]:
                return False
            i -= 1
            j += 1

        return True