# Generated by Django 2.1 on 2018-12-13 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('editrecipes', '0018_aisle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterModelOptions(
            name='aisle',
            options={'ordering': ['number']},
        ),
        migrations.AddField(
            model_name='aisle',
            name='ingredient',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='editrecipes.Ingredient'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aisle',
            name='shop',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='editrecipes.Shop'),
            preserve_default=False,
        ),
    ]
