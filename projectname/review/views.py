from django.shortcuts import render, redirect
from .models import Reviews
from .forms import ReviewsForm
from django.db.models import Avg, F

def review(request):
    reviews = Reviews.objects.order_by('-date')[:3]
    result = Reviews.objects.aggregate(середне=Avg('rate'))
    avg = result.get('середне', 0)

    return render(request, 'review/reviews.html', {'reviews': reviews, 'avg': round(avg,1)})

def create(request):
    error = ''
    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Не вірно заповнено форму'

    form = ReviewsForm()

    data = {
        'form': form,
        'error': error,
    }

    return render(request, 'review/create.html', data)