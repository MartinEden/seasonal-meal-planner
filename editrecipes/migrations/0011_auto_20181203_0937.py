# Generated by Django 2.1 on 2018-12-03 09:37

# Generated by Django 2.1 on 2018-12-03 09:35

from django.db import migrations

def add_ingredient_quantities(apps, schema_editor):
    Recipe = apps.get_model('editrecipes', 'Recipe')
    IngredientQuantity = apps.get_model('editrecipes', 'IngredientQuantity')
    Quantity  = apps.get_model('editrecipes', 'Quantity')
    Unit = apps.get_model('editrecipes', 'Unit')
    u = Unit(name="item")
    u.save()
    q = Quantity(amount=0, unit=u)
    q.save()
    for recipe in Recipe.objects.all():
        recipe.ingredient_quantities.clear()
        for i in recipe.ingredients.all():
            iq = IngredientQuantity(ingredient=i, quantity=q, recipe=recipe)
            iq.save()
        recipe.save()

class Migration(migrations.Migration):

    dependencies = [
        ('editrecipes', '0009_auto_20180903_1100'),
    ]

    operations = [
        migrations.RunPython(add_ingredient_quantities),
    ]