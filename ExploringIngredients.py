__author__ = 'Tyler Paulsen'
from Cuisine import Cuisine
import json

# Script that explores the ingredients from the list of cleaned ingredients.
# To see what the list of cleaned ingredients consists of, read

cuisines = []
file = "Ingredients_Cleaned.json"
with open(file) as data_file:
    data = json.load(data_file)
for i in range(len(data)):
    cuisines.append(Cuisine().init_json(data[i]))
    cuisines[i].trim()

k = 15
while k < 50:
    print(k)
    for cuisine in cuisines:
        print(cuisine.name + "\t\t:\t"),
        i = 0
        percentage = 0
        for ingredient in sorted(cuisine.ingredients.items(), key=lambda x:x[1],reverse=True):
            percentage += ingredient[1]
            if i > k:
                break
            i += 1
        print(str(float(percentage) / cuisine.ingredients_added))
    k+=5
