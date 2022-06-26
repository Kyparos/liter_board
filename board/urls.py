from django.urls import include, path

from . import views

app_name = 'board'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/', views.post_user, name='user_post'),
    path('register/', views.register_request, name='register'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("django.contrib.auth.urls")),
    path('<int:user_id>/<int:post_id>/', views.set_clink, name='set_clink'),
]
