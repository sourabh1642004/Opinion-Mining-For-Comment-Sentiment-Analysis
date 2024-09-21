from django.http import HttpResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.shortcuts import render, redirect

def index(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        with open('comments.txt', 'a') as file:
            file.write(comment + '\n')
        return redirect('index')
    return render(request, "index.html")