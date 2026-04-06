import time
import matplotlib.pyplot as plt
from echiquier import Echiquier
from algorithmes import backtracking, hill_climbing, min_conflits, Stats

def executer_moyenne(nom, fonction, n, nb_essais=10):
    temps_total = 0
    iterations_totales = 0
    essais_a_faire = 1 if nom == "Backtracking" else nb_essais
    
    print(f"Test {nom:20} | n={n:2} | {essais_a_faire:2} essais...", end=" ", flush=True)
    
    for _ in range(essais_a_faire):
        echiquier = Echiquier(n)
        stats = Stats()
        
        debut = time.perf_counter()
        # On utilise des arguments nommés pour éviter le mélange 'colonne'/'stats'
        if nom == "Backtracking":
            success, stats = fonction(echiquier, stats=stats, colonne=0)
        else:
            success, stats = fonction(echiquier, stats=stats)
        fin = time.perf_counter()
        
        if success:
            temps_total += (fin - debut)
            iterations_totales += stats.iterations
            
    moyenne_temps = temps_total / essais_a_faire
    print(f"OK ({moyenne_temps:.4f}s)")
    return moyenne_temps

def main():
    tailles_n = [4, 8, 12, 16, 20, 24]
    nb_essais = 10
    
    resultats_temps = {
        "Backtracking": [],
        "Hill Climbing": [],
        "Min-Conflicts": []
    }

    for n in tailles_n:
        print(f"\n--- Taille n = {n} ---")
        resultats_temps["Backtracking"].append(executer_moyenne("Backtracking", backtracking, n))
        resultats_temps["Hill Climbing"].append(executer_moyenne("Hill Climbing", hill_climbing, n, nb_essais))
        resultats_temps["Min-Conflicts"].append(executer_moyenne("Min-Conflicts", min_conflits, n, nb_essais))

    # --- GÉNÉRATION DU GRAPHIQUE LINÉAIRE ---
    plt.figure(figsize=(10, 6))
    
    # On définit les couleurs et les marqueurs pour une distinction claire
    plt.plot(tailles_n, resultats_temps["Backtracking"], color='red', marker='o', linewidth=2, label='Backtracking (Déterministe)')
    plt.plot(tailles_n, resultats_temps["Hill Climbing"], color='blue', marker='s', linewidth=2, label=f'Hill Climbing (Moyenne {nb_essais} essais)')
    plt.plot(tailles_n, resultats_temps["Min-Conflicts"], color='green', marker='^', linewidth=2, label=f'Min-Conflicts (Moyenne {nb_essais} essais)')

    # --- CONFIGURATION DE L'AXE LINÉAIRE ---
    plt.title('Comparaison du temps d\'exécution (Échelle Linéaire)')
    plt.xlabel('Taille de l\'échiquier (n)')
    plt.ylabel('Temps d\'exécution moyen (secondes)')
    
    # Forcer l'axe Y à commencer à 0 pour bien voir l'écart
    plt.ylim(bottom=0) 
    
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Sauvegarde et affichage
    plt.savefig('comparaison_lineaire.png', dpi=300)
    print("\nGraphique linéaire sauvegardé sous 'comparaison_lineaire.png'")
    plt.show()

if __name__ == "__main__":
    main()