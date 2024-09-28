from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from ..models import Thread, ThreadComment
from ..forms.knowhow_threads_forms import ThreadCreateForm, ThreadCommentCreateForm
from django.contrib.auth.decorators import login_required

def index(request):    
    threads = Thread.objects.all()[:10]

    return render(request, 'thread.html', {'threads': threads})


def detail(request, id): 
    thread = get_object_or_404(Thread, id=id)    
    comments = thread.threadcomment_set.all()
    # comments = ThreadComment.objects.filter(
    #     thread=id).order_by('-created_at')[:10]

    # コメント書き込み処理．
    if request.method == 'POST':        
        form = ThreadCommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.thread_id = thread
            comment.save()
            return redirect('threads_detail', id=id)
    else:
        form = ThreadCommentCreateForm()        

    return render(request, 'threaddetail.html', {
        'thread': thread,
        'comments': comments,
        'form': form
    })


# スレッド作成処理
def create(request):
    if request.method == 'POST':    
        form = ThreadCreateForm(request.POST, request.FILES)        
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user  # 投稿者はログインしているユーザーにする

            # ファイルがアップロードされている場合
            if 's3_url' in request.FILES:
                pass

            else:                
                thread.s3_url = ''            

            thread.save()
            form.save_m2m()  # ManyToManyFieldの保存
            return redirect('threads_detail', id=thread.id)  # 成功後のリダイレクト
    else:
        form = ThreadCreateForm()
    return render(request, 'threadcreate.html', {'form': form})

def like_thread(request):
    pass
