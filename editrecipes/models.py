from datetime import timedelta

from django.db import models
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models.functions import Lower
from memoize import mproperty


def months_ago(now, then):
    return now - then if now - then > 0 else now - then + 12


class Month(models.Model):
    month = models.CharField(max_length=10)

    def previous(self):
        id = (self.id - 1) % 12
        id = id if id != 0 else 12
        return Month.objects.get(id=id)

    def next(self):
        id = (self.id + 1) % 12
        id = id if id != 0 else 12
        return Month.objects.get(id=id)

    def shortname(self):
        return self.month[0:3]

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


class Aisle(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return "%s - %s" % (self.number, self.name)

    class Meta:
        ordering = ['number']


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    seasonal = models.ManyToManyField(Month, related_name="seasonal_month")
    peak = models.ManyToManyField(Month, related_name="peak_month",
                                  blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    aisle = models.ForeignKey(Aisle, on_delete=models.DO_NOTHING, null=True)

    def in_season(self, month_id):
        return self.seasonal.filter(id=month_id)

    class Meta:
        ordering = [Lower("name")]

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
    conversion_factor = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "1%s = %s%s" % (self.from_unit, self.conversion_factor, self.to_unit)


class SideDish(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient)

    def seasonal_ingredients(self, month_id):
        return [i for i in self.ingredients.all() if i.in_season(month_id)]

    def in_season(self, month_id):
        return any(self.seasonal_ingredients(month_id))

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=200, blank=True)
    ingredients = models.ManyToManyField(Ingredient,
                                         through="IngredientQuantity",
                                         related_name='recipes')
    course = models.ManyToManyField(Course, related_name='courses'),
    category = models.ForeignKey('DishType', on_delete=models.CASCADE,
                                 blank=True, null=True, related_name='recipes')
    sidedish = models.ManyToManyField(SideDish, blank=True)
    feeds = models.IntegerField()
    time = models.DurationField()
    can_be_made_in_advance = models.BooleanField(default=False)

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
        ordering = [Lower("name")]


class IngredientQuantity(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING,
                               related_name='ingredient_quantities')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    unit = models.ForeignKey(Unit,
                             default=0,
                             on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Quantity of ingredient"

    def rounded_amount(self):
        if self.amount - int(self.amount) > 0:
            return self.amount
        return int(self.amount)

    def __str__(self):
        return "%s %s" % (self.quantity(), self.ingredient)

    def quantity(self):
        if self.unit.name != "item":
            return "%s%s" % (self.rounded_amount(), self.unit)
        else:
            return "%s" % (self.rounded_amount())


class Recent(models.Model):
    meal = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return "%s: %s" % (self.date, self.meal)

    def get_meals_since(date):
        recent_meals = Recent.objects.filter(date__gte=date)
        #print(recent_meals)
        return recent_meals


class Guest(models.Model):
    name = models.CharField(max_length=100)
    problem_tags = models.ManyToManyField(Tag, blank=True,
                                          related_name="guest_for_whom_problematic")
    problem_ingredients = models.ManyToManyField(Ingredient, blank=True,
                                                 related_name="guest_for_whom_problematic")

    def __str__(self):
        return self.name


# class RecipeIngredientQuantity(models.Model):
#    recipe = models.ForeignKey(Recipe)
#    ingredient = models.ForeignKey(Ingredient)

#    class Meta:
#        unique_together = (('recipe', 'ingredient'))


class IngredientQuantityInline(admin.TabularInline):
    model = IngredientQuantity
    extra = 0


class RecipesAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple(
            "Ingredient", False)},
    }
    inlines = (IngredientQuantityInline,)
    list_display = ("name", "category", "feeds", "time", "can_be_made_in_advance")
    list_editable = ("category", "feeds", "time", "can_be_made_in_advance")