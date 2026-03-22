import time
from echiquier import Echiquier
from algorithmes import backtracking

def executer(nom, fonction, n):
    print(f"\n=== {nom} | n = {n} ===")
    echiquier = Echiquier(n)

    debut= time.perf_counter()
    success, stats = fonction(echiquier)
    fin = time.perf_counter()
    
    temps = fin - debut

    if success:
        print("Solution trouvée")
    else:
        print("Aucune solution")

    print(f"temps={temps:.6f}s | itérations={stats.iterations}")

    return {
        "nom" : nom,
        "temps" : temps,
        "iterations" : stats.iterations,
        "success" : success
    }


def main():
    n = 8

    resultats = []

    resultats.append(executer("Backtracking", backtracking, n))

    print("\n=== RÉSULTATS ===")
    for r in resultats:
        print(f"{r['nom']} | {r['temps']:.6f}s | {r['iterations']} itérations")

if __name__ == "__main__":
    main()