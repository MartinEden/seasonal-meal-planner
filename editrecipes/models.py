from django.db import models
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from memoize import mproperty


def months_ago(now, then):
    return now - then if now - then > 0 else now - then + 12


class Month(models.Model):
    month = models.CharField(max_length=10)

    def this_but_not_last(self):
        return set(self.this_months_recipes()) - set(Month.a_months_recipes(
            self.id - 1 if self.id > 1 else 12))

    def this_but_not_next(self):
        return set(self.this_months_recipes()) - set(Month.a_months_recipes(
            self.id + 1 if self.id < 12 else 1))

    @staticmethod
    def a_months_recipes(month_id):
        for r in Recipe.objects.all():
            if not r.always_available() and Month.objects.get(id=month_id) in \
                    r.months_in_season:
                yield r

    def this_months_recipes(self):
        for r in Recipe.objects.all():
            if not r.always_available() and self in r.months_in_season:
                yield r

    def this_months_always_available_peak_recipes(self):
        for r in Recipe.objects.all():
            if r.always_available() and self in r.months_in_peak_season:
                yield r

    def __str__(self):
        return self.month


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class DishType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    seasonal = models.ManyToManyField(Month, related_name="seasonal_month")
    peak = models.ManyToManyField(Month, related_name="peak_month",
                                  blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def in_season(self, month_id):
        return Month.objects.get(id=month_id) in self.seasonal.all()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SideDish(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient)

    def seasonal_ingredients(self, month_id):
        return [i for i in self.ingredients.all() if i.in_season(month_id)]

    def in_season(self, month_id):
        return any(self.seasonal_ingredients(month_id))

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200, blank=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    category = models.ForeignKey('DishType', on_delete=models.CASCADE,
                                 blank=True, null=True, related_name='recipes')
    sidedish = models.ManyToManyField(SideDish, blank=True)

    @mproperty
    def months_in_season(self):
        months = Month.objects.all()
        for i in self.ingredients.all():
            months = months & i.seasonal.all()  # intersection
        return months

    @mproperty
    def months_in_peak_season(self):
        months = Month.objects.all()
        for i in self.ingredients.all():
            months = months & i.seasonal.all()
            if len(i.peak.all()) > 0:
                months = months & i.peak.all()  # intersection
        return months

    def always_available(self):
        if len(self.months_in_season) == 12:
            return True
        else:
            return False

    def clashing_seasonality(self):
        if len(self.months_in_season) == 0:
            return True
        else:
            return False

    def in_season(self, month_id):
        return month_id in [month.id for month in self.months_in_season]

    def length_time_in_season(self):
        return len(self.months_in_season)

    def season_start(self, month_id):
        return months_ago(month_id, self.months_in_season[0].id) if \
            month_id is not None else self.months_in_season[0].id

    def tags(self):
        tags = []
        for i in self.ingredients.all():
            for t in i.tags.all():
                tags.append(t)
        return set(tags)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


# class RecipeIngredientQuantity(models.Model):
#    recipe = models.ForeignKey(Recipe)
#    ingredient = models.ForeignKey(Ingredient)

#    class Meta:
#        unique_together = (('recipe', 'ingredient'))

class RecipesAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple(
            "Ingredient", False)},
    }
