from django.shortcuts import render
from .models import Articles

def news_home(request):
    # Get all articles ordered by date
    news = Articles.objects.order_by('-date')
    # Passing articles to a template for display on the 'news_home' page
    return render(request, 'news/news_home.html', {'news': news})
