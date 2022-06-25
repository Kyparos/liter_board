# %%
import requests
import json
from tqdm import tqdm
import pickle

# %%
url = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=11007'

req = requests.get(url)

cocktail_json = json.loads(req.content)

# %%
cocktails = []
url_template = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i='
for i in tqdm(range(11000, 16000)):
    req = requests.get(url_template + str(i))
    cocktail_json = json.loads(req.content)
    if cocktail_json['drinks'] is None:
        continue
    cocktails.append(cocktail_json['drinks'][0])

with open('cocktails_11000_15999.pkl', 'wb') as f:
    pickle.dump(cocktails, f)

# %%

categories = []
for cock in cocktails:
    categories.append(cock['strCategory'])

categories_enum = list(enumerate(set(categories)))
categories = list(set(categories)) + ['Spirit']
with open('categories_enum.json', 'w') as f:
    json.dump(categories_enum, f)
# %%
cocktails_to_json = []
ingredients = []
img_data = []
ingredients_amount = []
ingredients_cocktail = []

for i, cock in enumerate(cocktails):
    cock_dict = {'model': 'board.Cocktails',
                 'pk': int(cock['idDrink'])}
    cock_fields = {'name': cock['strDrink'],
                   'image': i,
                   'category': categories.index(cock['strCategory'])}
    ref = cock['strDrinkThumb']
    img_data.append({'model': 'board.Images', 'pk': i, 'fields': {'ref': ref}})
    cock_dict['fields'] = cock_fields
    cocktails_to_json.append(cock_dict)
    j = 1
    for q in range(1, 16):
        if cock[f'strIngredient{str(j)}'] is None: break
        ingredients.append(cock[f'strIngredient{str(j)}'])
        j += 1

    for k in range(1, j):
        ingredients_amount.append(cock[f'strMeasure{str(k)}'])
    ingredients_cocktail += [cock['idDrink']] * (j - 1)

# %%

ingredients_uni = list(set(ingredients) - {None})

ingredients_data = []
ing_url = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?i='
for ing in tqdm(ingredients_uni):
    req = requests.get(ing_url + ing)
    if json.loads(req.content)['ingredients'] is None:
        continue
    ing_json = json.loads(req.content)['ingredients'][0]
    ing_dict = {'pk': int(ing_json['idIngredient']),
                'model': 'board.Ingredients',
                'fields': {'name': ing_json['strIngredient']}}
    ingredients_data.append(ing_dict)


# %%

def id_ing_by_name(name):
    for ing in ingredients_data:
        if ing['fields']['name'].upper() == name.upper():
            return ing['pk']
    return None


# %%

ingredients_data.sort(key=lambda x: x['pk'])

# %%

ingredients_cocktail_ing_key = list(map(id_ing_by_name, ingredients))

ing_cock_data = []
i = 0
for ing, cock, amount in zip(ingredients_cocktail_ing_key, ingredients_cocktail, ingredients_amount):
    ing_cock_data.append({'pk': i,
                          'model': 'board.IngredientsAmount',
                          'fields': {'cocktail': cock, 'ingredient': ing, 'ingredient_amount': amount}})
    i += 1

# %%
to_json = img_data + ingredients_data + cocktails_to_json + ing_cock_data
with open('data_to_dump.json', 'w') as f:
    json.dump(to_json, f)
