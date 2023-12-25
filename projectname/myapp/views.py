from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.views.generic import ListView
from django.db.models import Q

def index(request):
    prod = Product.objects.order_by('-date')
    return render(request, 'myapp/index.html', {'prod': prod})

def about(request):
    return render(request, 'myapp/about.html')

class Search(ListView):

    template_name = 'myapp/index.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        search_query = self.request.GET.get('q', '').strip()
        return Product.objects.filter(Q(title__icontains=search_query))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context




