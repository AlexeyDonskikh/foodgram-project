from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import Favorite, Purchase, Subscription
from recipes.models import Ingredient


class CustomModelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return self.Meta.model.objects.create(**validated_data)

    def validate(self, value):
        user = self.context['request'].user
        if user.id == value:
            raise ValidationError('Нельзя подписаться на самого себя')
        return value


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient


class SubscriptionSerializer(CustomModelSerializer):
    class Meta:
        fields = ('author', )
        model = Subscription


class FavoriteSerializer(CustomModelSerializer):
    class Meta:
        fields = ('recipe', )
        model = Favorite


class PurchaseSerializer(CustomModelSerializer):
    class Meta:
        fields = ('recipe', )
        model = Purchase
