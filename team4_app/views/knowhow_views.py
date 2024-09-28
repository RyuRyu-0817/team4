from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from ..models import KnowHow, KnowHowComment, Category, KnowHowLike
from ..forms.knowhow_threads_forms import KnowhowCommentCreateForm, KnowhowCreateForm, SearchForm, SortForm, SORT_CHOICES
from ..utils import upload_file_to_s3
from django.http import JsonResponse
import json

from django.db.models import Count, Q

def index(request):        
    knowhows = KnowHow.objects.all()
    search_form = SearchForm(request.GET or None)    
    sort_form = SortForm(request.GET or None)
    categories = Category.objects.all()

    # リクエスト者がどのノウハウにいいねしてるか
    like_knowhows = []
    if request.user.is_authenticated:
        for knowhow in knowhows:
            if knowhow.knowhowlike_set.filter(user=request.user).exists():
                like_knowhows.append(knowhow)

    # 検索フォームの処理
    if search_form.is_valid():        
        query = search_form.cleaned_data.get('query', '')        
        if query:
            knowhows = knowhows.filter(Q(title__icontains=query) | Q(discription__icontains=query))  # 検索結果でフィルタリング

    # ソートフォームの処理（検索後もソート適用）
    if sort_form.is_valid():
        sort_by = sort_form.cleaned_data.get('sort_by', '')
        if sort_by == 'latest':
            knowhows = knowhows.order_by('-created_at')
        elif sort_by == 'likes':
            knowhows = knowhows.annotate(num_likes=Count('knowhowlike')).order_by('-num_likes') 
        else:            
            pass

    # テンプレートのレンダリング
    return render(request, 'knowhow.html', {
        'search_form': search_form,         
        'sort_form': sort_form, 
        'knowhows': knowhows,
        'categories': categories,
        "like_knowhows": like_knowhows
    })


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

def categories(request, id):
    category = get_object_or_404(Category, id=id)
    knowhows = KnowHow.objects.filter(categories=category)  
    search_form = SearchForm(request.GET or None)
    sort_form = SortForm(request.GET or None)
    categories = Category.objects.all()

    # リクエスト者がどのノウハウにいいねしてるか
    like_knowhows = []
    if request.user.is_authenticated:
        for knowhow in knowhows:
            if knowhow.knowhowlike_set.filter(user=request.user).exists():
                like_knowhows.append(knowhow)

    # 検索フォームの処理
    if search_form.is_valid():        
        query = search_form.cleaned_data.get('query', '')        
        if query:
            knowhows = knowhows.filter(Q(title__icontains=query) | Q(discription__icontains=query))  # 検索結果でフィルタリング

    # ソートフォームの処理（検索後もソート適用）
    if sort_form.is_valid():
        sort_by = sort_form.cleaned_data.get('sort_by', '')
        if sort_by == 'latest':
            knowhows = knowhows.order_by('-created_at')
        elif sort_by == 'likes':
            knowhows = knowhows.annotate(num_likes=Count('knowhowlike')).order_by('-num_likes') 
        else:            
            pass

    return render(request, 'knowhow_category.html', {
        'category': category,         
        'search_form': search_form, 
        'sort_form': sort_form,
        'knowhows': knowhows,
        'categories': categories,
        "like_knowhows": like_knowhows
        
        })

def like_knowhow(request):
    # リクエストボディをJSONとして解析
    
    data = json.loads(request.body)
    knowhow_id = data.get('knowhow_id')
        
    
    knowhow = KnowHow.objects.get(id=knowhow_id)

    
    is_liked = KnowHowLike.objects.filter(user=request.user, knowhow=knowhow).exists()

    if is_liked:
        KnowHowLike.objects.filter(user=request.user, knowhow=knowhow).delete()
        is_liked = False
    else:
        print("create")
        KnowHowLike.objects.create(user=request.user, knowhow=knowhow)
        is_liked = True

    return JsonResponse({'is_liked': is_liked, 'total_likes': knowhow.knowhowlike_set.count()})