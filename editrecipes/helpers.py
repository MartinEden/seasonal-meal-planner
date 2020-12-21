import datetime

from editrecipes.models import Month, Recipe
from editrecipes.viewmodels import RecipeWithSeasonality


def get_month(month_id=None):
    if month_id is not None:
        return Month.objects.get(id=month_id)
    else:
        this_month = datetime.datetime.now().strftime("%B")
        return Month.objects.get(month=this_month)


class MonthRecipes(object):
    def __init__(self, month_id=get_month().id):
        def sort(r):
            return (-r.in_season(month_id),
                    r.length_time_in_season(),
                    r.season_start(month_id))

        self.month = get_month(month_id)
        all_recipes = Recipe.objects.all() \
                                    .select_related('category') \
                                    .prefetch_related('ingredients')
        self.all = sorted(all_recipes, key=sort)

    def a_months_recipes(self, month):
        return set(r for r in self.all
                   if not r.always_available() and month in r.months_in_season)

    def this_months_recipes(self):
        return self.a_months_recipes(self.month)

    def this_but_not_last(self):
        last_month = self.month.previous()
        return self.this_months_recipes() - self.a_months_recipes(last_month)

    def this_but_not_next(self):
        next_month = self.month.next()
        return self.this_months_recipes() - self.a_months_recipes(next_month)

    def evergreen_recipes_that_peak_this_month(self):
        for r in self.all:
            if r.always_available() and self.month in r.months_in_peak_season:
                yield r

    def seasonal_recipes(self):
        recipes = dict((r.name, RecipeWithSeasonality(r)) for r in
                       self.this_months_recipes())
        for r in self.this_but_not_last():
            recipes[r.name].just_in = True
        for r in self.this_but_not_next():
            recipes[r.name].last_chance = True
        return sorted(recipes.values(), key=lambda r: (-r.last_chance, -r.just_in, r.name))
