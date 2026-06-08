from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError


class UserCRUDTest(TestCase):
	def _create_user(self, **kwargs):
		User = get_user_model()
		data = dict(
			email="user@example.com",
			chat_id="chat123",
		)
		data.update(kwargs)
		user = User.objects.create(**data)
		user.set_password(data.get("password", "pass"))
		user.save()
		return user

	def test_create_user(self):
		u = self._create_user()
		self.assertIsNotNone(u.pk)
		self.assertEqual(str(u), u.email)
		self.assertEqual(u.chat_id, "chat123")

	def test_read_user(self):
		u = self._create_user(email="reader@example.com")
		fetched = get_user_model().objects.get(pk=u.pk)
		self.assertEqual(fetched.email, "reader@example.com")

	def test_update_user(self):
		u = self._create_user(email="updater@example.com")
		u.full_name = "New Name"
		u.phone_number = "+70001112233"
		u.save()

		refreshed = get_user_model().objects.get(pk=u.pk)
		self.assertEqual(refreshed.full_name, "New Name")
		self.assertEqual(refreshed.phone_number, "+70001112233")

	def test_delete_user(self):
		u = self._create_user(email="deleteme@example.com")
		pk = u.pk
		u.delete()
		self.assertFalse(get_user_model().objects.filter(pk=pk).exists())

	def test_unique_email_constraint(self):
		self._create_user(email="unique@example.com")
		with self.assertRaises(IntegrityError):
			self._create_user(email="unique@example.com")

