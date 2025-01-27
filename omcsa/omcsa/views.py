from django.shortcuts import render
from sentiment.pipeline import sentiment_pipeline
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

# Global variable to store the uploaded file in memory
uploaded_file_content = None

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
        for original_comment in comments:
            sentiment_result = sentiment_pipeline.predict(original_comment)
            sentiments.append(sentiment_result)

    return render(request, 'index.html', {
        'sentiments': sentiments,
        'uploaded_file': uploaded_file,
    })