from django.shortcuts import render
from langdetect import detect
from googletrans import Translator
import pycountry
from transformers import pipeline
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

# Global variable to store the uploaded file in memory
uploaded_file_content = None

def get_language_name(lang_code):
    try:
        # Handle locale codes like 'zh-cn'
        if '-' in lang_code:
            lang_code = lang_code.split('-')[0]
        return pycountry.languages.get(alpha_2=lang_code).name
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
        sentiment_analyzer = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

        for original_comment in comments:
            lang_code = detect(original_comment)
            lang_name = get_language_name(lang_code)
            translated_comment = translator.translate(original_comment, dest='en').text if lang_code != 'en' else original_comment

            sentiment_result = sentiment_analyzer(translated_comment)[0]
            sentiment = sentiment_result['label']

            sentiments.append((original_comment, lang_name, sentiment, translated_comment))

    return render(request, 'index.html', {
        'sentiments': sentiments,
        'uploaded_file': uploaded_file,
    })