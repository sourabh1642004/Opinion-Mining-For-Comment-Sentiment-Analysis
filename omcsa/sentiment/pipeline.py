# omcsa/sentiment/pipeline.py
import pickle
import tensorflow as tf
from sklearn.pipeline import Pipeline
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from googletrans import Translator
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
from .text_preprocessor import TextPreprocessor
import pycountry
import langid
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Ensure consistent language detection results
DetectorFactory.seed = 0

# Load the custom model and tokenizer
model = tf.keras.models.load_model('sentiment_model.h5')
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

class SentimentPipeline:
    def __init__(self, model, tokenizer, max_length=100):
        self.model = model
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.translator = Translator()

    def preprocess(self, text):
        lang_code, _ = langid.classify(text)
        lang_name = self.get_language_name(lang_code)

        translated_text = self.translator.translate(text, dest='en').text if lang_code != 'en' else text
        return translated_text, lang_name

    def get_language_name(self, lang_code):
        if '-' in lang_code:
            lang_code = lang_code.split('-')[0]
        
        language = pycountry.languages.get(alpha_2=lang_code)
        return language.name if language else lang_code

    def predict(self, text):
        translated_text, lang_name = self.preprocess(text)
        text_seq = self.tokenizer.texts_to_sequences([translated_text])
        text_pad = pad_sequences(text_seq, maxlen=self.max_length, padding='post', truncating='post')
        sentiment_score = self.model.predict(text_pad)[0][0]
        # Adjusted threshold for NEUTRAL sentiment
        if sentiment_score > 0.6:
            sentiment = 'POSITIVE'
        elif sentiment_score < 0.4:
            sentiment = 'NEGATIVE'
        else:
            sentiment = 'NEUTRAL'
        return text, lang_name, sentiment, translated_text

# Initialize the pipeline
sentiment_pipeline = SentimentPipeline(model, tokenizer)