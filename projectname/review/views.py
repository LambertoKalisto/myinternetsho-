from django.shortcuts import render, redirect
from .models import Reviews
from .forms import ReviewsForm
from django.db.models import Avg, F


def review(request):
    # Getting the three latest reviews, ordered by date
    reviews = Reviews.objects.order_by('-date')[:3]

    # Getting the average rating of reviews
    result = Reviews.objects.aggregate(середне=Avg('rate'))
    avg = result.get('середне', 0)

    # Passing reviews and average rating to the template for display on the 'reviews.html' page
    return render(request, 'review/reviews.html', {'reviews': reviews, 'avg': round(avg, 1)})

def create(request):
    error = ''
    if request.method == 'POST':
        # Creating a form for entering a new review
        form = ReviewsForm(request.POST)
        if form.is_valid():
            # Saving the new review to the database
            form.save()
            # Redirecting the user to the home page after successfully creating the review
            return redirect('home')
        else:
            # Handling the case where the form is filled incorrectly
            error = 'Не вірно заповнено форму'

    # Initializing an empty form for entering a new review
    form = ReviewsForm()

    data = {
        'form': form,
        'error': error,
    }

    # Passing the form and error to the template for display on the 'create.html' page
    return render(request, 'review/create.html', data)