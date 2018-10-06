from django.contrib import admin
from .models import Month, Recipe, Ingredient, Tag, DishType, SideDish
from django import forms

admin.site.register(Month)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(DishType)
admin.site.register(SideDish)

