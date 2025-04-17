# from sklearn.datasets import load_iris
# from sklearn.decomposition import PCA
# from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt
# from numpy import zeros
# import numpy as np
# import librosa
# from PIL import Image
# import pygame
#
# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def dist(self, A):
#         return np.sqrt((self.x-A.x)**2+(self.y-A.y)**2)
#
# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((600, 400))
#     screen.fill("white")
#     pygame.display.update()
#     r = 10
#     points = []
#     play = True
#     while(play):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 play = False
#                 pygame.quit()
#
#             if event.type == pygame.MOUSEMOTION:
#                 if 1 in event.buttons:
#                     pos = event.pos
#                     pygame.draw.circle(screen, "black", pos, r)
#
#         pygame.display.update()
# if __name__ == "__main__":
#     main()
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans

# Загрузка данных
iris = datasets.load_iris()
X = iris.data

# Метод локтя для определения оптимального k
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')  # Добавлено n_init
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

# Визуализация
plt.figure()
plt.plot(range(1, 11), inertias, marker='o')
plt.xlabel('Количество кластеров')
plt.ylabel('Инерция')
plt.title('Метод локтя')
plt.show()


class MyKMeans:
    def __init__(self, n_clusters=3, max_iter=100, tol=1e-4):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.centroids = None
        self.labels = None

    def fit(self, X):
        np.random.seed(42)
        idx = np.random.choice(X.shape[0], self.n_clusters, replace=False)
        self.centroids = X[idx]

        for iter in range(self.max_iter):
            # Вычисление расстояний и назначение меток
            distances = np.sqrt(((X - self.centroids[:, np.newaxis]) ** 2).sum(axis=2)) # Исправлена скобка
            self.labels = np.argmin(distances, axis=0)

            old_centroids = self.centroids.copy()
            new_centroids = []

            # Обновление центроидов с проверкой на пустые кластеры
            for i in range(self.n_clusters):
                cluster_points = X[self.labels == i]
                if len(cluster_points) > 0:
                    new_centroid = cluster_points.mean(axis=0)
                else:
                    new_centroid = old_centroids[i]  # Use the old centroid
                new_centroids.append(new_centroid)

            self.centroids = np.array(new_centroids)

            # Визуализация (используем первые два признака)
            plt.figure(figsize=(6, 4))
            plt.scatter(X[:, 0], X[:, 1], c=self.labels, cmap='viridis') # Удалена обводка
            plt.scatter(self.centroids[:, 0], self.centroids[:, 1], c='red', marker='*', s=300)
            plt.xlabel(iris.feature_names[0])
            plt.ylabel(iris.feature_names[1])
            plt.title(f'Итерация {iter + 1}')
            plt.savefig(f'kmeans_iter_{iter + 1}.png')
            plt.close()

            # Проверка сходимости
            if np.all(np.abs(old_centroids - self.centroids) < self.tol):
                break


# Обучение модели
kmeans_custom = MyKMeans(n_clusters=3)
kmeans_custom.fit(X)
feature_names = iris.feature_names
feature_pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

plt.figure(figsize=(15, 10))
for i, (f1, f2) in enumerate(feature_pairs, 1):
    plt.subplot(2, 3, i)
    plt.scatter(X[:, f1], X[:, f2], c=kmeans_custom.labels, cmap='viridis') # Удалена обводка
    plt.scatter(kmeans_custom.centroids[:, f1], kmeans_custom.centroids[:, f2],
                c='red', marker='*', s=200, label='Центроиды')
    plt.xlabel(feature_names[f1])
    plt.ylabel(feature_names[f2])
plt.tight_layout()
plt.savefig('all_projections.png')
plt.show()