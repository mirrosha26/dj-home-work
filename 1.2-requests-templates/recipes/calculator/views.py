from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}

def calculator_views(request, **kwargs):
    key = kwargs['key']
    servings = int(request.GET.get('servings'))
    if not servings:
        servings = 1

    recipe = DATA.get(key)
    if recipe:
        for key, value in recipe.items():
            recipe[key] = value * servings
            
    context = {
        'recipe': recipe,
        }
    return render(request, 'calculator/index.html', context)
