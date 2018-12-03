from django.db import models
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from memoize import mproperty


def months_ago(now, then):
    return now - then if now - then > 0 else now - then + 12


class Month(models.Model):
    month = models.CharField(max_length=10)

    def previous(self):
        return Month.objects.get(id=(self.id - 1) % 12)

    def next(self):
        return Month.objects.get(id=(self.id + 1) % 12)

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
        return self.seasonal.filter(id=month_id)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class UnitConversion(models.Model):
    from_unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING,
                                  related_name='convert_from_unit')
    to_unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING,
                                related_name='convert_to_unit')
    conversion_factor = models.DecimalField(max_digits = 6, decimal_places=2)

class Quantity(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING)

    def __str__(self):
        if self.amount == int(self.amount):
            return "%s %s" % (self.amount, self.unit)
        else:
            return "%s %s" % (int(self.amount), self.unit)

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
    ingredient_quantities = models.ManyToManyField(Ingredient,
                                                  through="IngredientQuantity",
                                                  related_name='recipes_with_quantities')
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

class IngredientQuantity(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    quantity = models.ForeignKey(Quantity, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Quantity of ingredient"

    def __str__(self):
        if self.quantity.unit != "item":
            return "%s %s" % (self.quantity, self.ingredient)
        else:
            return "%s %s" % (int(self.quantity.amount), self.ingredient)

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
