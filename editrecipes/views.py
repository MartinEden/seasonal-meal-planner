from django.shortcuts import get_object_or_404, render, redirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .models import Recipe, Month, Tag, DishType, SideDish, Ingredient
import datetime


def get_month(month_id):
    if month_id is not None:
        return Month.objects.get(id=month_id)
    else:
        this_month = datetime.datetime.now().strftime("%B")
        return Month.objects.get(month=this_month)


def index(request):
    return month(request)

def recipe(request, name, month_id=None):
    recipe = get_object_or_404(Recipe, name__exact=name)
    this_month = get_month(month_id)
    dishes = {}
    for dish in recipe.sidedish.all():
        dishes[dish] = dish.seasonal_ingredients(this_month.id)
    val  = URLValidator()
    try:
        val(recipe.url)
        valid_url = True
    except ValidationError:
        valid_url = False
    return render(request, 'editrecipes/recipe.html', {'recipe': recipe,
                                                       'months':
                                                           Month.objects.all(),
                                                       'this_month':this_month,
                                                        'dishes':dishes,
                                                       'valid_url':valid_url})

def grid(request):
    return render(request, 'editrecipes/recipe-month.html',
                  {'recipes':Recipe.objects.all(),
                   'months': Month.objects.all()})

def month(request, month_id = None):
    month = get_month(month_id)
    seasonal_recipes = month.this_months_recipes()
    recipes = sorted(Recipe.objects.all(), key=lambda x: (-x.in_season(
        month.id), x.length_time_in_season(), x.season_start(month_id)))
    just_in = month.this_but_not_last()
    last_chance = month.this_but_not_next()
    other_seasonal = sorted(set(seasonal_recipes) - set(just_in) - set(
        last_chance), key=lambda x: x.length_time_in_season() )
    always_available_recipes = month.this_months_always_available_peak_recipes()
    clashing_season_recipes = [r for r in recipes if r.clashing_seasonality()]
    context = {
        'recipes': recipes,
        'always_available_recipes': always_available_recipes,
        'seasonal_recipes': seasonal_recipes,
        'clashing_season_recipes': clashing_season_recipes,
        'just_in':just_in,
        'last_chance':last_chance,
        'other_seasonal':other_seasonal,
         'months': Month.objects.all(),
        'this_month': month,
        'tags': Tag.objects.all()
    }

    return render(request, 'editrecipes/index.html', context)


def category(request, category=None):
    if category is None:
        return render(request, 'editrecipes/categories.html',
                      {'categories':DishType.objects.all()})
    else:
        dishtype = get_object_or_404(DishType, name__exact=category)
        return render(request, 'editrecipes/category.html',
                      {'category':dishtype})

def sidedish(request, sidedish=None, month_id = None):
    if sidedish is None:
        return render(request, 'editrecipes/sidedishes.html',
                      {'sidedishes':SideDish.objects.all()})
    else:
        sidedish = get_object_or_404(SideDish, name__exact=sidedish)
        month = get_month(month_id)
        return render(request, 'editrecipes/sidedish.html',
                      {'sidedish':sidedish,
                       'seasonal':sidedish.seasonal_ingredients(month.id),
                       'months':Month.objects.all(),
                       'this_month':month})

def select_recipes(request, month_id = None):
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
    ingredients = []
    for recipe in recipes:
        ingredients.extend(recipe.ingredients.all())
    ingredients = set(ingredients)
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
                      {'recipes':recipes,
                       'ingredient':search,
                       'ingredients': ingredients})
    else:
        return render(request, 'editrecipes/search.html', {})

def ingredients(request, month_id = None):
    month = get_month(month_id)
    return render(request, 'editrecipes/ingredients.html',
                  {'this_month':month,
                   'ingredients':Ingredient.objects.all(),
                   'months':Month.objects.all()
                   })