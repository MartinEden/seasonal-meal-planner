# Generated by Django 2.1 on 2018-08-25 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editrecipes', '0006_auto_20180824_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='SideDish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ingredients', models.ManyToManyField(to='editrecipes.Ingredient')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='sidedish',
            field=models.ManyToManyField(to='editrecipes.SideDish'),
        ),
    ]
