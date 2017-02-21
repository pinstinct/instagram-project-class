import random

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from member.models import MyUser
from post.models import Post
from utils.test import make_dummy_users


class BaseTestCase(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(1)

    def tearDown(self):
        self.browser.quit()

    def make_url(self, url):
        result = '{}{}'.format(self.live_server_url, url)
        return result

    def make_user_and_login(self):
        # 유저 생성
        test_username = 'test_user'
        test_password = 'test_password'
        user = MyUser.objects.create_user(test_username, test_password)

        # 유저를 로그인
        self.browser.get(self.make_url('/member/login/'))
        input_username = self.browser.find_element_by_id('id_username')
        input_username.send_keys(test_username)
        input_password = self.browser.find_element_by_id('id_password')
        input_password.send_keys(test_password)
        input_password.send_keys(Keys.ENTER)
        return user


class NewVisitorTest(BaseTestCase):
    def test_first_visitor_redirect_to_signup(self):
        # 로그인하지 않은 유저가 member:signup으로 잘 이동했는지 확인
        self.browser.get(self.live_server_url)
        self.assertEqual(self.make_url('/member/signup/'), self.browser.current_url)

    def test_logged_in_user_redirect_to_post(self):
        self.make_user_and_login()

        # 이후 다시 root url로 요청
        self.browser.get(self.live_server_url)
        self.assertEqual(self.make_url('/post/'), self.browser.current_url)


class ProfilTest(BaseTestCase):
    """
    프로필 페이지에서의 동작을 테스트 한다.
    """

    def access_profile_page_and_check_status(self, status_name, unit, num):
        self.browser.get(self.make_url('/member/profile/'))
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('{status_name} {num}{unit}'.format(
            status_name=status_name,
            num=num,
            unit=unit
        ),
            page_text
        )

    def test_profile_display_status_post_count(self):
        user = self.make_user_and_login()
        num = random.randrange(1, 10)
        for i in range(num):
            Post.objects.create(
                author=user,
            )
        self.access_profile_page_and_check_status(
            status_name='게시물',
            unit='개',
            num=num
        )

    def test_profile_display_status_follower_count(self):
        user = self.make_user_and_login()
        users = make_dummy_users()
        num = random.randrange(1, 10)
        for i in range(num):
            users[i].follow(user)

        self.access_profile_page_and_check_status(
            status_name='팔로워',
            unit='명',
            num=num
        )

    def test_profile_display_status_following_count(self):
        user = self.make_user_and_login()
        users = make_dummy_users()
        num = random.randrange(1, 10)
        for i in range(num):
            user.follow(users[i])

        self.access_profile_page_and_check_status(
            status_name='팔로우',
            unit='명',
            num=num
        )


class LoginRequiredTest(BaseTestCase):
    def logout_user_redirect_to_where(self, where):
        test_url = where
        self.browser.get(self.make_url(test_url))
        return self.assertEqual(
            '{}/member/login/?next={}'.format(self.live_server_url, test_url),
            self.browser.current_url
        )

    def login_user_redirect_to_where(self, where):
        test_url = where
        self.make_user_and_login()
        self.browser.get(self.make_url(test_url))
        return self.assertEqual(self.make_url(test_url), self.browser.current_url)

    def test_profile_logout_user(self):
        return self.logout_user_redirect_to_where('/member/profile/')

    def test_profile_login_user(self):
        return self.login_user_redirect_to_where('/member/profile/')

    def test_change_profile_logout_user(self):
        return self.logout_user_redirect_to_where('/member/profile/image/')

    def test_change_profile_login_user(self):
        return self.login_user_redirect_to_where('/member/profile/image/')

    def test_post_list_logout_user(self):
        return self.logout_user_redirect_to_where('/post/')

    def test_post_list_login_user(self):
        return self.login_user_redirect_to_where('/post/')

    def test_post_add_logout_user(self):
        return self.logout_user_redirect_to_where('/post/add/')

    def test_post_add_login_user(self):
        return self.login_user_redirect_to_where('/post/add/')

    def test_post_detail_logout_user(self):
        return self.logout_user_redirect_to_where('/post/100/')

    def test_post_detail_login_user(self):
        return self.login_user_redirect_to_where('/post/100/')
