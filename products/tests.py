from django.test import TestCase

# Create your tests here.

from rest_framework.test import APIClient
from rest_framework import status
from .models import Product

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_data = {'name': 'Test Product'}
        self.product = Product.objects.create(name='Existing Product')

    def test_create_product(self):
        response = self.client.post('/api/products/', self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(name='Test Product').name, 'Test Product')

    def test_get_product_by_name(self):
        response = self.client.get(f'/api/products/by_name/?name={self.product.name}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_update_product_by_name(self):
        response = self.client.put(
            f'/api/products/update_by_name/?name={self.product.name}',
            {'name': 'Updated Product'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(id=self.product.id).name, 'Updated Product')

    def test_delete_product_by_name(self):
        response = self.client.delete(f'/api/products/delete_by_name/?name={self.product.name}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
