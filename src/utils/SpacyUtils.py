import spacy
from collections import Counter


class SpacyUtil:
    def __init__(self, model='en_core_web_sm', lemma=True, remove_stopwords=True, lower=True, remove_numbers=True):

        self.model_name = model
        self.nlp = spacy.load(self.model_name)
        self.lemma = lemma
        self.remove_stopwords = remove_stopwords
        self.lower = lower
        self.remove_numbers = remove_numbers

    def preprocess_text(self, text=''):

        doc = self.nlp(text)

        tokens = []
        for token in doc:
            if (self.remove_stopwords and token.is_stop) or token.is_punct or (self.remove_numbers and token.like_num):
                continue
            token_text = token.lemma_.lower() if self.lemma else token.text
            if not self.lower:
                token_text = token_text.capitalize()
            tokens.append(token_text)

        return ' '.join(tokens)

    def extract_keywords(self, text, max_keywords=10, use_noun=True, use_adj=True, use_verb=True):

        doc = self.nlp(text)

        pos_to_include = set()
        if use_noun:
            pos_to_include.add('NOUN')
        if use_adj:
            pos_to_include.add('ADJ')
        if use_verb:
            pos_to_include.add('VERB')

        # Extract lemmatized tokens of the specified parts of speech
        keywords = [token.lemma_.lower() for token in doc
                    if token.pos_ in pos_to_include and not token.is_stop and not token.is_punct]

        # Count the frequency of each keyword
        keyword_freq = Counter(keywords)

        # Extract the most common keywords based on the frequency
        most_common_keywords = keyword_freq.most_common(max_keywords)

        # Return a list of keywords
        keywords_string = ', '.join(keyword for keyword, freq in most_common_keywords)

        return keywords_string

