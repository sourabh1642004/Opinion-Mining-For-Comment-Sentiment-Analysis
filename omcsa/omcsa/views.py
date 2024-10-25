from django.shortcuts import render
from langdetect import detect
from googletrans import Translator
import pycountry
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

def get_language_name(lang_code):
    try:
        # Handle locale codes like 'zh-cn'
        if '-' in lang_code:
            lang_code = lang_code.split('-')[0]
        return pycountry.languages.get(alpha_2=lang_code).name
    except AttributeError:
        return lang_code

def index(request):
    sentiments = []
    display_mode = request.POST.get('display_mode', 'graph')
    uploaded_file = request.FILES.get('file') if request.method == 'POST' else None

    if uploaded_file:
        request.session['uploaded_file'] = uploaded_file.read().decode('utf-8')
    elif 'uploaded_file' in request.session:
        uploaded_file = InMemoryUploadedFile(
            file=io.BytesIO(request.session['uploaded_file'].encode('utf-8')),
            field_name='file',
            name='uploaded_file.txt',
            content_type='text/plain',
            size=len(request.session['uploaded_file']),
            charset='utf-8'
        )

    if request.method == 'POST' or uploaded_file:
        comment = request.POST.get('comment', '')
        if uploaded_file:
            comments = uploaded_file.read().decode('utf-8').splitlines()
        else:
            comments = [comment]

        sia = SentimentIntensityAnalyzer()
        translator = Translator()

        for original_comment in comments:
            lang_code = detect(original_comment)
            lang_name = get_language_name(lang_code)
            translated_comment = translator.translate(original_comment, dest='en').text if lang_code != 'en' else original_comment

            sentiment_scores = sia.polarity_scores(translated_comment)
            if sentiment_scores['compound'] > 0:
                sentiment = 'Positive'
            elif sentiment_scores['compound'] < 0:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'
            sentiments.append((original_comment, lang_name, sentiment, translated_comment))

    positive_count = len([s for s in sentiments if s[2] == 'Positive'])
    neutral_count = len([s for s in sentiments if s[2] == 'Neutral'])
    negative_count = len([s for s in sentiments if s[2] == 'Negative'])

    return render(request, 'index.html', {
        'sentiments': sentiments,
        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,
        'display_mode': display_mode,
        'uploaded_file': uploaded_file,
    })