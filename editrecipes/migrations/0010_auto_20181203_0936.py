# Generated by Django 2.1 on 2018-12-03 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('editrecipes', '0009_auto_20180903_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='editrecipes.Ingredient')),
            ],
            options={
                'verbose_name': 'Quantity of ingredient',
            },
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnitConversion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conversion_factor', models.DecimalField(decimal_places=2, max_digits=6)),
                ('from_unit', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='convert_from_unit', to='editrecipes.Unit')),
                ('to_unit', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='convert_to_unit', to='editrecipes.Unit')),
            ],
        ),
        migrations.AddField(
            model_name='quantity',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='editrecipes.Unit'),
        ),
        migrations.AddField(
            model_name='ingredientquantity',
            name='quantity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='editrecipes.Quantity'),
        ),
        migrations.AddField(
            model_name='ingredientquantity',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='editrecipes.Recipe'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredient_quantities',
            field=models.ManyToManyField(related_name='recipes_with_quantities', through='editrecipes.IngredientQuantity', to='editrecipes.Ingredient'),
        ),
    ]
