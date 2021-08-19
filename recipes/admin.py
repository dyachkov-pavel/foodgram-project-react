from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Follow, Ingredient, RecipeIngredient, Recipe, Tag, Favourite, Purchase

User = get_user_model()


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'description', 'time',)
    search_fields = ('author', 'title', 'tag')
    list_filter = ('author', 'tag', 'title')
    inlines = [RecipeIngredientInline]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension',)
    search_fields = ('title', 'dimension',)
    list_filter = ('dimension', 'title',)
    inlines = [RecipeIngredientInline]


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe_id',
                    'recipe', 'ingredient_id',
                    'ingredient', 'quantity',)
    search_fields = ('recipe', 'ingredient',)
    list_filter = ('recipe', 'ingredient',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
