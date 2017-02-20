from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from member.models import MyUser
from post.models import Post
from .forms import LoginForm, SignupForm, ProfileImageForm

"""
1. def login 뷰를 생성
2. member app을 include를 이용해 'member' namespace를 지정
    instagram/urls.py와 member/ulrs.py 모두 사용
3. login 뷰는 member/login URL과 연결되도록 member/urls.py 구현
4. login 뷰에서는 member/login.html 파일을 렌더함
5. settings.py에 TEMPLATE_DIR 변수를 할당하고 추가

과제 : 폼을 이용해 정상적으로 동작하게 해오기
html파일에서 POST 요청을 보내기 위해서 form을 정의하고
input 요소 2개의 name을 username, password로 설정하고
button type submit을 실행
(login.html에 작성하면됨)
"""


def login_fbv(request):
    """
    request.method == 'POST'일 때와 아닐 때의 동작을 구분
    POST일 때는 authenticate, login을 거치는 로직을 실행
    GET일 때는 member/login.html을 render하여 return 한다.
    """

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            # authenticate 인자로 POST로 전달받은 username, password 사용
            user = authenticate(username=username, password=password)
            if user is not None:
                # 장고의 인증관리 시스템을 이용하여 세션을 관리해주기 위해 login() 함수 사용
                login(request, user)
                # return HttpResponse('Login Success')
                return redirect('post:list')
            else:
                form.add_error(None, 'ID or PW incorrect')
                # return HttpResponse('Login Failed')
    # GET method 요청이 온 경우
    else:
        # 빈 login form 객체를 생성
        form = LoginForm()
    context = {
        'form': form,
    }
    # return render(request, 'member/login.html')
    return render(request, 'member/login.html', context)


def signup_fbv(request):
    """
    회원 가입을 구현
    1. member/signup.html 파일 생성
    2. SignupForm 클래스 구현
    3. 해당 Form을 사용해서 signup.html 템플릿 구성
    4. POST 요청을 받아 MyUser 객체를 생성 후 로그인
    5. 로그인 완료되면 post_list 뷰로 이동
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.create_user()
            login(request, user)
            return redirect('post:list')
    else:
        form = SignupForm()
    context = {
        'form': form
    }
    return render(request, 'member/signup.html', context)


def logout_fbv(request):
    logout(request)
    return redirect('member:login')


@login_required
def profile(request):
    """
    자신의 게시물 수, 자신의 팔로워 수 자신의, 자신의 팔로잉 수
    context로 전달하여 출력
    :param request:
    :return:
    """
    post_count = Post.objects.filter(author=request.user).count()
    follower_count = request.user.follower_set.count()
    following_count = request.user.following.count()
    context = {
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
    }
    return render(request, 'member/profile.html', context)


def change_profile_image(request):
    """
    해당 유저의 프로필 이미지를 바꾼다.
    0. 유저 모델에 img_profile 필드 추가, migrations
    1. change_profile_image.html 파일 작성
    2. ProfileImageForm 생성
    3. 해당 Form을 템플릿에 렌더링
    4. request.method == 'POST'일 때 reqest.FILES의 값을 이용해서
    request.user의 img_profile을 변경 저장
    5. 처리 완료 후 member:profile 이동
    6. profile.html에서 user의 프로필 이미지를 img태그를 사용해서 보여줌
    {{ MEDIA_URL }}을 사용
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            user.img_profile = request.FILES['img_profile']
            user.save()
            return redirect('member:profile')
    else:
        form = ProfileImageForm()
    context = {
        'form': form
    }
    return render(request, 'member/change_profile_image.html', context)
