__author__ = 'Tyler Paulsen'
from fuzzywuzzy import process
class Cuisine:
    ingredient_threshold = 1
    def __init__(self, name=None):
        self.name = name
        self.ingredients = {}
        self.ingredients_added = 0
        self.num_recipes = 0

    def init_json(self, data):
        self.name = data['cuisine']
        self.ingredients = dict(data['ingredients'])
        self.ingredients_added = sum(self.ingredients.values())
        self.num_recipes = int(data['num_recipes'])
        return self

    # Increments the number of recipes included in this cuisine
    def inc_num_recipes(self):
        self.num_recipes += 1

    def trim(self):
        sorted_ingredients = sorted(self.ingredients.items(), key=lambda x:x[1])
        for ingredient in sorted_ingredients:
            if ingredient[1] > self.ingredient_threshold:
                break
            del self.ingredients[ ingredient[0] ]

    # Returns the percentage of recipes in this cuisine containing a given
    # ingredient
    def ingredient_percent(self,ingredient):
        if not self.ingredients.has_key(ingredient):
            return None
        return float(self.ingredients[ingredient]) / self.ingredients_added

    def trim_limit(self,limit):
        self.ingredients = dict(sorted(self.ingredients.items(), key=lambda x:x[1],reverse=True)[:limit])
        self.ingredients_added = sum(self.ingredients.values())
        return
        count = 0
        total = 0
        for ingredient in sorted_ingredients:
            if limit <= float(total)/self.ingredients_added:
                self.ingredients = dict(sorted_ingredients[:count])
            count += 1
            total += ingredient[1]

        self.ingredients_added = sum(self.ingredients.values())

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
                'num_recipes':self.num_recipes,
                'ingredients':sorted_x
                }

    def remove_ingredient(self,ingredient):
        if self.ingredients.has_key(ingredient):
            del self.ingredients[ingredient]
