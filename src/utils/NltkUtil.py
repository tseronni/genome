# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# from collections import Counter
# import string
# from rake_nltk import Rake
#
#
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('omw-1.4')  # Para o lematizador funcionar com diferentes idiomas
#
# class NLTKUtil:
#     def __init__(self, language='english', lemma=True, remove_stopwords=True, lower=True, remove_numbers=True):
#         self.language = language
#         self.lemma = lemma
#         self.remove_stopwords = remove_stopwords
#         self.lower = lower
#         self.remove_numbers = remove_numbers
#         self.lemmatizer = WordNetLemmatizer() if lemma else None
#         self.stopwords = set(stopwords.words(language)) if remove_stopwords else set()
#
#     def preprocess_text(self, text):
#         # Tokenize text
#         tokens = word_tokenize(text, language=self.language)
#         return ' '.join([self._process_token(token) for token in tokens if token])
#
#     def _process_token(self, token):
#         # Check if we should remove numbers
#         if token.isdigit() and self.remove_numbers:
#             return ''
#         # Convert to lower case if needed
#         if self.lower:
#             token = token.lower()
#         # Remove stopwords and punctuation
#         if token in self.stopwords or token in string.punctuation:
#             continue
#         # Lemmatize token if needed
#         if self.lemma:
#             token = self.lemmatizer.lemmatize(token)
#         return token
#
#     def extract_keywords(self, text, max_keywords=10):
#         tokens = word_tokenize(text, language=self.language)
#         keywords = [token.lower() for token in tokens if token.lower() not in self.stopwords and token not in string.punctuation]
#         keyword_freq = Counter(keywords)
#         return [keyword for keyword, freq in keyword_freq.most_common(max_keywords)]
#
#     def extract_keywords_using_rake(self, text):
#         rake = Rake(stopwords=self.stopwords)
#         rake.extract_keywords_from_text(text)
#         return rake.get_ranked_phrases()
#
