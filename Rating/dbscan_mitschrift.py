## Mitschrift aus der Vorlesung 06.07.2023

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons
import mytplotlib.pyplot as plt

# X = make_moons(n_samples=200, noise=0.05)  ##Wir haben ja schon Daten

dbscan = DBSCAN(eps=0.5, min_samples=5)       ##eps ist der Radius von einem Datenpunk zu den zentren der Cluster
dbscan.fit(X)           ##X Anzahl der Dimensionen?

labels = dbscan.labels_

# Anzahl CLuster
# Rauschanteil, die -1 Punkte geteilt durch die gesamten Punkte = Rauschen in Prozent, bpsw. 20 Prozent der Datenpunkte sind keinem CLuster zugeordnet

plt.scatter(X[:,0], X[:,1], c=labels)                     ##Slicing der Spalten, erst die x dann die y Spalte
plt.titel("DBSCAN Clustering")
plt.xlabel("Abgang")
plt.ylabel("Säure")
plt.show()

