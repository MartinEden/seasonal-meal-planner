# Generated by Django 2.1 on 2019-08-01 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('editrecipes', '0023_remove_month_shortname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='editrecipes.Recipe')),
            ],
        ),
    ]
