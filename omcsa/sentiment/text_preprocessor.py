# omcsa/text_preprocessor.py
from sklearn.base import BaseEstimator, TransformerMixin
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore

class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, tokenizer, max_length=100):
        self.tokenizer = tokenizer
        self.max_length = max_length

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_seq = self.tokenizer.texts_to_sequences(X)
        X_pad = pad_sequences(X_seq, maxlen=self.max_length, padding='post', truncating='post')
        return X_pad