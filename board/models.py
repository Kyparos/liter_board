from django.db import models
from django.conf import settings


class Ingredients(models.Model):
    name = models.CharField(max_length=200)
    units = [('oz', 'ounce'),
             ('ml', 'milliliters')]


class Images(models.Model):
    ref = models.CharField(max_length=200)


class Cocktails(models.Model):
    name = models.CharField(max_length=200)
    image_id = models.ForeignKey(Images, on_delete=models.SET_NULL, null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredients, through='IngredientsAmount')


class Countries(models.Model):
    name = models.CharField(max_length=200)


class Users(models.Model):
    full_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    country_id = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True)
    followers = models.ManyToManyField('self')
    liter_board = models.ManyToManyField(Cocktails, through='CocktailsAmount')
    user_auth_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Posts(models.Model):
    post_text = models.CharField(max_length=5000)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    clink = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField(Images)
    cocktails = models.ManyToManyField(Cocktails, through='CocktailRating', related_name='cock')


class CocktailRating(models.Model):
    POOR = 1
    AVERAGE = 2
    GOOD = 3
    RATING_CHOICES = (
        (POOR, 'Poor'),
        (AVERAGE, 'Average'),
        (GOOD, 'Good'),
    )

    cocktail_id = models.ForeignKey(Cocktails, related_name='cocktail_rating', on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts, related_name='cocktail_rating', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, default=AVERAGE)

    class IngredientsAmount(models.Model):
        ingredient_id = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
        cocktail_id = models.ForeignKey(Cocktails, on_delete=models.CASCADE)


class CocktailsAmount(models.Model):
    cocktail_id = models.ForeignKey(Cocktails, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

