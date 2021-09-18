from rest_framework.reverse import reverse

from tests.base import BaseTest
from db_models.models import UserProfile


class UsersTest(BaseTest):
    """ 用户功能测试类 """

    def setUp(self):
        super(UsersTest, self).setUp()
        self.create_user_url = reverse("users-list")
        self.list_user_url = reverse("users-list")

    def test_create_user(self):
        """ 测试创建用户 """

        self.login()

        # 已存在用户名 -> 无法创建
        resp = self.post(self.create_user_url, {
            "username": self.username,
            "password": self.password,
            "re_password": self.password,
            "email": self.email,
        }).json()
        self.assertDictEqual(resp, {
            'code': 1,
            'message': 'username: 用户名已存在;',
            'data': None
        })

        # 两次密码不一致 -> 无法创建
        resp = self.post(self.create_user_url, {
            "username": "new_user",
            "password": "new_password",
            "re_password": "diff_password",
            "email": "user@cloudwise.com",
        }).json()
        self.assertDictEqual(resp, {
            "code": 1,
            "message": "re_password: 两次密码不一致;",
            "data": None
        })

        # 邮箱格式不正确 -> 无法创建
        resp = self.post(self.create_user_url, {
            "username": "new_user",
            "password": "new_password",
            "re_password": "diff_password",
            "email": "this is a email",
        }).json()
        self.assertDictEqual(resp, {
            "code": 1,
            "message": "email: 邮箱格式不正确;",
            "data": None
        })

        # 全新用户名，两次密码一致 -> 创建成功
        resp = self.post(self.create_user_url, {
            "username": "new_user",
            "password": "new_password",
            "re_password": "new_password",
            "email": "user@cloudwise.com",
        }).json()
        self.assertEqual(resp.get("code"), 0)
        self.assertEqual(resp.get("message"), "success")
        self.assertTrue(resp.get("data", None) is not None)

        self.logout()

    def test_list_user(self):
        """ 测试查询用户列表 """

        self.login()

        # 查询用户列表 -> 查询成功
        resp = self.get(self.create_user_url).json()
        self.assertEqual(resp.get("code"), 0)
        self.assertEqual(resp.get("message"), "success")
        self.assertTrue(resp.get("data", None) is not None)

        self.logout()

    def test_retrieve_user(self):
        """ 测试查询一个用户 """

        self.login()

        # 创建用户
        username = "retrieve_user"
        password = "retrieve_user"
        email = "retrieve_user@cloudwise.com"
        user = UserProfile.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

        # 查询不存在用户 -> 查询失败
        resp = self.get(reverse("users-detail", [99])).json()
        self.assertDictEqual(resp, {
            'code': 1,
            'message': 'Not found.',
            'data': None
        })

        # 查询存在用户 -> 查询成功
        resp = self.get(reverse("users-detail", [user.id])).json()
        user_info = resp.get("data", None)
        self.assertEqual(resp.get("code"), 0)
        self.assertEqual(resp.get("message"), "success")
        self.assertTrue(user_info is not None)
        self.assertEqual(user_info.get("username"), username)
        self.assertEqual(user_info.get("email"), email)
        self.assertNotEqual(user_info.get("password"), password)

        self.logout()

    def test_update_user(self):
        """ 测试更新一个已有用户 """

        self.login()

        # 创建用户
        username = "update_user"
        password = "update_user"
        email = "update_user@cloudwise.com"
        user = UserProfile.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

        # 更新不存在用户 -> 更新失败
        resp = self.put(reverse("users-detail", [99]), {
            "username": username,
            "password": "update_user_pass",
            "re_password": "update_user_pass",
            "email": "update_user@cloudwise.com",
        }).json()
        self.assertDictEqual(resp, {
            'code': 1,
            'message': 'Not found.',
            'data': None
        })

        # 更新已有用户 -> 密码不一致
        resp = self.put(reverse("users-detail", [user.id]), {
            "username": username,
            "password": "update_user_pass",
            "re_password": "update_user_pass_diff",
            "email": "update_user@cloudwise.com",
        }).json()
        self.assertDictEqual(resp, {
            "code": 1,
            "message": "re_password: 两次密码不一致;",
            "data": None
        })

        # 更新已有用户，两次密码一致 -> 更新成功
        new_email = "update_user_email@cloudwise.com"
        resp = self.put(reverse("users-detail", [user.id]), {
            "username": username,
            "password": "update_user_pass",
            "re_password": "update_user_pass",
            "email": new_email,
        }).json()
        self.assertEqual(resp.get("code"), 0)
        self.assertEqual(resp.get("message"), "success")
        self.assertTrue(resp.get("data", None) is not None)

    def test_partial_update_user(self):
        """ 测试更新一个现有用户的一个或多个字段 """

        # 创建用户
        username = "partial_update_user"
        password = "partial_update_user"
        email = "partial_update_user@cloudwise.com"
        user = UserProfile.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

        self.login()

        # 更新不存在用户 -> 更新失败
        resp = self.patch(reverse("users-detail", [99]), {
            "password": "partial_update_user_pass",
            "re_password": "partial_update_user_pass",
            "email": "partial_update_user_email@cloudwise.com",
        }).json()
        self.assertDictEqual(resp, {
            'code': 1,
            'message': 'Not found.',
            'data': None
        })

        # 更新存在用户 -> 更新成功
        new_email = "partial_update_user_email@cloudwise.com"
        resp = self.patch(reverse("users-detail", [user.id]), {
            "password": "new_password_one",
            "re_password": "new_password_one",
            "email": new_email,
        }).json()
        self.assertEqual(resp.get("code"), 0)
        self.assertEqual(resp.get("message"), "success")
        self.assertTrue(resp.get("data", None) is not None)

        self.logout()

    def test_delete_user(self):
        """ 测试删除一个现有用户 """

        # 创建用户
        username = "delete_user"
        password = "delete_user"
        email = "delete_user@cloudwise.com"
        user = UserProfile.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

        self.login()

        # 删除不存在用户 -> 删除失败
        resp = self.delete(reverse("users-detail", [99])).json()
        self.assertDictEqual(resp, {
            'code': 1,
            'message': 'Not found.',
            'data': None
        })

        self.logout()