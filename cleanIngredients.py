__author__ = 'Tyler'
import json
from fuzzywuzzy import process
from Cuisine import Cuisine

#


# get the data from the file
file = 'ingredients.json'
num_ingredients = 0.0
with open(file) as data_file:
    data = json.load(data_file)

# total number of ingredients
total = len(data)
cuisines = []
# trim all of the ingredients in the cleaned json file.
for i in range(len(data)):
    cuisines.append(Cuisine().init_json(data[i]))
    cuisines[i].trim()


cuisines_1 = None
ans = None
while ans != "y" and ans != "n":
    ans = raw_input("Remove common ingredients? (y/n): ")
# remove the common ingredients between cuisines
# if a word is 90% like another word in the list and is in 85% of the cuisines combine them
if ans == "y":
    print("Removing common ingredients...")
    # get the first cuisine from the list, and append it after the comparison
    cuisine_1 = cuisines[0]
    del cuisines[0]
    for ingredient in cuisine_1.ingredients.keys():
        similar = 0
        count = 0
        for cuisine_2 in cuisines:
            count += 1
            ingredients = cuisine_2.ingredients.keys()
            # find the best match in the list of ingredients
            choice = process.extract(ingredient,ingredients)[0]
            if choice[1] >= 90:
                similar += 1

            if float(similar/count) < .65:
                break

        # remove the ingredient it if it in 85% of the cuisines
        if float(similar/count) >= .85:
            print("Removing Ingredient: " + ingredient)
            cuisine_1.remove_ingredient(ingredient)
            for cuisine in cuisines:
                cuisine.remove_ingredient(ingredient)
            
    #add the first back
    cuisines.append(cuisine_1)

print("Combining common ingredients per cuisine")
# remove common ingredients in a particular cuisine
for cuisine in cuisines:
    # threshold for how similar the ingredients need to be in order to be combined
    threshold = 95
    print("Processing: "+cuisine.name)
    # loop until the ingredients are reduced to 50, or a threshold of 90 is reached
    while len(cuisine.ingredients) >= 50 and threshold >= 90:
        ingredients = cuisine.ingredients.keys()
        # look through all the ingredients in a cuisine
        for ingredient in ingredients:
            # find the best match for an ingredient
            choice = process.extract(ingredient,ingredients)[1]
            # if the first choice is above the threshold, process it
            if choice[1] >= threshold:
                print(choice[0] + " : " + ingredient)
                # keep the ingredient that has the shortest length
                keep = choice[0] if len(choice[0]) <= len(ingredient) else ingredient
                delete = choice[0] if len(choice[0]) >= len(ingredient) else ingredient
                # skip if the length of the is the same
                if len(keep.split(" ")) == len(delete.split(" ")):
                    continue
                print(keep + " < " + delete)
                cuisine.add_ingredient(keep)
                cuisine.remove_ingredient(delete)
        threshold -= 5
        print(threshold)
        print("size:"+str(len(cuisine.ingredients)))

# create new json file
cuisine_json = []
for i in range(len(cuisines)):
    cuisine_json.append(cuisines[i].json_dump())

with open("Ingredients_Cleaned.json","w") as outfile:
    json.dump(cuisine_json,outfile,indent=4,sort_keys=True)
