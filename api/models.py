from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Favorite(models.Model):
    """
    Stores a favorite relation between `auth.User` and `recipes.Recipe`.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favored_by',
        verbose_name='Рецепт в избранном',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite',
            )
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class Subscription(models.Model):
    """
    Stores a subscription relation between two `auth.User`.
    User is subscribed to author.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписался на',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписчик',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribes')]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Purchase(models.Model):
    """
    Stores a purchase relation between `auth.User` and `recipes.Recipe`.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='автор',
        related_name='purchases')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='рецепт',
        related_name='purchases')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_purchases')]
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'
