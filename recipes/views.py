from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Recipe

# Create your views here.

# Home page
def home(request):
   return render(request, 'recipes/recipes_home.html')

# Login page
def login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("recipes:list")
        else:
            error_message = "Invalid username or password"

    context = {
        "form": form,
        "error_message": error_message,
    }

    return render(request, "auth/login.html", context)

def logout_view(request):
    logout(request)
    return render(request, 'auth/success.html')

# Recipe list
@login_required(login_url='/login/')
def recipes_list(request):
   recipes = Recipe.objects.all()
   context = {
      'recipes': recipes
   }
   return render(request, 'recipes/recipes_list.html', context)

# Recipe detail
@login_required(login_url='/login/')
def recipes_details(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    ingredients_list = recipe.ingredients.split(", ")

    return render(request, "recipes/recipes_details.html", {
        "recipe": recipe,
        "ingredients_list": ingredients_list,
    })
