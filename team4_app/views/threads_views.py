from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from ..models import Thread, ThreadComment
from ..forms.knowhow_threads_forms import CommentForm


def index(request):
    threads = Thread.objects.all().order_by('-num_favorites')[:10]

    return render(request, 'thread.html', {'threads': threads})


def detail(request, id): 
    thread = get_object_or_404(Thread, id=id)    
    comments = thread.threadcomment_set.all()
    # comments = ThreadComment.objects.filter(
    #     thread=id).order_by('-created_at')[:10]

    # コメント書き込み処理．
    if request.method == 'POST':        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.thread_id = thread
            comment.save()
            return redirect('threads_detail', id=id)
    else:
        form = CommentForm()        

    return render(request, 'threaddetail.html', {
        'thread': thread,
        'comments': comments,
        'form': form
    })


# スレッド作成処理
def create(request):
    pass
