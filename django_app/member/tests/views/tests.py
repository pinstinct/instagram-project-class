from django.test import TestCase

from member.models import MyUser


class ProfileViewTest(TestCase):
    def test_user_not_authenticated(self):
        url_profile = '/member/profile/'
        response = self.client.get(url_profile)
        self.assertRedirects(
            response,
            '/member/login/?next={}'.format(
                url_profile
            )
        )


class UserLoginTest(TestCase):
    def logout_user_redirect_to_where(self, where):
        test_url = where
        response = self.client.get(test_url)
        return self.assertRedirects(response, '/member/login/?next=' + test_url)

    def login_user_redirect_to_where(self, where):
        test_url = where
        test_username = 'test_user'
        test_password = 'test_password'
        MyUser.objects.create_user(test_username, test_password)
        self.client.post(
            '/member/login/',
            {
                'username': test_username,
                'password': test_password,
            }
        )
        response = self.client.get(test_url)
        return self.assertEqual(response.status_code, 200)

    def test_profile_logout_user(self):
        return self.logout_user_redirect_to_where('/member/profile/')

    def test_profile_login_user(self):
        return self.login_user_redirect_to_where('/member/profile/')

    def test_change_profile_logout_user(self):
        return self.logout_user_redirect_to_where('/member/profile/image/')

    def test_change_profile_login_user(self):
        return self.login_user_redirect_to_where('/member/profile/image/')
