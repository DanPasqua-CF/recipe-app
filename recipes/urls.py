from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.recipes_list, name='list'),
    path('detail/<int:id>/', views.recipes_details, name='detail'),
    path('search/', views.recipe_search, name='search')
]
