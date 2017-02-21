from django.test import TestCase
from selenium.webdriver.common.keys import Keys

from member.models import MyUser


def make_user_and_login(client):
    # 유저 생성
    test_username = 'test_user'
    test_password = 'test_password'
    user = MyUser.objects.create_user(test_username, test_password)

    # 유저를 로그인
    client.browser.get(client.make_url('/member/login/'))
    input_username = client.browser.find_element_by_id('id_username')
    input_username.send_keys(test_username)
    input_password = client.browser.find_element_by_id('id_password')
    input_password.send_keys(test_password)
    input_password.send_keys(Keys.ENTER)
    return user


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


class ChangeProfileImageViewTest(TestCase):
    def test_user_not_authenticated(self):
        url_change_profile_img = '/member/profile/image/'
        response = self.client.get(url_change_profile_img)
        self.assertRedirects(
            response,
            '/member/login/?next={}'.format(
                url_change_profile_img
            )
        )

    def test_uses_change_profile_image_template(self):
        test_username = 'test_username'
        test_password = 'test_password'
        user = MyUser.objects.create_user(
            username=test_username,
            password=test_password
        )
        response = self.client.get('/member/profile/image/')
        self.assertTemplateUsed(
            response,
            'member/change_profile_image.html'
        )

    def test_url_resolves_to_change_profile_image(self):
        pass


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
