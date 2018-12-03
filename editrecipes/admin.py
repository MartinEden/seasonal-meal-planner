from django.contrib import admin
from .models import Month, Recipe, RecipesAdmin, Ingredient, Tag, DishType, \
    SideDish

admin.site.register(Month)
admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(DishType)
admin.site.register(SideDish)

