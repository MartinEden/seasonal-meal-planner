# Generated by Django 2.1 on 2019-07-08 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editrecipes', '0019_auto_20181213_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aisle',
            name='shop',
        ),
        migrations.DeleteModel(
            name='Shop',
        ),
    ]