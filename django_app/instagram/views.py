from django.shortcuts import redirect

"""
유저가 로그인했을 경우, post:list로 이동
로그인 하지 않았을 경우, member:signup으로 이동

테스트 작성
    1. index URL로 접근했을 때, 로그인 하지 않았을 경우 member:signup으로 가는지 확인
    2. 로그인 했을 경우 post:list로 가는지 확인
        2-1. 테스트용 유저를 생성
        2-2. 해당 유저 정보로 memeber:login에 POST요청 (로그인)
        2-3. 이후 위 테스트 실행
"""


def index(request):
    if request.user.is_authenticated:
        return redirect('post:list')

    else:
        return redirect('member:signup')
