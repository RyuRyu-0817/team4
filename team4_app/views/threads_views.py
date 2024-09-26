from django.shortcuts import render

# threadsのviewsを書くところ
def index(request):
    return render(request, 'index.html')
