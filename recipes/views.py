from django.shortcuts import render, get_object_or_404
from .models import Recipe

# Create your views here.

# Home page
def home(request):
   return render(request, 'recipes/recipes_home.html')

# Recipe list
def recipes_list(request):
   recipes = Recipe.objects.all()
   context = {
      'recipes': recipes
   }
   return render(request, 'recipes/recipes_list.html', context)

# Recipe detail
def recipes_details(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    ingredients_list = recipe.ingredients.split(", ")

    return render(request, "recipes/recipes_details.html", {
        "recipe": recipe,
        "ingredients_list": ingredients_list,
    })
