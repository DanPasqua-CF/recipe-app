from django import forms

CHART_CHOICES = (
    ('', 'No Chart'),
    ('bar', 'Bar Chart'),
    ('pie', 'Pie Chart'),
    ('line', 'Line Chart'),
)

DIFFICULTY_CHOICES = (
    ('', 'Any Difficulty'),
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Intermediate', 'Intermediate'),
    ('Hard', 'Hard'),
)


class RecipeSearchForm(forms.Form):    
    recipe_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter recipe name'
        }),
        label='Recipe Name'
    )
    
    ingredient = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter ingredient'
        }),
        label='Ingredient'
    )
    
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,
        label='Difficulty Level'
    )
    
    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        required=False,
        label='Chart Type'
    )
