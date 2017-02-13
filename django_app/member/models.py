import random
import sys
from django.db import models, IntegrityError


class MyUser(models.Model):
    username = models.CharField('유저네임', unique=True, max_length=30)
    last_name = models.CharField('성', max_length=20)
    first_name = models.CharField('이름', max_length=20)
    nickname = models.CharField('닉네임', max_length=20)
    email = models.EmailField('이메일', blank=True)
    date_joined = models.DateField('가입한 날짜', auto_now_add=True)
    last_modified = models.DateField('수정한 날짜', auto_now=True)

    # following = models.ManyToManyField(
    #     'self',
    #     verbose_name='Following User',
    #     symmetrical=False,
    #     blank=True,
    # )

    def __str__(self):
        return self.username

    @staticmethod
    def create_dummy_user(num):
        """
        num 개수만큼 User1 ~ User<num>까지 임의의 유저를 생성한다.
        :return: 생성된 유저 수
        """
        last_name_list = ['박', '이', '김', '서']
        first_name_list = ['민아', '혜리', '소진', '아영']
        nickname_list = ['빵', '리헬', '쏘지', '율곰']
        created_count = 0
        for i in range(num):
            try:
                MyUser.objects.create(
                    username='User {}'.format(i + 1),
                    last_name=random.choice(last_name_list),
                    first_name=random.choice(first_name_list),
                    nickname=random.choice(nickname_list)
                )
                created_count += 1
            # 무결성 검사
            except IntegrityError as e:
                print(e)
        return created_count

    @staticmethod
    def assign_global_variables():
        # sys 모듈은 파이썬 인터프리터 관련 내장모듈
        #  __main__ 모듈을 module 변수에 할당
        module = sys.modules['__main__']
        users = MyUser.objects.filter(username__startswith='User')
        for index, user in enumerate(users):
            # 글로벌 변수를 할당하기 위해서 메인 모듈에서 하는 것
            # __main__ 모듈에 'u1, uw, u3, ...' 이름으로 각 MyUser객체를 할당
            setattr(module, 'u{}'.format(index + 1), user)


    def follow(self, myuser):
        pass

    def unfollow(self, myuser):
        pass

    @property
    def followers(self):
        pass

    def change_nickname(self):
        pass
