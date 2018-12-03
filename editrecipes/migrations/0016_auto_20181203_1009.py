# Generated by Django 2.1 on 2018-12-03 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editrecipes', '0015_auto_20181203_1008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredient_quantities',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='editrecipes.IngredientQuantity', to='editrecipes.Ingredient'),
        ),
    ]
