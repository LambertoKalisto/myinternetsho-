from django.shortcuts import render
from .models import Articles

def news_home(request):
    # Отримання всіх статей, впорядкованих за датою
    news = Articles.objects.order_by('-date')
    # Передача статей у шаблон для відображення на сторінці 'news_home'
    return render(request, 'news/news_home.html', {'news': news})
