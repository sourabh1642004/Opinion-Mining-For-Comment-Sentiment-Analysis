from django.http import HttpResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.shortcuts import render, redirect
from textblob import TextBlob

def index(request):
    sentiment = None
    if request.method == 'POST':
        comment = request.POST.get('comment')
        with open('comments.txt', 'a') as file:
            file.write(comment + '\n')
        analysis = TextBlob(comment)
        if analysis.sentiment.polarity > 0:
            sentiment = 'Positive'
        elif analysis.sentiment.polarity < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        return render(request, "index.html", {'sentiment': sentiment})
    return render(request, "index.html")