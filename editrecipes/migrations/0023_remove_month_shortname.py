# Generated by Django 2.1 on 2019-07-15 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editrecipes', '0022_month_shortname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='month',
            name='shortname',
        ),
    ]
