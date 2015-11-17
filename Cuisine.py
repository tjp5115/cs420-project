__author__ = 'Tyler Paulsen'
from fuzzywuzzy import process
class Cuisine:
    ingredient_threshold = 1
    def __init__(self, name=None):
        self.name = name
        self.ingredients = {}
        self.ingredients_added = 0

    def init_json(self, data):
        self.name = data['cuisine']
        self.ingredients = dict(data['ingredients'])
        self.ingredients_added = sum(self.ingredients.values())
        return self

    def trim(self):
        sorted_ingredients = sorted(self.ingredients.items(), key=lambda x:x[1])
        for ingredient in sorted_ingredients:
            if ingredient[1] > self.ingredient_threshold:
                break
            del self.ingredients[ ingredient[0] ]

    def add_ingredient(self,ingredient):
        self.ingredients_added += 1
        # trim the list to fuzzy search every so often.
        if self.ingredients_added % 500 == 0 and len(self.ingredients) > 100:
            print(self.name + " : " +str(self.ingredients_added))
            self.trim()
        choice = process.extract(ingredient, self.ingredients.keys())
        if len(choice) == 0:
            self.ingredients[ingredient] = 1
        elif choice[0][1] > 90:
            self.ingredients[choice[0][0]] += 1
        else:
            self.ingredients[ingredient] = 1

    def json_dump(self):
        sorted_x = sorted(self.ingredients.items(), key=lambda x:x[1],reverse=True)
        return {'cuisine':self.name,
                'ingredients':sorted_x
                }

    def remove_ingredient(self,ingredient):
        if self.ingredients.has_key(ingredient):
            del self.ingredients[ingredient]
