from django.db import models
from django.conf import settings


class Ingredients(models.Model):
    name = models.CharField(max_length=200)



class Images(models.Model):
    ref = models.CharField(max_length=200)


class Cocktails(models.Model):
    COCKTAILS_CATEGORIES = [(0, 'Ordinary Drink'),
                            (1, 'Homemade Liqueur'),
                            (2, 'Shake'),
                            (3, 'Cocktail'),
                            (4, 'Shot'),
                            (5, 'Soft Drink'),
                            (6, 'Other/Unknown'),
                            (7, 'Cocoa'),
                            (8, 'Punch / Party Drink'),
                            (9, 'Coffee / Tea'),
                            (10, 'Beer'),
                            (11, 'Spirit')]
    name = models.CharField(max_length=200)
    image = models.ForeignKey(Images, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.IntegerField(choices=COCKTAILS_CATEGORIES, default=0)
    ingredients = models.ManyToManyField(Ingredients, through='IngredientsAmount')


class Countries(models.Model):
    name = models.CharField(max_length=200)


class Users(models.Model):
    full_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True)
    followers = models.ManyToManyField('self')
    liter_board = models.ManyToManyField(Cocktails, through='CocktailsAmount')
    user_auth = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Posts(models.Model):
    post_text = models.CharField(max_length=5000)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
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
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, null=True)
    cocktail = models.ForeignKey(Cocktails, on_delete=models.CASCADE)
    ingredient_amount = models.TextField(max_length=70, null=True)


class CocktailsAmount(models.Model):
    cocktail = models.ForeignKey(Cocktails, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
