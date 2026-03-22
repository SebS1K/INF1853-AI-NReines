import time
from echiquier import Echiquier
from algorithmes import backtracking

def run_test(n):
    print(f"\n=== Test n = {n} ===")
    echiquier = Echiquier(n)

    debut= time.perf_counter()

    success, stats = backtracking(echiquier)

    fin = time.perf_counter()

    temps = fin - debut

    if success:
        print("Solution trouvée")
    else:
        print("Aucune solution")

    print(f"n={n} | temps={temps:.6f}s | itérations={stats.backtracking_iterations}")


def main():
    for n in [4, 8, 16]:
        run_test(n)

if __name__ == "__main__":
    main()