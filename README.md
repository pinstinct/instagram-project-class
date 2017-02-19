# 소개
구현한 주요 기능은 다음과 같다.

1. 사진 등록
2. 팔로우 하기
3. 좋아요 하기
4. 코멘트 남기기
5. 로그인 하기 (Custom User Model 생성)
6. 회원 가입
7. CSS 

# 프로젝트 관리

```shell
.
├── README.md
├── django_app
│   ├── db.sqlite3
│   ├── manage.py
│   ├── instagram (프로젝트)
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── wsgi.py
│   ├── member (어플리케이션)
│   ├── post (어플리케이션)
└── requirements.txt

```

## Requirements
- Python (3.4.3)
- Django (1.10.5)
- Pillow (4.0.0)

## Installation
```shell
$ pip install -r 'requierements.txt'
```