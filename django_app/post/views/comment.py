from django.shortcuts import redirect

from post.forms import CommentForm
from post.models import Post, Comment

__all__ = (
    'comment_add',
    'comment_delete',
)


def comment_add(request, post_id):
    if request.method == 'POST':
        form = CommentForm(data=request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']

            # 세션 미들위어가 request에 user객체를 넣어 보내줌
            user = request.user
            post = Post.objects.get(id=post_id)

            # 아래와 동일한데 모델에 구현한 기능을 사용
            # post.add_comment(user, content)

            Comment.objects.create(
                author=user,
                post=post,
                content=content,
            )
        return redirect('post:list')


def comment_delete(request, post_id, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        if comment.author.id == request.user.id:
            comment.delete()
        return redirect('post:list')
