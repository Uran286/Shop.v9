from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Category, Choosen


User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Product


class CategoryApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id', 'title',
        )

    """
    Representation to category like with 
    parent category and children category 
    """

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.children.exists():
            representation['children'] = CategoryApiSerializer(
                instance.children.all(), many=True
            ).data
        return representation


class ChoosenAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Choosen
        fields = ('product', 'user')




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')