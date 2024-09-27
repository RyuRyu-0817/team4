from django.shortcuts import render
from ..models import KnowHow


# homeのviewsを書くところ
def index(request):
    
    return render(request, 'home.html')
