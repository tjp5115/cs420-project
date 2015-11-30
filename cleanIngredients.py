__author__ = 'Tyler'
import json
from fuzzywuzzy import process
from Cuisine import Cuisine

def compare_ingredients(cuisine_1,cuisine_2):
    cuisine_1.trim()
    for cuisine in cuisine_1.ingredients:
        return

file = 'ingredients.json'
num_ingredients = 0.0
with open(file) as data_file:
    data = json.load(data_file)

total = len(data)
cuisines = []
for i in range(len(data)):
    cuisines.append(Cuisine().init_json(data[i]))
    cuisines[i].trim()


cuisines_1 = None
ans = None
while ans != "y" and ans != "n":
    ans = raw_input("Remove common ingredients? (y/n): ")
if ans == "y":
    print("Removing common ingredients...")

    cuisine_1 = cuisines[0]
    del cuisines[0]
    for ingredient in cuisine_1.ingredients.keys():
        similar = 0
        count = 0
        for cuisine_2 in cuisines:
            count += 1
            ingredients = cuisine_2.ingredients.keys()
            choice = process.extract(ingredient,ingredients)[0]
            if choice[1] >= 90:
                similar += 1

            if float(similar/count) < .65:
                break

        if float(similar/count) >= .85:
            print("Removing Ingredient: " + ingredient)
            cuisine_1.remove_ingredient(ingredient)
            for cuisine in cuisines:
                cuisine.remove_ingredient(ingredient)
            
    #add the first back
    cuisines.append(cuisine_1)

print("Combining common ingredients per cuisine")

for cuisine in cuisines:
    threshold = 95
    print("Processing: "+cuisine.name)
    while len(cuisine.ingredients) >= 50 and threshold >= 90:
        ingredients = cuisine.ingredients.keys()
        for ingredient in ingredients:
            choice = process.extract(ingredient,ingredients)[1]
            if choice[1] >= threshold:
                print(choice[0] + " : " + ingredient)
                keep = choice[0] if len(choice[0]) <= len(ingredient) else ingredient
                delete = choice[0] if len(choice[0]) >= len(ingredient) else ingredient

                if len(keep.split(" ")) == len(delete.split(" ")):
                    continue
                print(keep + " < " + delete)
                cuisine.add_ingredient(keep)
                cuisine.remove_ingredient(delete)
        threshold -= 5
        print(threshold)
        print("size:"+str(len(cuisine.ingredients)))

cuisine_json = []
for i in range(len(cuisines)):
    cuisine_json.append(cuisines[i].json_dump())

with open("Ingredients_Cleaned.json","w") as outfile:
    json.dump(cuisine_json,outfile,indent=4,sort_keys=True)
