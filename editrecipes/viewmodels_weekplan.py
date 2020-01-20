from math import ceil

from editrecipes.helpers import MonthRecipes


class Day:
    def __init__(self, data):
        self.name = data["name"]
        self.guests = data["guests"]
        self.meals = []


class Constraint:
    def __init__(self, data):
        self.tag_name = data["name"]
        self.max = data["max"]
        self.min = data["min"]
        self.recipe = None


class WeekPlan:
    def __init__(self, data):
        self.days = [Day(day) for day in data["days"]]
        self.constraints = [Constraint(c) for c in data["chosenTags"]]

        # self.number_of_meals = ceil(len(self.days) / 2)
        self.menu = []

        potential_recipes = MonthRecipes().seasonal_recipes()
        # min = [c for c in self.constraints if c.min > 0]
        # choose min recipes first
        potential = [r for r in potential_recipes if r.last_chance is True and r.just_in is True]
        self.potential_to_menu(potential)
        potential = [r for r in potential_recipes if r.last_chance is False and r.just_in is True]
        self.potential_to_menu(potential)
        potential = [r for r in potential_recipes if r.last_chance is True and r.just_in is False]
        self.potential_to_menu(potential)
        potential = [r for r in potential_recipes if r.last_chance is False and r.just_in is False]
        self.potential_to_menu(potential)

        self.assign_to_days()

    def potential_to_menu(self, potential):
        while len(potential) > 0:
            self.menu.append(potential.pop())

    def assign_to_days(self):
        leftovers = None
        for day in self.days:
            if leftovers:
                day.recipe = leftovers
                leftovers = None
            else:
                meal = self.menu.pop()
                # if meal doesn't violate max constraints
                # if meal doesn't violate guests constraints
                day.recipe = meal
                leftovers = meal
