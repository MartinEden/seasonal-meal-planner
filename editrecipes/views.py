from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
import json

from editrecipes.helpers import get_month, MonthRecipes
from editrecipes.viewmodels import RecipeWithSeasonality
from .models import Recipe, Month, Tag, DishType, SideDish, Ingredient, \
    IngredientQuantity, Aisle, Guest


def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return
    else:
        form = loginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def index(request):
    return month(request)


@login_required
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


@login_required
def year_chart(request):
    data = {
        'recipes': Recipe.objects.all()
                                 .prefetch_related('ingredients__peak')
                                 .prefetch_related('ingredients__seasonal'),
        'months': Month.objects.all(),
        'this_month': get_month()
    }
    return render(request, 'editrecipes/year-chart.html', data)


@login_required
def tag_chart(request):
    data = {
        'recipes': Recipe.objects.all().prefetch_related('ingredients__tags'),
        'tags': Tag.objects.all()
    }
    return render(request, 'editrecipes/tag-chart.html', data)


@login_required
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


@login_required
def category(request, category=None):
    if category is None:
        return render(request, 'editrecipes/categories.html',
                      {'categories': DishType.objects.all()})
    else:
        dishtype = get_object_or_404(DishType, name__exact=category)
        return render(request, 'editrecipes/category.html',
                      {'category': dishtype})


@login_required
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


@login_required
def select_recipes(request, month_id=None):
    month = get_month(month_id)
    filter_tags = request.GET.getlist('tags')
    recipes = sorted(Recipe.objects.all(), key=lambda x: (-x.in_season(
        month.id), x.length_time_in_season(), x.season_start(month_id)))
    tags = {}
    for tag in Tag.objects.all():
        tags[tag] = tag.name in filter_tags
    guests = Guest.objects.all()
    context = {
        'recipes': recipes,
        'months': Month.objects.all(),
        'this_month': month,
        'tags': tags,
        'guests':guests,
    }
    return render(request, 'editrecipes/select-recipes.html', context)


@login_required
def shopping_list(request):
    recipe_ids = request.GET.getlist('recipes')
    recipes = Recipe.objects.filter(pk__in=recipe_ids)
    ingredients = {}
    for recipe in recipes:
        for i in recipe.ingredient_quantities.all():
            if not i.ingredient in ingredients.keys():
                ingredients[i.ingredient] = []
            ingredients[i.ingredient] += [i]

    if any(i for i in ingredients if i.aisle is None):
        return redirect("sort_into_aisles")

    items = sorted(ingredients.items(), key=lambda x: x[0].aisle.number)

    context = {"ingredients": items}
    print(context["ingredients"])
    return render(request, 'editrecipes/shopping-list.html', context)


@login_required
def plan_week(request):
    ingredients = [i.name for i in Ingredient.objects.all()]
    tags = [t.name for t in Tag.objects.all()]
    return render(request, 'editrecipes/plan-week.html', {"tags": tags, "ingredients": ingredients})


@login_required
def sort_into_aisles(request, aisle=None):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.isdigit() and value.isdigit():
                i = Ingredient.objects.get(id=key)
                i.aisle = Aisle.objects.get(number=value)
                i.save()
    if aisle=="all":
        ingredients = Ingredient.objects.all()
    elif aisle is not None:
        ingredients = Ingredient.objects.filter(aisle__name=aisle)
    else:
        ingredients = Ingredient.objects.filter(aisle=None)
    context = {"ingredients": ingredients,
    "aisles":
        Aisle.objects.all(),
               "aisle":aisle}
    return render(request, 'editrecipes/sort-into-aisles.html', context)


@login_required
def search(request):
    all_ingredients = [i.name for i in Ingredient.objects.all()]
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
                       'ingredients': ingredients,
                       'all_ingredients': all_ingredients})
    else:
        return render(request, 'editrecipes/search.html', {"all_ingredients": all_ingredients})


@login_required
def ingredients(request, month_id=None):
    month = get_month(month_id)
    return render(request, 'editrecipes/ingredients.html',
                  {'this_month': month,
                   'ingredients': Ingredient.objects.all(),
                   'months': Month.objects.all()
                   })
