from django.shortcuts import render
from django.db.models import Count, Sum
from ..models import KnowHow, School, CustomUser


# homeのviewsを書くところ
def index(request):
    
    top_schools = School.objects.annotate(
        total_likes=Count('customuser__knowhow__knowhowlike')
    ).order_by('-total_likes')[:5]

    # 学校ごとのユーザーごとの「いいね数」を集計
    schools_with_users = []
    for school in top_schools:
        # 学校に属するユーザーごとの「いいね数」を集計
        users_in_school = CustomUser.objects.filter(school=school).annotate(
            user_likes=Count('knowhow__knowhowlike')
        ).order_by('-user_likes')
        schools_with_users.append({
            'school': school,
            'users': users_in_school
        })

    # ユーザーごとのノウハウの総イイネ数を集計して、上位5位を取得
    top_users = CustomUser.objects.annotate(
        total_likes=Count('knowhow__knowhowlike')
    ).order_by('-total_likes')[:5]

    # 両方のデータを1つのコンテキストにまとめてテンプレートに渡す
    context = {
        'schools_with_users': schools_with_users,
        'top_users': top_users,
    }


    return render(request, 'home.html', context)
