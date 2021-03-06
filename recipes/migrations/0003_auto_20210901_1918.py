# Generated by Django 3.2.4 on 2021-09-01 16:18

from django.db import migrations, models
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='title',
            field=models.CharField(max_length=256, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='quantity',
            field=models.PositiveIntegerField(validators=[recipes.validators.validate_more_than_zero], verbose_name='количество'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=30, verbose_name='название'),
        ),
    ]
