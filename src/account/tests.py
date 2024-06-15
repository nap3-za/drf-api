import datetime

from random import randint

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import Group
from django.db import transaction

from rest_framework import status
from rest_framework.test import APITestCase 

from .models import Account


class AccountTests(APITestCase):

	@classmethod
	def setUpTestData(cls):
		account = Account.objects.create_user(
			username="ict",
			name="user_name",
			surname="user_surname",
			gender="MLE",
			email="ict@email.com",
			phone_number="+27123456785",
			password="root.1352",
		)


	def test_account_sign_up(self):
		user_data = {
			"username":"nfx",
			"name":"user_name",
			"surname":"user_surname",
			"gender":"MLE",
			"email": "nfx@email.com",
			"phone_number":"+27123456789",
			"password":"root.1352",
			"password2":"root.1352",
		}

		sign_up_url = reverse("sign-up")
		response = self.client.post(sign_up_url, user_data, format="json")

		# Signing out
		self.client.post(path=reverse("knox_logout"))

		# Necessary Checks
		account = Account.objects.get(username="nfx")

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(account.email, user_data["email"])
		self.assertEqual(account.name, user_data["name"])
		self.assertEqual(account.surname, user_data["surname"])
		self.assertEqual(account.username, user_data["username"])
		self.assertEqual(account.gender, user_data["gender"])
		self.assertEqual(account.phone_number, user_data["phone_number"])


	def test_account_sign_in_out(self):
		data = {
			"username":"ict",
			"password":"root.1352",
		}

		# Signing in
		sign_in_url = reverse("sign-in")
		sign_in_response = self.client.post(sign_in_url, data, format="json")
		self.assertEqual(sign_in_response.status_code, status.HTTP_200_OK)
		self.assertTrue(sign_in_response.data.get("token"))

		# Adding Authorization Token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {sign_in_response.data['token']}")

		# Signing out
		self.client.post(path=reverse("knox_logout"))


	def test_account_update_delete(self):

		# Signing In
		sign_in_data = {
			"username":"ict",
			"password":"root.1352",
		}

		sign_in_url = reverse("sign-in")
		sign_in_response = self.client.post(sign_in_url, sign_in_data, format="json")

		# Adding Authorization Token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {sign_in_response.data['token']}")
		
		# Testing Update
		update_data = {
			"username":"nfx_ict",
			"name":"user_name_u",
			"surname":"user_surname_u",
			"gender":"FML",
			"phone_number":"+27123456780",
			"email": "nfx.ict@email.com",
		}
		account = Account.objects.get(username=sign_in_data["username"])

		update_url = f"{reverse('account:account-list')}{str(account.pk)}/"
		update_response = self.client.put(update_url, update_data, format="json")
		
		account = Account.objects.get(username=update_data["username"])

		self.assertEqual(account.email, update_data["email"])
		self.assertEqual(account.name, update_data["name"])
		self.assertEqual(account.surname, update_data["surname"])
		self.assertEqual(account.username, update_data["username"])
		self.assertEqual(account.gender, update_data["gender"])
		self.assertEqual(account.phone_number, update_data["phone_number"])

		# Testing Delete
		deactivation_url = reverse("account:account-delete")
		deactivation_data = {
			"username":"nfx_ict",
			"password":"root.1352",
		}

		deactivation_response = self.client.post(deactivation_url, deactivation_data, format="json")
		self.assertEqual(deactivation_response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Account.objects.get(email=update_data["email"]).is_active, False)

	def test_account_extras(self):
		pass




