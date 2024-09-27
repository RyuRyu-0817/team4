from django.shortcuts import render, get_object_or_404, redirect
from ..models import KnowHow, KnowHowComment
from ..forms.knowhow_threads_forms import KnowhowCommentCreateForm, KnowhowCreateForm
from ..utils import upload_file_to_s3


# knowhowのviewsを書くところ
def index(request):    
    knowhows = KnowHow.objects.all().order_by('-num_favorites')[:10]

    return render(request, 'knowhow.html', {'knowhows': knowhows})


def detail(request, id): 
    knowhow = get_object_or_404(KnowHow, id=id)    
    comments = knowhow.knowhowcomment_set.all()
    # comments = ThreadComment.objects.filter(
    #     thread=id).order_by('-created_at')[:10]

    # コメント書き込み処理．
    if request.method == 'POST':        
        form = KnowhowCommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.knowhow = knowhow
            comment.save()
            return redirect('knowhow_detail', id=id)
    else:
        form = KnowhowCommentCreateForm()        

    return render(request, 'knowhowdetail.html', {
        'knowhow': knowhow,
        'comments': comments,
        'form': form
    })


# ノウハウ作成処理
def create(request):
    if request.method == 'POST':    
        form = KnowhowCreateForm(request.POST, request.FILES)    
        if form.is_valid():
            knowhow = form.save(commit=False)
            knowhow.author = request.user  # 投稿者はログインしているユーザーにする

            # ファイルがアップロードされている場合
            if 's3_url' in request.FILES:               
               filename = request.FILES['s3_url'].name
               knowhow.s3_url = upload_file_to_s3(request.FILES['s3_url'].file, filename)
            else:                
                knowhow.s3_url = ''            

            knowhow.save()
            form.save_m2m()  # ManyToManyFieldの保存
            return redirect('knowhow_index')  # 成功後のリダイレクト
    else:
        form = KnowhowCreateForm()

    return render(request, 'knowhowcreate.html', {'form': form})
