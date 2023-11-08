# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.decomposition import TruncatedSVD
# import numpy as np
#
#
# class TFIDFUtil:
#     def __init__(self, max_features=1000, ngram_range=(1, 1), max_df=0.5, min_df=2):
#         self.vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=ngram_range, max_df=max_df, min_df=min_df)
#
#     def fit_corpus(self, documents):
#         """ Fit the TF-IDF vectorizer to the entire corpus. """
#         self.vectorizer.fit(documents)
#
#     def extract_keywords(self, document, top_n=10):
#         """ Extract top N keywords from a single document using the TF-IDF score. """
#         # Generate the TF-IDF matrix for the document
#         tfidf_matrix = self.vectorizer.transform([document])
#
#         # Get the feature names
#         feature_names = np.array(self.vectorizer.get_feature_names_out())
#
#         # Sort the indices of the feature matrix in descending order of scores
#         sorted_indices = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]
#
#         # Get the top n feature names and their scores
#         top_features = [(feature_names[index], tfidf_matrix[0, index]) for index in sorted_indices[:top_n]]
#
#         # Return only the feature names as a comma-separated string
#         keywords_string = ', '.join(feature for feature, score in top_features)
#
#         return keywords_string

