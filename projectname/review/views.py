from django.shortcuts import render, redirect
from .models import Reviews
from .forms import ReviewsForm
from django.db.models import Avg, F


def review(request):
    # Отримання трьох останніх відгуків, впорядкованих за датою
    reviews = Reviews.objects.order_by('-date')[:3]

    # Отримання середнього значення рейтингу відгуків
    result = Reviews.objects.aggregate(середне=Avg('rate'))
    avg = result.get('середне', 0)

    # Передача відгуків та середнього рейтингу у шаблон для відображення на сторінці 'reviews.html'
    return render(request, 'review/reviews.html', {'reviews': reviews, 'avg': round(avg, 1)})

def create(request):
    error = ''
    if request.method == 'POST':
        # Створення форми для введення нового відгуку
        form = ReviewsForm(request.POST)
        if form.is_valid():
            # Збереження нового відгуку в базі даних
            form.save()
            # Перенаправлення користувача на домашню сторінку після успішного створення відгуку
            return redirect('home')
        else:
            # Обробка випадку, коли форма заповнена невірно
            error = 'Не вірно заповнено форму'

    # Ініціалізація порожньої форми для введення нового відгуку
    form = ReviewsForm()

    data = {
        'form': form,
        'error': error,
    }

    # Передача форми та помилки у шаблон для відображення на сторінці 'create.html'
    return render(request, 'review/create.html', data)