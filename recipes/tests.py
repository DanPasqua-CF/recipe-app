from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from .forms import RecipeSearchForm
import pandas as pd


class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(
            name='Coffee', 
            ingredients='Water, Coffee Beans, Cream, Sugar',
            cooking_time=5
        )
    
    # Name field label
    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=1)
        label = recipe._meta.get_field("name").verbose_name
        self.assertEqual(label, "name")

    # Max length for Name field
    def test_recipe_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)

    # Ingredients max length
    def test_ingredients_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("ingredients").max_length
        self.assertEqual(max_length, 225)

    # Type value for cooking_time
    def test_cooking_time_type(self):
        recipe = Recipe.objects.get(id=1)
        self.assertIsInstance(recipe.cooking_time, int)

    # Test difficulty calculation
    def test_calculate_difficulty(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.calculate_difficulty, "Medium")
    
    # Additional difficulty calculation tests
    def test_calculate_difficulty_easy(self):
        recipe = Recipe.objects.create(
            name='Tea',
            ingredients='Tea Leaves, Sugar, Water',
            cooking_time=5
        )
        self.assertEqual(recipe.calculate_difficulty, 'Easy')
    
    def test_calculate_difficulty_intermediate(self):
        recipe = Recipe.objects.create(
            name='Steak',
            ingredients='Steak, Salt, Pepper',
            cooking_time=15
        )
        self.assertEqual(recipe.calculate_difficulty, 'Intermediate')
    
    def test_calculate_difficulty_hard(self):
        recipe = Recipe.objects.create(
            name='Lasagna',
            ingredients='Pasta, Beef, Tomato, Cheese, Onion, Garlic',
            cooking_time=45
        )
        self.assertEqual(recipe.calculate_difficulty, 'Hard')

class RecipeFormTest(TestCase):    
    def test_form_fields_exist(self):
        form = RecipeSearchForm()
        self.assertIn('recipe_name', form.fields)
        self.assertIn('ingredient', form.fields)
        self.assertIn('difficulty', form.fields)
        self.assertIn('chart_type', form.fields)
    
    def test_recipe_name_field_label(self):
        form = RecipeSearchForm()
        self.assertEqual(form.fields['recipe_name'].label, 'Recipe Name')
    
    def test_ingredient_field_label(self):
        form = RecipeSearchForm()
        self.assertEqual(form.fields['ingredient'].label, 'Ingredient')
    
    def test_difficulty_field_label(self):
        form = RecipeSearchForm()
        self.assertEqual(form.fields['difficulty'].label, 'Difficulty Level')
    
    def test_chart_type_field_label(self):
        form = RecipeSearchForm()
        self.assertEqual(form.fields['chart_type'].label, 'Chart Type')
    
    def test_recipe_name_max_length(self):
        form = RecipeSearchForm()
        self.assertEqual(form.fields['recipe_name'].max_length, 100)
    
    def test_ingredient_max_length(self):
        form = RecipeSearchForm()
        self.assertEqual(form.fields['ingredient'].max_length, 100)
    
    def test_form_valid_with_empty_data(self):
        form = RecipeSearchForm(data={})
        self.assertTrue(form.is_valid())
    
    def test_form_valid_with_recipe_name_only(self):
        form = RecipeSearchForm(data={'recipe_name': 'Pasta'})
        self.assertTrue(form.is_valid())
    
    def test_form_valid_with_all_fields(self):
        form = RecipeSearchForm(data={
            'recipe_name': 'Pasta',
            'ingredient': 'tomato',
            'difficulty': 'Easy',
            'chart_type': 'bar'
        })
        self.assertTrue(form.is_valid())
    
    def test_difficulty_choices(self):
        form = RecipeSearchForm()
        choices = [choice[0] for choice in form.fields['difficulty'].choices]
        self.assertIn('', choices)
        self.assertIn('Easy', choices)
        self.assertIn('Medium', choices)
        self.assertIn('Intermediate', choices)
        self.assertIn('Hard', choices)
    
    def test_chart_type_choices(self):
        form = RecipeSearchForm()
        choices = [choice[0] for choice in form.fields['chart_type'].choices]
        self.assertIn('', choices)
        self.assertIn('bar', choices)
        self.assertIn('pie', choices)
        self.assertIn('line', choices)
    
    def test_recipe_name_placeholder(self):
        form = RecipeSearchForm()
        placeholder = form.fields['recipe_name'].widget.attrs.get('placeholder')
        self.assertEqual(placeholder, 'Enter recipe name')
    
    def test_ingredient_placeholder(self):
        form = RecipeSearchForm()
        placeholder = form.fields['ingredient'].widget.attrs.get('placeholder')
        self.assertEqual(placeholder, 'Enter ingredient')
    
    def test_form_invalid_with_too_long_recipe_name(self):
        long_name = 'a' * 101
        form = RecipeSearchForm(data={'recipe_name': long_name})
        self.assertFalse(form.is_valid())
    
    def test_form_invalid_with_too_long_ingredient(self):
        long_ingredient = 'a' * 101
        form = RecipeSearchForm(data={'ingredient': long_ingredient})
        self.assertFalse(form.is_valid())

class RecipeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test user
        cls.user = User.objects.create_user(
            username='testuser',
            password='Test123!'
        )
        
        Recipe.objects.create(
            name='Tea',
            ingredients='Tea Leaves, Sugar, Water',
            cooking_time=5
        )
        Recipe.objects.create(
            name='Coffee',
            ingredients='Coffee, Sugar, Milk',
            cooking_time=3
        )
        Recipe.objects.create(
            name='Pasta',
            ingredients='Pasta, Tomato, Garlic, Onion, Basil',
            cooking_time=20
        )
        Recipe.objects.create(
            name='Soup',
            ingredients='Chicken, Vegetables, Salt, Pepper, Water, Herbs',
            cooking_time=45
        )
    
    def setUp(self):
        self.client = Client()
    
    # Home view tests
    def test_home_view_accessible(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
    
    # Login view tests
    def test_login_view_accessible(self):
        response = self.client.get(reverse('recipes:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('recipes:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
    
    # Recipe list view tests
    def test_recipe_list_requires_login(self):
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/list/')
    
    def test_recipe_list_accessible_when_logged_in(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
    
    # Recipe detail view tests
    def test_recipe_detail_requires_login(self):
        response = self.client.get(reverse('recipes:detail', args=[1]))
        self.assertEqual(response.status_code, 302)
    
    def test_recipe_detail_accessible_when_logged_in(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.get(reverse('recipes:detail', args=[1]))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_detail_shows_correct_recipe(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.get(reverse('recipes:detail', args=[1]))
        self.assertEqual(response.context['recipe'].name, 'Tea')
    
    def test_recipe_detail_contains_ingredients_list(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.get(reverse('recipes:detail', args=[1]))
        self.assertIn('ingredients_list', response.context)
        self.assertIsInstance(response.context['ingredients_list'], list)
    
    # Recipe search view tests
    def test_recipe_search_requires_login(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 302)
    
    def test_recipe_search_accessible_when_logged_in(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_search_displays_form(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.get(reverse('recipes:search'))
        self.assertIsInstance(response.context['form'], RecipeSearchForm)
    
    def test_recipe_search_by_name(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': 'Tea',
            'ingredient': '',
            'difficulty': '',
            'chart_type': ''
        })
        recipes_df = response.context['recipes_df']
        self.assertIsNotNone(recipes_df)
        self.assertEqual(len(recipes_df), 1)
        self.assertIn('Tea', recipes_df.values[0])
    
    def test_recipe_search_by_ingredient(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': '',
            'ingredient': 'Sugar',
            'difficulty': '',
            'chart_type': ''
        })
        recipes_df = response.context['recipes_df']
        self.assertIsNotNone(recipes_df)
        self.assertEqual(len(recipes_df), 2)
    
    def test_recipe_search_by_difficulty(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': '',
            'ingredient': '',
            'difficulty': 'Easy',
            'chart_type': ''
        })
        recipes_df = response.context['recipes_df']
        self.assertIsNotNone(recipes_df)
        self.assertEqual(len(recipes_df), 2)
    
    def test_recipe_search_combined_filters(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': '',
            'ingredient': 'Sugar',
            'difficulty': 'Easy',
            'chart_type': ''
        })
        recipes_df = response.context['recipes_df']
        self.assertIsNotNone(recipes_df)
        self.assertEqual(len(recipes_df), 2)
    
    def test_recipe_search_no_results(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': 'NonexistentRecipe',
            'ingredient': '',
            'difficulty': '',
            'chart_type': ''
        })
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('No recipes found', str(messages[0]))
    
    def test_recipe_search_with_chart(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': '',
            'ingredient': '',
            'difficulty': '',
            'chart_type': 'bar'
        })
        chart = response.context['chart']
        self.assertIsNotNone(chart)
        self.assertIsInstance(chart, str)
        self.assertTrue(len(chart) > 0)
    
    def test_recipe_search_no_chart_when_not_requested(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': 'Tea',
            'ingredient': '',
            'difficulty': '',
            'chart_type': ''
        })
        chart = response.context['chart']
        self.assertIsNone(chart)
    
    def test_recipe_search_bar_chart_generation(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': '',
            'ingredient': '',
            'difficulty': '',
            'chart_type': 'bar'
        })
        self.assertIsNotNone(response.context['chart'])
    
    def test_recipe_search_pie_chart_generation(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': '',
            'ingredient': '',
            'difficulty': '',
            'chart_type': 'pie'
        })
        self.assertIsNotNone(response.context['chart'])
    
    def test_recipe_search_line_chart_generation(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.post(reverse('recipes:search'), {
            'recipe_name': '',
            'ingredient': '',
            'difficulty': '',
            'chart_type': 'line'
        })
        self.assertIsNotNone(response.context['chart'])
    
    # Logout view
    def test_logout_view_redirects(self):
        self.client.login(username='testuser', password='Test123!')
        response = self.client.get(reverse('recipes:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/success.html')

# Recipe URLs
class RecipeURLTest(TestCase):
    def test_home_url_resolves(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')
    
    def test_login_url_resolves(self):
        url = reverse('recipes:login')
        self.assertEqual(url, '/login/')
    
    def test_logout_url_resolves(self):
        url = reverse('recipes:logout')
        self.assertEqual(url, '/logout/')
    
    def test_list_url_resolves(self):
        url = reverse('recipes:list')
        self.assertEqual(url, '/list/')
    
    def test_detail_url_resolves(self):
        url = reverse('recipes:detail', args=[1])
        self.assertEqual(url, '/detail/1/')
    
    def test_search_url_resolves(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/search/')

    def test_about_url_resolves(self):
        url = reverse('recipes:about')
        self.assertEqual(url, '/about/')

    def test_add_recipe_url_resolves(self):
        url = reverse('recipes:add')
        self.assertEqual(url, '/add-recipe/')
