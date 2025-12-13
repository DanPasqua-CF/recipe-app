# Recipe App

Recipe App enables users to add, modify and delete their favorite recipes. Pictures of the finished meal can be added to show off or use for reference. Each recipe has an automatically-calculated difficulty feature, which can be categorized and visualized in a pie chart, bar graph or line graph, so users can gauge the challenge of certain recipes.

## Difficulty Calculation
The Recipe App provides users the ability to see the difficulty of the selected recipe based on the following criteria combinations:
- **Easy** - Cooking time: **< 10 minutes**, Ingredients: **< 4 items**
- **Medium** - Cooking time: **< 10 minutes**, Ingredients: **>= 4 items**
- **Intermediate** - Cooking time: **>= 10 minutes**, Ingredients: **< 4 items**
- **Hard** - Cooking time: **>= 10 minutes**, Ingredients: **>= 4 items**

## Installation
To install the Recipe application, follow these instructions:

1. Clone the repository:

```bash
https://github.com/DanPasqua-CF/recipe-app.git
cd recipe-app/src
````

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Create a superuser for admin access:

```bash
python manage.py createsuperuser
```

6. Start the development server:

```bash
python manage.py runserver
```

Access Recipe App: `http://127.0.0.1:8000/`

## Maintenance
**Developer**: Dan Pasqua  
**Portfolio**: https://danpasqua-cf.github.io/portfolio-website/  
**Contact**: dan.pasqua.cf@gmail.com  
**LinkedIn**: https://www.linkedin.com/in/dan-pasqua/ 

## Contributions
Feel free to contribute to this repository. Please remember to follow Python and Django best practices; keep styling consistent; and add tests for any new features.
