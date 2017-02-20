from django.test import LiveServerTestCase, Client

from member.models import MyUser


class IndexTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_user_is_not_authenticated_redirect_to_signup(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/member/signup/')

    def test_user_is_authenticated_redirect_to_signup(self):
        # 유저를 로그인 시킨다.
        # 테스트용 유저를 생성한다. (ORM)
        test_username = 'test_user'
        test_password = 'test_password'
        MyUser.objects.create_user(test_username, test_password)

        # member:login으로 POST요청을 보낸다. (self.client.post)
        # views의 login_fbv 함수 참고 
        self.client.post(
            '/member/login/',
            {
                'username': test_username,
                'password': test_password,
            }
        )

        # 이후 root url('/')의 response를 받아온다.
        response = self.client.get('/')

        # 해당 response가 /post/로 잘 redirect 되는지 확인
        self.assertRedirects(response, '/post/')
