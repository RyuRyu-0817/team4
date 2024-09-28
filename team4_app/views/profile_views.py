from django.shortcuts import render, get_object_or_404
from ..models import CustomUser, KnowHow

def profile_view(request, id):    
    user = get_object_or_404(CustomUser, id=id)    
    knowhows = KnowHow.objects.filter(author=user).order_by('-created_at')  # 新しい順に並べる
    
    
    return render(request, 'profile.html', {'user': user,'knowhows': knowhows })
