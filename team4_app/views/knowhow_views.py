from django.shortcuts import render

# knowhowのviewsを書くところ
def index(request):
    return render(request, 'index.html')
