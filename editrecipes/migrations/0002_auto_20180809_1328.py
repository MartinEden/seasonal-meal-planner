# Generated by Django 2.1 on 2018-08-09 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editrecipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='peak',
            field=models.ManyToManyField(related_name='peak_month', to='editrecipes.Month'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='seasonal',
            field=models.ManyToManyField(related_name='seasonal_month', to='editrecipes.Month'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='tags',
            field=models.ManyToManyField(to='editrecipes.Tag'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(to='editrecipes.Ingredient'),
        ),
    ]
