import io

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

from foodgram.settings import TAGS
from recipes.forms import RecipeForm
from recipes.models import Recipe
from recipes.utils import edit_recipe, generate_pdf, get_recipes, save_recipe

User = get_user_model()


def index(request):
    """
    Display most recent `recipes.Recipe`, fitered with tags, 6 per page.
    """
    tags = request.GET.getlist('tag', TAGS)

    recipes = Recipe.objects.filter(
        tags__title__in=tags
    ).select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).distinct()

    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/index.html',
        {
            'page': page,
            'paginator': paginator,
        }
    )


def recipe_view_redirect(request, recipe_id):
    """
    Redirect to the `recipe_view_slug` page.
    """
    recipe = get_object_or_404(Recipe.objects.all(), id=recipe_id)

    return redirect('recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug)


def recipe_view_slug(request, recipe_id, slug):
    """
    Display a single `recipes.Recipe`.
    """
    recipe = get_object_or_404(
        Recipe.objects.select_related('author'),
        id=recipe_id,
        slug=slug
    )

    return render(request, 'recipes/singlePage.html', {'recipe': recipe})


@login_required
def recipe_new(request):
    """
    GET: Display a form for a new `recipes.Recipe`.
    POST: Validate and save the form to database.
    On successful save redirect to `recipe_view_slug` page
    of created `recipes.Recipe`.
    Otherwise stay on page and show validation errors.
    """
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = save_recipe(request, form)

        return redirect(
            'recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug
        )

    return render(request, 'recipes/formRecipe.html', {'form': form})


@login_required
def recipe_edit(request, recipe_id, slug):
    """
    GET: Display a form for editing of existing `recipes.Recipe`.
    POST: Validate and save the form to database.
    On successful save redirect to `recipe_view_slug` page
    of created `recipes.Recipe`.
    Otherwise stay on page and show validation errors.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if not request.user.is_superuser:
        if request.user != recipe.author:
            return redirect(
                'recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug
            )

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        edit_recipe(request, form, instance=recipe)
        return redirect(
            'recipe_view_slug', recipe_id=recipe.id, slug=recipe.slug
        )

    return render(
        request,
        'recipes/formRecipe.html',
        {'form': form, 'recipe': recipe}
    )


@login_required
def recipe_delete(request, recipe_id, slug):
    """
    Delete the given `recipes.Recipe`.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.is_superuser or request.user == recipe.author:
        recipe.delete()
    return redirect('index')


def profile_view(request, username):
    """
    Display all `recipes.Recipe` of a given `auth.User`, filtered with tags
    """
    author = get_object_or_404(User, username=username)
    tags = request.GET.getlist('tag', TAGS)
    author_recipes = author.recipes.filter(
        tags__title__in=tags
    ).prefetch_related('tags').distinct()

    paginator = Paginator(author_recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/authorRecipe.html',
        {
            'author': author,
            'page': page,
            'paginator': paginator,
        }
    )


@login_required
def subscriptions(request):
    """
    Display all `auth.User` the visitor is subscribed to,
    each with their 3 most recent `recipes.Recipe`, 6 per page.
    """
    authors = User.objects.filter(
        following__user=request.user
    ).prefetch_related(
        'recipes'
    ).annotate(recipe_count=Count('recipes')).order_by('username')

    paginator = Paginator(authors, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/myFollow.html',
        {
            'page': page,
            'paginator': paginator,
        }
    )


@login_required
def favorites(request):
    """
    Display all `recipes.Recipe` that visitor had marked as favorite,
    filtered with tags
    """
    tags = request.GET.getlist('tag')

    recipes = get_recipes(request, tags)

    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'recipes/favorite.html',
        {
            'page': page,
            'paginator': paginator,
        }
    )


@login_required
def purchases(request):
    """
    Display all `recipes.Recipe` the visitor had put in their shoplist.
    """
    recipes = request.user.purchases.all()
    return render(
        request,
        'recipes/shopList.html',
        {'recipes': recipes},
    )


@login_required
def purchases_download(request):
    """
    Download a list of `recipes.Ingredient` from shoplist as a PDF document.
    """
    ingredients = request.user.purchases.select_related(
        'recipe'
    ).order_by(
        'recipe__ingredients__title'
    ).values(
        'recipe__ingredients__title', 'recipe__ingredients__dimension'
    ).annotate(amount=Sum('recipe__recipe_ingredients__quantity')).all()

    pdf = generate_pdf(
        'misc/shopListPDF.html', {'ingredients': ingredients}
    )

    return FileResponse(
        io.BytesIO(pdf),
        filename='ingredients.pdf',
        as_attachment=True
    )
