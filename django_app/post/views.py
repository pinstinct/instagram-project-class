"""
Post List를 보여주는 화면을 구성
1. View에 post_list 함수 작성
2. Template에 post_list.html 파일 작성
3. View에서 post_list.html을 render한 결과를 리턴하도록 함
4. instagram/urls.py에 post/urls.py를 연결시킴 (app_name은 post)
5. '/post/'로 접속했을 때, post_list View에 연결되도록 post/urls.py에 내용을 작성
6. 전체 Post를 가져오는 쿼리셋을 context로 넘기도록 post_list뷰에 구현
7. post_list.html에서 {% for %} 태그를 사용해 post_list의 내용을 순회하며 표현
"""

from django.shortcuts import render
from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'post/post_list.html', context)
