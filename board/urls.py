from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/', views.post_user, name='user_post')
]
