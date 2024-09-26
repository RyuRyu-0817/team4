from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from ..models import Thread, ThreadComment
from ..forms.knowhow_threads_forms import CommentForm

def index(request):
    threads = Thread.objects.all().order_by('-num_favorites')[:10]
    
    return render(request, 'threads/index.html', {'threads': threads})


def detail(request, id):
    thread = get_object_or_404(Thread, id=id)
    comments = ThreadComment.objects.filter(thread=id).order_by('-created_at')[:10]
    
    # コメント書き込み処理．
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.thread = thread
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    
    return render(request, 'threaddetail.html', {'thread': thread, 'comments': comments, 'form': form})
    
    
# スレッド作成処理
def create(request):
    pass