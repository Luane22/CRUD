from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Company, Doc, User
from .serializers import CompanySerializer, DocSerializer, UserSerializer
import json
from datetime import datetime, timedelta


class CompanyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company1 = Company.objects.create(
            name='Company 1',
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self.company2 = Company.objects.create(
            name='Company 2',
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self.valid_payload = {
            'name': 'New Company',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'timezone': '-03:00',
            'language': 'pt',
            'invited_users': [],
            'created_by': None,
            'documents': []
        }
        self.invalid_payload = {
            'name': '',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'timezone': '-03:00',
            'language': 'pt',
            'invited_users': [],
            'created_by': None,
            'documents': []
        }

    def test_get_all_companies(self):
        response = self.client.get(reverse('company-list'))
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_company(self):
        response = self.client.get(
            reverse('company-detail', kwargs={'pk': self.company1.pk}))
        company = Company.objects.get(pk=self.company1.pk)
        serializer = CompanySerializer(company)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_company(self):
        response = self.client.get(
            reverse('company-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_company(self):
        response = self.client.post(
            reverse('company-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_company(self):
        response = self.client.post
