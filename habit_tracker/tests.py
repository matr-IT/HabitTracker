from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User
from habit_tracker.models import Habit


class HabitCRUDTests(APITestCase):
	def setUp(self):
		# create two users
		self.u1 = User(email="user1@example.com")
		self.u1.set_password("pass")
		self.u1.save()

		self.u2 = User(email="user2@example.com")
		self.u2.set_password("pass")
		self.u2.save()

		# create habits: one for u1, one for u2 (public), one without owner
		self.h1 = Habit.objects.create(
			owner=self.u1,
			place="дом",
			time="07:00:00",
			action="u1habit",
			periodicity=3,
			time_to_complete=10,
			is_public=False,
		)

		self.h2 = Habit.objects.create(
			owner=self.u2,
			place="дом",
			time="08:00:00",
			action="u2habit",
			periodicity=2,
			time_to_complete=20,
			is_public=True,
		)

		self.h_template = Habit.objects.create(
			owner=None,
			place="парк",
			time="09:00:00",
			action="template",
			periodicity=1,
			time_to_complete=5,
			is_public=True,
		)

		self.client = APIClient()

	def test_list_returns_only_user_habits(self):
		url = reverse("habit_tracker:list")
		# unauthenticated -> 401 or 403 depending on auth config
		r = self.client.get(url)
		self.assertIn(r.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

		# authenticated as u1 -> only h1
		self.client.force_authenticate(user=self.u1)
		r = self.client.get(url)
		self.assertEqual(r.status_code, status.HTTP_200_OK)
		data = r.json()
		# results paginated
		results = data.get("results", data)
		self.assertTrue(any(item["id"] == self.h1.id for item in results))
		self.assertFalse(any(item["id"] == self.h2.id for item in results))

	def test_public_list_accessible_without_auth(self):
		url = reverse("habit_tracker:public-list")
		r = self.client.get(url)
		self.assertEqual(r.status_code, status.HTTP_200_OK)
		data = r.json()
		results = data.get("results", data)
		# should contain public habits (h2 and h_template)
		ids = {item["id"] for item in results}
		self.assertIn(self.h2.id, ids)
		self.assertIn(self.h_template.id, ids)

	def test_create_sets_owner_and_requires_auth(self):
		url = reverse("habit_tracker:create")
		payload = {
			"place": "квартира",
			"time": "10:00:00",
			"action": "new habit",
			"is_pleasant": False,
			"periodicity": 2,
			"time_to_complete": 15,
			"is_public": False,
			# attempt to set owner should be ignored
			"owner": self.u2.id,
		}

		# unauthenticated -> 401 or 403 depending on auth config
		r = self.client.post(url, payload, format="json")
		self.assertIn(r.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

		# authenticated as u1 -> created and owner == u1
		self.client.force_authenticate(user=self.u1)
		r = self.client.post(url, payload, format="json")
		self.assertEqual(r.status_code, status.HTTP_201_CREATED)
		body = r.json()
		self.assertEqual(body.get("owner"), self.u1.id)

	def test_retrieve_update_delete_permissions(self):
		detail_url = lambda pk: reverse("habit_tracker:detail", args=[pk])
		update_url = lambda pk: reverse("habit_tracker:update", args=[pk])
		delete_url = lambda pk: reverse("habit_tracker:delete", args=[pk])

		# authenticate as u1
		self.client.force_authenticate(user=self.u1)

		# retrieve own habit
		r = self.client.get(detail_url(self.h1.id))
		self.assertEqual(r.status_code, status.HTTP_200_OK)

		# cannot retrieve other's habit (should be 404)
		r = self.client.get(detail_url(self.h2.id))
		self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

		# update own habit
		r = self.client.patch(update_url(self.h1.id), {"action": "updated"}, format="json")
		self.assertEqual(r.status_code, status.HTTP_200_OK)
		self.h1.refresh_from_db()
		self.assertEqual(self.h1.action, "updated")

		# cannot update other's habit
		r = self.client.patch(update_url(self.h2.id), {"action": "bad"}, format="json")
		self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

		# delete own habit
		r = self.client.delete(delete_url(self.h1.id))
		self.assertIn(r.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))

		# cannot delete other's habit
		r = self.client.delete(delete_url(self.h2.id))
		self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

