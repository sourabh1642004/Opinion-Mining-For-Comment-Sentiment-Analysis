from django.shortcuts import render
from googletrans import Translator
import pycountry
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

# Ensure consistent language detection results
DetectorFactory.seed = 0

# Load the custom model and tokenizer
model = tf.keras.models.load_model('sentiment_model.h5')
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# Global variable to store the uploaded file in memory
uploaded_file_content = None

def get_language_name(lang_code):
    try:
        # Handle locale codes like 'zh-cn'
        if '-' in lang_code:
            lang_code = lang_code.split('-')[0]
        
        # Special handling for Hinglish (Hindi-English mixed text)
        if any(word in lang_code.lower() for word in ['hi', 'hin']):
            return 'Hinglish'
            
        language = pycountry.languages.get(alpha_2=lang_code)
        if language:
            return language.name
        else:
            return lang_code
    except AttributeError:
        return lang_code

def index(request):
    global uploaded_file_content
    sentiments = []
    uploaded_file = request.FILES.get('file') if request.method == 'POST' else None

    if request.method == 'POST' and uploaded_file:
        uploaded_file_content = uploaded_file.read().decode('utf-8')
    
    comment = request.POST.get('comment', '')
    comments = uploaded_file_content.splitlines() if uploaded_file_content else []

    if comment:
        comments.append(comment)

    if comments:
        translator = Translator()

        for original_comment in comments:
            try:
                # Improved language detection for Hindi and Hinglish
                if any(char.isascii() for char in original_comment) and any(not char.isascii() for char in original_comment):
                    lang_code = 'hi'  # Assuming mixed script is Hinglish
                else:
                    lang_code = detect(original_comment)
                lang_name = get_language_name(lang_code)
            except LangDetectException as e:
                lang_code = 'unknown'
                lang_name = 'Unknown'
                print(f"Error detecting language for comment '{original_comment}': {e}")

            translated_comment = translator.translate(original_comment, dest='en').text if lang_code != 'en' else original_comment

            # Tokenize and pad the comment
            comment_seq = tokenizer.texts_to_sequences([translated_comment])
            comment_pad = pad_sequences(comment_seq, maxlen=100, padding='post', truncating='post')

            # Predict sentiment
            sentiment_score = model.predict(comment_pad)[0][0]
            sentiment = 'POSITIVE' if sentiment_score > 0.5 else 'NEGATIVE'

            sentiments.append((original_comment, lang_name, sentiment, translated_comment))

    return render(request, 'index.html', {
        'sentiments': sentiments,
        'uploaded_file': uploaded_file,
    })