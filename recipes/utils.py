from decimal import Decimal

import pdfkit
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from foodgram.settings import PDF_OPTIONS
from recipes.models import Ingredient, Recipe, RecipeIngredient


def get_recipes(request, tags):
    if tags:
        recipe_list = Recipe.objects.filter(
            favored_by__user=request.user).prefetch_related(
            'author', 'tags').filter(
            tags__slug__in=tags).distinct()
    else:
        recipe_list = Recipe.objects.filter(favored_by__user=request.user)
    return recipe_list


def get_ingredients(request):
    """
    Parse POST request body for ingredient names and their respective amounts.
    """
    ingredients = {}
    for key, name in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = request.POST[
                f'valueIngredient_{num}'
            ]

    return ingredients


def save_recipe(request, form):
    """
    Create and save a Recipe instance with neccessary m2m relationships.
    """
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            objs = []
            ingredients = get_ingredients(request)
            for name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=name)
                objs.append(
                    RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=Decimal(quantity.replace(',', '.'))
                    )
                )
            RecipeIngredient.objects.bulk_create(objs)

            form.save_m2m()
            return recipe
    except IntegrityError:
        raise HttpResponseBadRequest


def edit_recipe(request, form, instance):
    """
    A wrapper function for save_recipe to allow editing.
    """
    try:
        with transaction.atomic():
            RecipeIngredient.objects.filter(recipe=instance).delete()
            return save_recipe(request, form)
    except IntegrityError:
        raise HttpResponseBadRequest


def generate_pdf(template_name, context):
    """
    Generate a PDF file from Django template.
    """
    html = get_template(template_name).render(context)
    return pdfkit.from_string(html, False, options=PDF_OPTIONS)
