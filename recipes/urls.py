from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.recipes_list, name='list'),
    path('detail/<int:id>/', views.recipes_details, name='detail')
]
