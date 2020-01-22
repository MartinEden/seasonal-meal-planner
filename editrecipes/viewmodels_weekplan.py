import random
from collections import defaultdict
from math import ceil

from editrecipes.helpers import MonthRecipes
from editrecipes.models import Recipe, Guest
from editrecipes.viewmodels import RecipeWithSeasonality


class ChosenMeal:
    def __init__(self, name=None):
        self.name = name


class Day:
    def __init__(self, data):
        self.name = data["name"]
        self.guests = data["guests"]
        self.meals = []
        self.recipe = ChosenMeal()


class Constraint:
    def __init__(self, data):
        self.name = data["name"]
        self.max = data["max"]
        self.min = data["min"]
        self.recipe = None


class WeekPlan:
    def __init__(self, data):
        self.days = [Day(day) for day in data["days"]]
        self.constraints = [Constraint(c) for c in data["chosenTags"]]

        # self.number_of_meals = ceil(len(self.days) / 2)
        self.menu = []
        recipes = MonthRecipes()

        potential_recipes = []
        for constraint in [c for c in self.constraints]:
            matching_recipes = [r for r in recipes.all if constraint.name in [t.name for t in r.tags()]]
            i = 0
            while i < constraint.min:
                potential_recipes.append(matching_recipes.pop(0))
                i += 1
            self.potential_to_menu(potential_recipes)

        potential_recipes = recipes.seasonal_recipes()
        potential = [r for r in potential_recipes if r.last_chance is True and r.just_in is True]
        self.potential_to_menu(potential)
        potential = [r for r in potential_recipes if r.last_chance is False and r.just_in is True]
        self.potential_to_menu(potential)
        potential = [r for r in potential_recipes if r.last_chance is True and r.just_in is False]
        self.potential_to_menu(potential)
        potential = [r for r in potential_recipes if r.last_chance is False and r.just_in is False]
        self.potential_to_menu(potential)
        self.potential_to_menu([r for r in recipes.evergreen_recipes_that_peak_this_month()])

        try:
            self.assign_to_days()
        except IndexError:
            self.potential_to_menu(recipes.all)
            try:
                self.assign_to_days()
            except IndexError:
                raise IndexError("Not enough meal options!")

    def potential_to_menu(self, potential):
        random.shuffle(potential)
        while len(potential) > 0:
            meal = potential.pop()
            if isinstance(meal, RecipeWithSeasonality):
                meal = Recipe.objects.get(pk=meal.recipepk)
            self.menu.append(meal)

    def assign_to_days(self):
        leftovers = None
        tags = defaultdict(int)
        for day in self.days:
            if leftovers and not any(day.guests):
                day.recipe.name = leftovers
                leftovers = None
            else:
                (meal, tags) = self.get_meal_meeting_max_constraints(day, tags)
                day.recipe.name = meal.name
                leftovers = meal.name

    def get_meal_meeting_max_constraints(self, day, tags):
        that_tags = tags
        i = self.skip_problem_meals(day.guests, 0)
        meal = self.menu.pop(i)
        for tag in meal.tags():
            that_tags[tag] += 1
        for c in [c for c in self.constraints if c.name in tags]:
            if that_tags[c.name] > c.max:
                return self.get_meal_meeting_max_constraints(tags)

        return meal, that_tags

    def skip_problem_meals(self, guests, i):
        for guest in [Guest.objects.get(name=g["dinerName"]) for g in guests]:
            for tag in [tag.name for tag in guest.problem_tags.all()]:
                if tag in [t.name for t in self.menu[i].tags()]:
                    print(tag + " is problematic for " + guest.name + "; skipping " + self.menu[i].name)
                    i += 1
                    return self.skip_problem_meals(guests, i)
        return i

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['menu']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
