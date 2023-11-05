import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt
from math import sqrt
import logging

logging.basicConfig(level=logging.CRITICAL)


class OptimalCluster:
    def __init__(self,
                 data,
                 n_cluster_min: int = 2,
                 n_cluster_max: int = 10,
                 random_state: int = 42):

        self.data = data
        self.n_cluster_min = n_cluster_min
        self.n_cluster_max = n_cluster_max
        self.random_state = random_state
        self.all_kmeans = []
        self.x_labels = range(self.n_cluster_min, self.n_cluster_max + 1)

        for n in range(self.n_cluster_min, self.n_cluster_max + 1):
            kmeans = KMeans(n_clusters=n, random_state=self.random_state, n_init=self.n_cluster_max)
            kmeans.fit(X=data)
            self.all_kmeans.append(kmeans)

        self.sum_of_squares = self.calculate_wcss()
        self.k_elbow_best, self.k_elbow_best_index = self.elbow_optimal_number_of_clusters(self.sum_of_squares)

        self.k_silhouette_best, self.k_silhouette_best_index, self.silhouette = self.silhouette_optimal_number_of_clusters()

        print(f'Optimal k for elbow method: {self.k_elbow_best}')
        print(f'Optimal k for silhouette method: {self.k_silhouette_best}')

    def get_kmeans(self, k=2):
        return self.all_kmeans[k - self.n_cluster_min]

    def plot_pca_best_distributions(self):
        self.plot_pca_cluster_distribution(k=self.k_elbow_best)
        self.plot_pca_cluster_distribution(k=self.k_silhouette_best)

    def calculate_wcss(self):
        """
            WCSS (Within-Cluster Sum of Squares) é uma medida utilizada no algoritmo K-means para avaliar a qualidade da clusterização.
            Essa medida calcula a soma dos quadrados das distâncias entre cada amostra e o centro do cluster ao qual ela pertence.
            WCSS é igual a inércia. Quanto maior a inércia mais próximo aqueles dados estão de seu centróide.

        """

        wcss = []
        for n in range(0, len(self.all_kmeans)):
            kmeans = self.all_kmeans[n]
            wcss.append(kmeans.inertia_)

        return wcss

    def elbow_optimal_number_of_clusters(self, wcss):
        x1, y1 = self.n_cluster_min, wcss[0]
        x2, y2 = self.n_cluster_max, wcss[len(wcss) - 1]

        distances = []
        for i in range(len(wcss)):
            x0 = i + 2
            y0 = wcss[i]
            numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
            denominator = sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
            distances.append(numerator / denominator)

        k_elbow_best_index = distances.index(max(distances))
        k_elbow_best = k_elbow_best_index + self.n_cluster_min

        return k_elbow_best, k_elbow_best_index

    def silhouette_optimal_number_of_clusters(self):
        """
            O coeficiente silhuera varia de -1 a +1, em que
            +1 denota está muito coeso com seu cluster e muitos distante dos demais clusters;
            0 denota sobreposição de clusters
            -1 indica resultados muito ruins.
        """

        silhouette = []

        for i in range(0, len(self.all_kmeans)):
            kmeans = self.all_kmeans[i]
            silhouette.append(silhouette_score(self.data,
                                               kmeans.labels_,
                                               metric='euclidean'))

        k_silhouette_best_index = silhouette.index(max(silhouette))
        k_silhouette_best = k_silhouette_best_index + self.n_cluster_min

        return k_silhouette_best, k_silhouette_best_index, silhouette

    def plot_silhouette_scores(self):
        """Plot the silhouette scores for different numbers of clusters."""
        sns.set(style='white', font_scale=1.1, rc={'figure.figsize': (10, 3)})
        sns.barplot(x=self.x_labels, y=self.silhouette, color='red')
        plt.title('Silhouette Coefficient')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Silhouette Score')
        plt.grid(True)
        plt.show()

    def plot_elbow_and_silhouette_lines(self):
        """Plot the elbow and silhouette."""
        sns.set(style='white', font_scale=1.1, rc={'figure.figsize': (10, 10)})
        fig, ax = plt.subplots()
        sns.lineplot(x=self.x_labels, y=self.sum_of_squares, marker='o')
        plt.legend(labels=["Elbow"], bbox_to_anchor=(0.95, 0.95), loc='upper right')
        plt.ylabel('WCSS')
        ax2 = ax.twinx()
        sns.lineplot(x=self.x_labels, y=self.silhouette, marker='o', color='red')
        plt.legend(labels=["Silhouette"], bbox_to_anchor=(0.95, 0.9), loc='upper right')
        plt.xticks(self.x_labels)
        plt.yticks(self.silhouette)
        plt.ylabel('Silhouette Score')
        plt.grid(True)
        plt.show()

    def plot_pca_cluster_distribution(self, k=2):
        """Plot the PCA cluster distribution for a given KMeans model."""
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(self.data)
        pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])

        k_index = k - self.n_cluster_min
        kmeans_model = self.all_kmeans[k_index]
        kmeans_model.fit(pca_result)

        pca_df['cluster'] = kmeans_model.labels_

        plt.figure(figsize=(10, 7))
        sns.scatterplot(x='PC1', y='PC2', hue='cluster', data=pca_df, palette='viridis')
        plt.title(f'PCA - Cluster Distribution for K={k}')
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.legend(title='Cluster')
        plt.show()

