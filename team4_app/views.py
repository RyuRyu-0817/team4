from django.shortcuts import render

# indexページのビュー
def index(request):
    return render(request, 'index.html')