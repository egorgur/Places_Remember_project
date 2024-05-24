import json

from django.test import TestCase
from django.contrib.auth.models import User
from memorizer.models import Memo
from django.urls import reverse
from urllib.parse import urlencode


class MemoViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="some vk_id",
            first_name="first_name",
            last_name="last_name",
            password="123",  # set password only for the tests
        )
        user.save()
        memo = Memo.objects.create(user=user, name="testMemoName", text="testMemoText", position_x=0.0, position_y=0.0)
        memo.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("memorizer:view_memo", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/")

    def test_memo_view(self):
        self.client.login(username="some vk_id", password="123")
        response = self.client.get(reverse("memorizer:view_memo", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, 200)

    def test_memo_data_update(self):
        self.client.login(username="some vk_id", password="123")
        data = urlencode({"name": "testMemoAgainUpdate",
                          "comment": "testCommentUpdate",
                          "position": json.dumps({
                              "x": 1.0,
                              "y": 1.0
                          })})
        response = self.client.post(reverse("memorizer:view_memo", kwargs={"pk": 2}), data,
                                    content_type="application/x-www-form-urlencoded")
        memo = Memo.objects.get(pk=2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(memo.name, "testMemoAgainUpdate")
        self.assertEqual(memo.text, "testCommentUpdate")
        self.assertEqual(memo.position_x, 1.0)
        self.assertEqual(memo.position_y, 1.0)

    def test_memo_deletion(self):
        user = User.objects.get(username="some vk_id")
        self.client.login(username="some vk_id", password="123")
        response = self.client.get(reverse("memorizer:delete_memo", kwargs={"pk": 2}))
        memo_exists = Memo.objects.filter(user=user).exists()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/memorizer/memories")
        self.assertEqual(memo_exists, False)

    def test_memo_creation(self):
        User.objects.get(username="some vk_id")
        self.client.login(username="some vk_id", password="123")
        data = urlencode({"name": "testMemoAgain",
                          "comment": "testComment",
                          "position": {
                              "x": 0.0,
                              "y": 0.0,
                          }})
        response = self.client.post(reverse("memorizer:create_memo"), data,
                                    content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 200)
