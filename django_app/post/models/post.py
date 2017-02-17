from django.conf import settings
from django.db import models

from member.models import MyUser

__all__ = (
    'Post',
    'PostLike',
)


# 둘 중에 편한 방식을 사용하면 됨 (두 가지 방식이 있음)
class PostManager(models.Manager):
    def visible(self):
        return super().get_queryset().filter(is_visible=True)


class PostUserVisibleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='post', blank=True)
    content = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(
        MyUser,
        through='PostLike',
        related_name='like_post_set',
    )
    is_visible = models.BooleanField(default=True)

    # Default 모델 매니저 교체
    objects = PostManager()
    # 커스텀 모델 매니저 추가
    visible = PostUserVisibleManager()

    # Post.obejcts.all() : 모든것 보임
    # Post.objecst.visible() : 디폴트 모델 매니져 교체
    # Post.visibles.all() : 커스텀 추가

    def __str__(self):
        return 'Post[{}]'.format(self.id)

    class Meta:
        ordering = ('-id',)

    def toggle_like(self, user):
        # 중간자 모델을 사용하기 때문에 PostLike 중간자 모델 매니저를 사용
        # 핵심은 중간자 모델을 거쳐서 해야한다는 것이다.

        # PostLike 중간자 모델에서 인자로 전달된 Post, MyUser 객체를 가진 row를 조회
        # pl_list = PostLike.objects.filter(post=self, user=user)
        pl_list = self.postlike_set.filter(user=user)

        # 현재 인자로 전달된 user가 해당 Post(self)를 좋아여 한 적이 있는지 검사
        # 만약에 이미 좋아요를 했을 경우 해당 내역을 삭제
        # 아직 내역이 없을 경우 생성
        if pl_list.exists():
            pl_list.delete()
        else:
            PostLike.objects.create(post=self, user=user)

            # 파이썬 삼항연산자
            # [True일 경우 실행할 구문] if 조건문 else [False일 경우 실행할 구문]
            # return PostLike.objects.create(post=self, user=user) if not pl_list.exists() else pl_list.delete()

    def add_comment(self, user, content):
        # 자신에게 연결된 Comment 객체의 역참조 매니저(comment_set)로 부터
        # create 메서드를 이용해 Comment 객체를 생성
        return self.comment_set.create(
            user=user,
            content=content
        )

    @property
    def like_count(self):
        return self.like_users.count()

    @property
    def comment_count(self):
        return self.comment_set.count()


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            ('user', 'post'),
        )

    def __str__(self):
        return 'Post[{}]\'s Like[{}]'.format(
            self.post_id,  # DB 까지 가서 검색함
            self.id,
        )
