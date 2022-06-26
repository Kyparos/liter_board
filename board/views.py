from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Post, CocktailRating, UserFollowing


def index(request):
    return render(request, 'board/index.html')


def posts(request, user_id):
    return render(request, 'board/posts.html', {'user': user_id})


def post_user(request, user_id):
    current_user = request.user
    user_posts = User.objects.get(id=user_id)
    posts = Post.objects.filter(user=user_id)
    posts_list = list(map(lambda x: ( x, zip(x.cocktails.all(), x.cocktail_rating.all())), posts))
    return render(request, 'posts.html', {'user': user_posts,
                                          'current_user': current_user,
                                                'posts': posts_list,
                                                'cocktail_rating': CocktailRating,
                                                'followings': UserFollowing.objects.filter(user_id=user_id)})
