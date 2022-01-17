from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('lft', 'rght', 'tree_id',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    products = serializers.SlugRelatedField(many=True, read_only=True, slug_field='id')
    scopes = serializers.SerializerMethodField(method_name="get_scopes", read_only=True)
    diameters = serializers.SerializerMethodField(method_name="get_diameters", read_only=True)
    lengths = serializers.SerializerMethodField(method_name="get_lengths", read_only=True)
    colors = serializers.SerializerMethodField(method_name="get_colors", read_only=True)
    pictures = serializers.SerializerMethodField(method_name="get_pictures", read_only=True)

    class Meta:
        model = Category
        exclude = ('lft', 'rght', 'tree_id', 'level', 'parent',)

    @classmethod
    def get_function_for_card(cls, obj, value):
        """ Метод для избежания дублирования кода """

        result = set()
        for product in obj.products.values(value):
            result.add(product[value])
        return result

    def get_scopes(self, obj):
        return self.get_function_for_card(obj, 'scope')

    def get_diameters(self, obj):
        return self.get_function_for_card(obj, 'diameter')

    def get_lengths(self, obj):
        return self.get_function_for_card(obj, 'length')

    def get_colors(self, obj):
        return self.get_function_for_card(obj, 'color')

    def get_pictures(self, obj):
        """ Метод для получения списка изображений по цветам без повторения цвета """

        result, colors = set(), self.get_colors(obj)
        for product in obj.products.values():
            if product['color'] in colors:
                result.add(product['picture'])
            colors.discard(product['color'])
        return result
