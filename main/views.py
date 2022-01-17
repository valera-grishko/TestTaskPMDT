from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, CardSerializer


class ShowCategories(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter().order_by('level')


class ShowCards(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        category = Category.objects.filter(id=self.kwargs['pk'])
        cards = category.get_descendants()
        return cards.filter(level=3)


class ShowCardDetail(generics.ListAPIView):
    serializer_class = CardSerializer

    def get_queryset(self):
        return Category.objects.filter(id=self.kwargs['pk'], level=3)


class ShowProducts(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        card = Category.objects.get(id=self.kwargs['pk'], level=3)
        return Product.objects.filter(card=card)
