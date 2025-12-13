from django.db import models
from django.urls import reverse

class Recipe(models.Model):
    # -----------------------------
    # Fields
    # -----------------------------
    name = models.CharField(max_length=50)
    ingredients = models.CharField(
        max_length=225,
        help_text="Enter the ingredients, separated by a comma"
    )
    cooking_time = models.IntegerField(help_text="Cooking time in minutes")
    pic = models.ImageField(
        upload_to='recipes/',  # saves files under 'recipes/' in S3
        default='recipes/no_picture.jpg',
        blank=True,
        null=True
    )

    # -----------------------------
    # Calculate difficulty
    # -----------------------------
    @property
    def calculate_difficulty(self):
        ingredients_list = self.ingredients.split(", ")
        if self.cooking_time < 10 and len(ingredients_list) < 4:
            return "Easy"
        elif self.cooking_time < 10 and len(ingredients_list) >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and len(ingredients_list) < 4:
            return "Intermediate"
        else:
            return "Hard"

    # -----------------------------
    # String representation
    # -----------------------------
    def __str__(self):
        return self.name

    # -----------------------------
    # Absolute URL
    # -----------------------------
    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"pk": self.pk})
