from django.shortcuts import render

# homeのviewsを書くところ
def index(request):
    return render(request, 'index.html')
