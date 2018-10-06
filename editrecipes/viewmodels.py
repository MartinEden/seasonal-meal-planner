from editrecipes.models import Recipe


class RecipeWithSeasonality(object):
    def __init__(self, recipe: Recipe):
        self.name = recipe.name
        self.category = recipe.category
        self.just_in = False
        self.last_chance = False
