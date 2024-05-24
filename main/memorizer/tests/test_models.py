from django.test import TestCase
from django.contrib.auth.models import User
from memorizer.models import Memo


class MemoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username="some vk_id",
            first_name="first_name",
            last_name="last_name"
        )
        Memo.objects.create(user=user, name="testMemoName", text="testMemoText", position_x=0.0, position_y=0.0)

    def test_filter(self):
        user = User.objects.get(id=1)
        memos_exists = Memo.objects.filter(user=user).exists()
        self.assertEqual(memos_exists, True)

    def test_memo_user(self):
        memo = Memo.objects.get(id=1)
        memo_user = memo.user
        user = User.objects.get(id=1)
        self.assertEqual(memo_user, user)

    def test_memo_name(self):
        memo = Memo.objects.get(id=1)
        self.assertEqual(memo.name, "testMemoName")

    def test_memo_text(self):
        memo = Memo.objects.get(id=1)
        self.assertEqual(memo.text, "testMemoText")

    def test_memo_position_x(self):
        memo = Memo.objects.get(id=1)
        self.assertEqual(memo.position_x, 0.0)

    def test_memo_position_y(self):
        memo = Memo.objects.get(id=1)
        self.assertEqual(memo.position_y, 0.0)
