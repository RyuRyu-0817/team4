from django.shortcuts import render
from ..models import KnowHow
# knowhowのviewsを書くところ
def index(request):
    knowhow = KnowHow.objects.all().order_by('-num_favorites')[:10]
    
    return render(request, 'knowhow/index.html', {'knowhow': knowhow})
