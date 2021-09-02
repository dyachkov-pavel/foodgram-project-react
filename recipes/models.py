from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import constraints
from .validators import validate_more_than_zero, validate_time

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='название')
    color = models.CharField(max_length=15, verbose_name='цвет')
    slug = models.SlugField(unique=True, verbose_name='ссылка')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    title = models.CharField(max_length=256, verbose_name='название')
    dimension = models.CharField(max_length=15,
                                 verbose_name='единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'dimension'],
                name='unique_ingredient_name'
            )
        ]

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=50, verbose_name='название')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_recipes',
        verbose_name='автор'
    )
    image = models.ImageField(upload_to='images/',
                              verbose_name='картинка')
    description = models.TextField(verbose_name='описание')
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='ing_recipes',
        verbose_name='ингредиент'
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='tag_recipes',
        verbose_name='тэг'
    )
    time = models.PositiveIntegerField(
        help_text='время в минутах',
        verbose_name='время приготовления',
        validators=[validate_time]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='ингредиент'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        validators=[validate_more_than_zero]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='one_ingredient_one_recipe'
            )
        ]
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='пользователь')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='автор')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='one_follow'
            )
        ]
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на авторов'
        ordering = ['author']

    def __str__(self):
        return self.author.username


class Favourite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='recipe_follower',
                             verbose_name='пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='fav_recipe',
                               verbose_name='рецепт')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='one_favourite'
            )
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ['-recipe__pub_date']

    def __str__(self):
        return self.recipe.title


class Purchase(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='user_purchase',
                             verbose_name='пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_purchase',
                               verbose_name='рецепт')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='one_recipe_one_purchase'
            )
        ]

        verbose_name = 'Покупка'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return self.recipe.title
