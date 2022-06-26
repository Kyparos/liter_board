from django.contrib import admin

from .models import Post, CocktailRating, UserFollowing, Ingredient, Image



admin.site.register(Post)
admin.site.register(CocktailRating)
admin.site.register(UserFollowing)
admin.site.register(Ingredient)
admin.site.register(Image)
