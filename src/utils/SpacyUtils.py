import spacy


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

