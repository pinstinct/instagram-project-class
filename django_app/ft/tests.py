from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from member.models import MyUser


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def make_url(self, url):
        result = '{}{}'.format(self.live_server_url, url)
        return result

    def test_first_visitor_redirect_to_signup(self):
        # 로그인하지 않은 유저가 member:signup으로 잘 이동했는지 확인
        self.browser.get(self.live_server_url)
        self.assertEqual(self.live_server_url + '/member/signup/', self.browser.current_url)

    def test_logged_in_user_redirect_to_post(self):
        # 유저 생성
        test_username = 'test_user'
        test_password = 'test_password'
        MyUser.objects.create_user(test_username, test_password)

        # 유저를 로그인
        self.browser.get(self.make_url('/member/login/'))
        input_username = self.browser.find_element_by_id('id_username')
        input_username.send_keys(test_username)
        input_password = self.browser.find_element_by_id('id_password')
        input_password.send_keys(test_password)
        input_password.send_keys(Keys.ENTER)

        # 이후 다시 root url로 요청
        self.browser.get(self.live_server_url)
        self.assertEqual(self.live_server_url + '/post/', self.browser.current_url)
