import datetime
import random
from collections import defaultdict
from math import ceil

from editrecipes.helpers import MonthRecipes
from editrecipes.models import Recipe, Guest, Recent
from editrecipes.viewmodels import RecipeWithSeasonality


class ChosenMeal:
    def __init__(self, name=None):
        self.name = name


class Day:
    def __init__(self, data):
        print(data)
        self.name = data["name"]
        self.guests = data["guests"]
        self.meals = []
        self.recipe = ChosenMeal()
        self.preprepared = data["preprepared"]
        self.maxTime = datetime.timedelta(minutes=int(data["maxTime"])) if data["maxTime"] is True else None


class Constraint:
    def __init__(self, data):
        self.name = data["name"]
        self.max = data["max"]
        self.min = data["min"]
        self.recipe = None

    def __str__(self):
        return str(self.min) + "<" + self.name + "<" + str(self.max)


class WeekPlan:
    def __init__(self, data):
        self.days = [Day(day) for day in data["days"]]
        self.constraints = [Constraint(c) for c in data["chosenTags"]]
        self.mostRecent = (data["mostRecent"]["value"]).strip()[:9]

        # self.number_of_meals = ceil(len(self.days) / 2)
        self.menu = []
        recipes = MonthRecipes()

        potential_recipes = []
        for constraint in [c for c in self.constraints if c.min is not None]:
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

        self.remove_recent_meals()

        try:
            self.assign_to_days()
            # Missing feature: not two meals of same category in a week
        except IndexError:
            self.potential_to_menu(recipes.all)
            try:
                self.assign_to_days()
            except IndexError:
                raise IndexError("Not enough meal options!")

    def remove_recent_meals(self):
        for meal in self.menu:
            try:
                recent = Recent.get_meals_since(self.mostRecent).get(meal=meal)
                self.menu.remove(meal)
                print(meal.name + " was recent, removed")
            except Recent.DoesNotExist:
                print(meal.name + " not recent")
        print(self.menu)
        
    def potential_to_menu(self, potential):
        random.shuffle(potential)
        while len(potential) > 0:
            meal = potential.pop()
            if isinstance(meal, RecipeWithSeasonality):
                meal = Recipe.objects.get(pk=meal.recipepk)
            self.menu.append(meal)

    def assign_to_days(self):
        leftovers = {}
        tags = defaultdict(int)
        for day in self.days:
            meals = [m for m in leftovers.keys() if leftovers[m] >= 2]
            if not any(day.guests) and any(meals):
                meal = meals[0]
                day.recipe.name = meal
                if leftovers[meal] >= 2:
                    leftovers[meal] = leftovers[meal] - 2
                else:
                    leftovers.pop(meal)
            else:
                (meal, tags) = self.get_meal_meeting_max_constraints(day, tags)
                day.recipe.name = meal.name
                leftovers[meal.name] = meal.feeds - (len(day.guests) + 2)
                if leftovers[meal.name] < 2:
                    leftovers.pop(meal.name)

    def get_meal_meeting_max_constraints(self, day, tags):
        that_tags = tags
        i = self.skip_problem_meals(day.maxTime, day.preprepared, day.guests, 0)
        meal = self.menu.pop(i)
        for tag in meal.tags():
            that_tags[tag.name] += 1
        for c in [c for c in self.constraints if c.max is not None]:
            if c.name in tags:
                if that_tags[c.name] > c.max:
                    for tag in meal.tags():
                        that_tags[tag.name] -= 1
                    print(meal.name + " violates " + c.name)
                    return self.get_meal_meeting_max_constraints(day, tags)

        return meal, that_tags

    def skip_problem_meals(self, max_time, preprepared, guests, i):
        if preprepared and (self.menu[i].can_be_made_in_advance is False):
            i += 1
            return self.skip_problem_meals(max_time, preprepared, guests, i)
        if max_time and self.menu[i].time > max_time:
            i += 1
            return self.skip_problem_meals(max_time, preprepared, guests, i)
        for guest in [Guest.objects.get(name=g["dinerName"]) for g in guests]:
            for tag in [tag.name for tag in guest.problem_tags.all()]:
                if tag in [t.name for t in self.menu[i].tags()]:
                    print(tag + " is problematic for " + guest.name + "; skipping " + self.menu[i].name)
                    i += 1
                    return self.skip_problem_meals(max_time, preprepared, guests, i)
        return i

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['menu']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
