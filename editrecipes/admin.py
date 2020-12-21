from django.contrib import admin
from .models import Month, Course, Recipe, RecipesAdmin, Ingredient, Tag, DishType, \
    SideDish, Unit, UnitConversion, IngredientQuantity, Aisle, Guest, Recent

admin.site.register(Month)
admin.site.register(Course)
admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(DishType)
admin.site.register(SideDish)
admin.site.register(Unit)
admin.site.register(UnitConversion)
admin.site.register(IngredientQuantity)
admin.site.register(Aisle)
admin.site.register(Guest)
admin.site.register(Recent)