from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from ..models import Thread, ThreadComment


def index(request):
    threads = Thread.objects.all().order_by('-num_favorites')[:10]
    
    return render(request, 'threads/index.html', {'threads': threads})


def detail(request, id):
    thread = get_object_or_404(Thread, id=id)
    comments = ThreadComment.objects.filter(thread_id=id).order_by('-created_at')[:10]
    
    # コメント書き込み処理
    if request.method == 'POST':
        pass
        
    
    return render(request, 'threads/detail.html', {'thread': thread, 'comments': comments})
    
    
# スレッド作成処理
def create(request):
    pass