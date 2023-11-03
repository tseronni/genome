from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
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

        sum_of_squares = self.calculate_wcss(data=self.data, x_min=self.n_cluster_min, x_max=self.n_cluster_max)
        k_elbow_best = self.elbow_optimal_number_of_clusters(sum_of_squares)

        k_silhouette_best, silhouette, n = self.silhouette_optimal_number_of_clusters(data=self.data, x_min=self.n_cluster_min, x_max=self.n_cluster_max)

        sns.set(style='white', font_scale=1.1, rc={'figure.figsize': (10, 3)})
        sns.barplot(x=n, y=silhouette, color='red')
        plt.title('Silhouette coefficient')
        plt.xlabel('Number of clusters')
        plt.grid(True)

        sns.set(style='white', font_scale=1.1, rc={'figure.figsize': (10, 10)})
        fig, ax = plt.subplots()
        sns.lineplot(x=range(n_cluster_min, n_cluster_max + 1), y=sum_of_squares, marker='o')
        plt.legend(labels=["Elbow"], bbox_to_anchor=(0.95, 0.95), loc='upper right')
        plt.yticks(sum_of_squares)
        ax2 = ax.twinx()
        sns.lineplot(x=range(n_cluster_min, n_cluster_max + 1), y=silhouette, marker='o', color='red')
        plt.legend(labels=["Silhouette"], bbox_to_anchor=(0.95, 0.9), loc='upper right')
        plt.xticks(range(n_cluster_min, n_cluster_max + 1))
        plt.yticks(silhouette)
        plt.grid(True)

        print(f'Optimal k for elbow method: {k_elbow_best}')
        print(f'Optimal k for silhouette method: {k_silhouette_best}')

    def calculate_wcss(self, data, x_min, x_max):
        """
            WCSS (Within-Cluster Sum of Squares) é uma medida utilizada no algoritmo K-means para avaliar a qualidade da clusterização.
            Essa medida calcula a soma dos quadrados das distâncias entre cada amostra e o centro do cluster ao qual ela pertence.
            WCSS é igual a inércia. Quanto maior a inércia mais próximo aqueles dados estão de seu centróide.

        """

        wcss = []
        for n in range(x_min, x_max + 1):
            kmeans = KMeans(n_clusters=n, random_state=self.random_state, n_init=x_max)
            kmeans.fit(X=data)
            wcss.append(kmeans.inertia_)

        return wcss

    def elbow_optimal_number_of_clusters(self, wcss):
        x1, y1 = 2, wcss[0]
        x2, y2 = 20, wcss[len(wcss) - 1]

        distances = []
        for i in range(len(wcss)):
            x0 = i + 2
            y0 = wcss[i]
            numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
            denominator = sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
            distances.append(numerator / denominator)

        return distances.index(max(distances)) + 2

    def silhouette_optimal_number_of_clusters(self, data, x_min, x_max):
        """
            O coeficiente silhuera varia de -1 a +1, em que
            +1 denota está muito coeso com seu cluster e muitos distante dos demais clusters;
            0 denota sobreposição de clusters
            -1 indica resultados muito ruins.
        """

        silhouette = []

        n = [i for i in range(x_min, x_max + 1)]

        for i in range(x_min, x_max + 1):
            kmeans = KMeans(n_clusters=i, random_state=self.random_state, n_init=x_max)
            kmeans.fit(data)
            silhouette.append(silhouette_score(data,
                                               kmeans.labels_,
                                               metric='euclidean'))

        k_silhouette_best = n[silhouette.index(max(silhouette))]

        return k_silhouette_best, silhouette, n

