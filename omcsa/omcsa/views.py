from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from textblob import TextBlob
from langdetect import detect
from googletrans import Translator
import pycountry

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
    translator = Translator()
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            comments = file.read().decode('utf-8').splitlines()
        else:
            comments = [request.POST.get('comment')]

        for comment in comments:
            lang_code = detect(comment)
            lang_name = get_language_name(lang_code)
            original_comment = comment
            if lang_code != 'en':
                comment = translator.translate(comment, src=lang_code, dest='en').text
            analysis = TextBlob(comment)
            if analysis.sentiment.polarity > 0:
                sentiment = 'Positive'
            elif analysis.sentiment.polarity < 0:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'
            sentiments.append((original_comment, lang_name, sentiment))

    return render(request, 'index.html', {'sentiments': sentiments})