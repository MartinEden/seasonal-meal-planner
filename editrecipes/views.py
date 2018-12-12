from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import get_object_or_404, render

from editrecipes.helpers import get_month, MonthRecipes
from editrecipes.viewmodels import RecipeWithSeasonality
from .models import Recipe, Month, Tag, DishType, SideDish, Ingredient, IngredientQuantity


def index(request):
    return month(request)


def recipe(request, name, month_id=None):
    recipe = get_object_or_404(Recipe, name__exact=name)
    this_month = get_month(month_id)
    dishes = {}
    for dish in recipe.sidedish.all():
        dishes[dish] = dish.seasonal_ingredients(this_month.id)
    val = URLValidator()
    try:
        val(recipe.url)
        valid_url = True
    except ValidationError:
        valid_url = False

    data = {
        'recipe': recipe,
        'months': Month.objects.all(),
        'this_month': this_month,
        'dishes': dishes,
        'valid_url': valid_url
    }
    return render(request, 'editrecipes/recipe.html', data)


def year_chart(request):
    data = {
        'recipes': Recipe.objects.all()
                                 .prefetch_related('ingredients__peak')
                                 .prefetch_related('ingredients__seasonal'),
        'months': Month.objects.all(),
        'this_month': get_month()
    }
    return render(request, 'editrecipes/year-chart.html', data)


def tag_chart(request):
    data = {
        'recipes': Recipe.objects.all().prefetch_related('ingredients__tags'),
        'tags': Tag.objects.all()
    }
    return render(request, 'editrecipes/tag-chart.html', data)


def month(request, month_id=None):
    recipes = MonthRecipes(month_id)
    always_available_recipes = recipes.evergreen_recipes_that_peak_this_month()
    clashing_season_recipes = [r for r in recipes.all if
                               r.clashing_seasonality()]
    context = {
        'always_available_recipes': always_available_recipes,
        'clashing_season_recipes': clashing_season_recipes,
        'seasonal_recipes': recipes.seasonal_recipes()
    }
    return render(request, 'editrecipes/index.html', context)


def category(request, category=None):
    if category is None:
        return render(request, 'editrecipes/categories.html',
                      {'categories': DishType.objects.all()})
    else:
        dishtype = get_object_or_404(DishType, name__exact=category)
        return render(request, 'editrecipes/category.html',
                      {'category': dishtype})


def sidedish(request, sidedish=None, month_id=None):
    if sidedish is None:
        return render(request, 'editrecipes/sidedishes.html',
                      {'sidedishes': SideDish.objects.all()})
    else:
        sidedish = get_object_or_404(SideDish, name__exact=sidedish)
        month = get_month(month_id)
        return render(request, 'editrecipes/sidedish.html',
                      {'sidedish': sidedish,
                       'seasonal': sidedish.seasonal_ingredients(month.id),
                       'months': Month.objects.all(),
                       'this_month': month})


def select_recipes(request, month_id=None):
    month = get_month(month_id)
    recipes = sorted(Recipe.objects.all(), key=lambda x: (-x.in_season(
        month.id), x.length_time_in_season(), x.season_start(month_id)))
    context = {
        'recipes': recipes,
        'months': Month.objects.all(),
        'this_month': month,
        'tags': Tag.objects.all()
    }
    return render(request, 'editrecipes/select-recipes.html', context)


def shopping_list(request):
    recipe_ids = request.GET.getlist('recipes')
    recipes = Recipe.objects.filter(pk__in=recipe_ids)
    ingredients = {}
    for recipe in recipes:
        for i in recipe.ingredient_quantities.all():
            if not i.ingredient.name in ingredients.keys():
                ingredients[i.ingredient.name] = []
            ingredients[i.ingredient.name] += [i]

    context = {"ingredients": ingredients}
    return render(request, 'editrecipes/shopping-list.html', context)


def search(request):
    if 'ingredient' in request.GET:
        search = request.GET['ingredient']
        ingredients = [i for i in Ingredient.objects.all() if search in i.name]
        recipes = {i: i.recipes.all() for i in ingredients}
        for i, r in recipes.items():
            print(i)
            for rec in r:
                print(rec)
        return render(request, 'editrecipes/search.html',
                      {'recipes': recipes,
                       'ingredient': search,
                       'ingredients': ingredients})
    else:
        return render(request, 'editrecipes/search.html', {})


def ingredients(request, month_id=None):
    month = get_month(month_id)
    return render(request, 'editrecipes/ingredients.html',
                  {'this_month': month,
                   'ingredients': Ingredient.objects.all(),
                   'months': Month.objects.all()
                   })
