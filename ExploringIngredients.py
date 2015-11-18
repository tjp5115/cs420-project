__author__ = 'Tyler Paulsen'
from Cuisine import Cuisine
import json

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
    #    print(cuisine.name + "\t\t:\t"),
        i = 0
        percentage = 0
        for ingredient in sorted(cuisine.ingredients.items(), key=lambda x:x[1],reverse=True):
            #print(str(ingredient)+"\t"),
            percentage += ingredient[1]
            if i > k:
                break
            i += 1
        print(str(float(percentage) / cuisine.ingredients_added))
    k+=5
