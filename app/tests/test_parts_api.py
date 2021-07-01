from django.urls import reverse
import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

URL = reverse('part:data-list')


class PublicPartsApiTests(TestCase):
	"""Test the publicly available API"""

	def setUp(self):
		self.client = APIClient()

	def test_login_required(self):
		"""Test that login is required for retrieving parts"""
		res = self.client.get(URL)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

