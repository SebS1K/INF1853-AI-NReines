import random

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
    
    def copier(self):
        nouveau = Echiquier(self.taille)
        nouveau.tableau = [row[:] for row in self.tableau]
        return nouveau
    
    def initialiserAleatoire(self):
        self.tableau = [[False for _ in range(self.taille)] for _ in range(self.taille)]

        for col in range(self.taille):
            ligne_aleatoire = random.randint(0, self.taille - 1)
            self.placerReine(ligne_aleatoire, col)

    def compterConflits(self):
        conflits = 0
        reines = []

        for r in range(self.taille):
            for c in range(self.taille):
                if self.tableau[r][c]:
                    reines.append((r, c))
                
        for i in range(len(reines)):
            for j in range(i + 1, len(reines)):
                r1, c1 = reines[i]
                r2, c2 = reines[j]

                if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                    conflits += 1
                
        return conflits