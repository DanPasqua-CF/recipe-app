from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
from .models import Recipe
from .forms import RecipeSearchForm

try:
    from .forms import RecipeSearchForm
except ImportError:
    RecipeSearchForm = None

# Create your views here.

# Home page
def home(request):
    return render(request, 'recipes/recipes_home.html')

# Records
def records(request):
    form = SalesSearchForm(request.POST or None)

    if request.method == 'POST':
         recipe_name = request.POST.get('name')
         chart_type = request.POST.get('chart_type')

         print(recipe_name, chart_type)

         print('Exploring querysets:')
         print('Case 1: Output of Recipe.objects.all()')
         qs = Recipe.objects.all()

         print('Case 2: Output of Recipe.objects.filter(name)')
         qs = Recipe.objects.filter(recipe_name = name)
         print(qs)

         print('Case 3: Output of qs.values()')
         print(qa.values())

         print('Case 4: Output of qs.values_list()')
         print(qs.values_list)

         print('Case 5: Output of Recipe.objects.get(id=1)')
         obj = Recipe.objects.get(id = 1)
         print(obj)

    context={
       'form': form
    }
    
    return render(request, 'recipes/', context)

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

# Recipe search
@login_required(login_url='/login/')
def recipe_search(request):
    form = RecipeSearchForm(request.POST or None)
    recipes_df = None
    chart = None
    
    if request.method == 'POST' and form.is_valid():
        recipe_name = form.cleaned_data.get('recipe_name')
        ingredient = form.cleaned_data.get('ingredient')
        difficulty = form.cleaned_data.get('difficulty')
        chart_type = form.cleaned_data.get('chart_type')        
        recipes = Recipe.objects.all()
        
        if recipe_name:
            recipes = recipes.filter(name__icontains=recipe_name)
        
        if ingredient:
            recipes = recipes.filter(ingredients__icontains=ingredient)
        
        if difficulty:
            pass
        
        if recipes.exists():
            recipes_data = []

            for recipe in recipes:
                calc_difficulty = recipe.calculate_difficulty

                if difficulty and calc_difficulty != difficulty:
                    continue
                    
                recipes_data.append({
                    'id': recipe.id,
                    'name': recipe.name,
                    'ingredients': recipe.ingredients,
                    'cooking_time': recipe.cooking_time,
                    'difficulty': calc_difficulty
                })
            
            if recipes_data:
                recipes_df = pd.DataFrame(recipes_data)                
                recipes_df.columns = ['ID', 'Recipe Name', 'Ingredients', 'Cooking Time (min)', 'Difficulty']
                
                if chart_type:
                    chart = generate_chart(recipes_df, chart_type)
            else:
                messages.info(request, 'No recipes found matching your search criteria.')
        else:
            messages.info(request, 'No recipes found matching your search criteria.')
    
    context = {
        'form': form,
        'recipes_df': recipes_df,
        'chart': chart,
    }
    
    return render(request, 'recipes/recipes_search.html', context)


def generate_chart(df, chart_type):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import io
    import base64
    
    plt.figure(figsize=(10, 6))
    
    if chart_type == 'bar':
        difficulty_counts = df['Difficulty'].value_counts()
        difficulty_counts.plot(kind='bar', color='#407690', edgecolor='#f4db67', linewidth=2)
        plt.title('Recipe Count by Difficulty Level', fontsize=16, fontweight='bold', color='#407690')
        plt.xlabel('Difficulty Level', fontsize=12, color='#407690')
        plt.ylabel('Number of Recipes', fontsize=12, color='#407690')
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        
    elif chart_type == 'pie':
        difficulty_counts = df['Difficulty'].value_counts()
        colors = ['#407690', '#2d5670', '#f4db67', '#5a8ca8']
        plt.pie(difficulty_counts.values, labels=difficulty_counts.index, 
                autopct='%1.1f%%', startangle=90, colors=colors)
        plt.title('Recipe Distribution by Difficulty', fontsize=16, fontweight='bold', color='#407690')
        
    elif chart_type == 'line':
        avg_cooking_time = df.groupby('Difficulty')['Cooking Time (min)'].mean().sort_index()
        plt.plot(avg_cooking_time.index, avg_cooking_time.values, marker='o', 
                linewidth=3, markersize=10, color='#407690', markerfacecolor='#f4db67')
        plt.title('Average Cooking Time by Difficulty', fontsize=16, fontweight='bold', color='#407690')
        plt.xlabel('Difficulty Level', fontsize=12, color='#407690')
        plt.ylabel('Average Cooking Time (minutes)', fontsize=12, color='#407690')
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight', facecolor='white')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()
    
    graphic = base64.b64encode(image_png).decode('utf-8')
    return graphic
