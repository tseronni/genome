import spacy


class SpacyUtil:
    def __init__(self, model='en_core_web_sm'):

        self.model_name = model
        self.nlp = spacy.load(self.model_name)

    def preprocess_text(self, text='', lemma=True, remove_stopwords=True, lower=True, remove_numbers=True):

        doc = self.nlp(text)

        tokens = []
        for token in doc:
            if (remove_stopwords and token.is_stop) or token.is_punct or (remove_numbers and token.like_num):
                continue
            token_text = token.lemma_.lower() if lemma else token.text
            if not lower:
                token_text = token_text.capitalize()
            tokens.append(token_text)

        return ' '.join(tokens)

