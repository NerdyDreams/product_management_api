from django.shortcuts import render, get_object_or_404

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'  # Default lookup by ID

    @action(detail=False, methods=['get'])
    def by_name(self, request):
        name = request.query_params.get('name', None)
        if name is None:
            return Response(
                {"error": "Name parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        product = get_object_or_404(Product, name=name)
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def update_by_name(self, request):
        old_name = request.query_params.get('name', None)
        new_name = request.data.get('name', None)

        if not old_name or not new_name:
            return Response(
                {"error": "Both old name and new name are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(Product, name=old_name)
        product.name = new_name
        try:
            product.save()
            serializer = self.get_serializer(product)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": "Product with this name already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['delete'])
    def delete_by_name(self, request):
        name = request.query_params.get('name', None)
        if name is None:
            return Response(
                {"error": "Name parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        product = get_object_or_404(Product, name=name)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

