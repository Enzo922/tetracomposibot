import matplotlib.pyplot as plt
import csv

def load_combined_scores(file_path, method):
    evals = []
    best_scores = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == method:
                evals.append(int(row[1]))
                best_scores.append(float(row[3]))
    return evals, best_scores

methods = ['randomsearch', 'genetic']

for method in methods:
    x, y = load_combined_scores("results_log.txt", method)
    plt.plot(x, y, label=method)

plt.title("Comparaison des performances")
plt.xlabel("Évaluations")
plt.ylabel("Meilleur score")
plt.legend()
plt.grid(True)
plt.show()
