__author__ = 'Tyler Paulsen'
import json
import timeit
from Cuisine import Cuisine

# creates a new json list of ingredients.
# for each cuisine, combine the common ingredients.
# note: takes an extremely long time to complete -- ~3.5 hours.

# get the total running time
# sanity check
def get_elapsed_time():
    elapsed = timeit.default_timer() - start_time
    m, s = divmod(elapsed, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

# global vars
start_time = timeit.default_timer()
file = 'train.json'
cuisine = {}
c = 0

print("Processing json file: "+file)
with open(file)as data_file:
        data = json.load(data_file)

# get each recipe in the train.json file
for recipe in data:
        name = recipe['cuisine'].strip()
        # add a new cuisine if not in the list.
        if not cuisine.has_key(name):
                cuisine[name] = Cuisine(name)

        # loop through each ingredient in the recipe
        for ingredient in recipe['ingredients']:
            # add a new ingredient to the the cuisine
            # read the Cuisine.py comments to see how this is computed.
            cuisine[name].add_ingredient(ingredient)
        cuisine[name].inc_num_recipes()
        c += 1
        if c % 5000 == 0:
            print("Current time counter: "+get_elapsed_time())

print("Total Number of Recipes: " + str(c))
print("Creating Json file with results: Ingredients.json")
cuisine_json = []
for name in cuisine:
    cuisine_json.append(cuisine[name].json_dump())
    
with open("Ingredients.json","w") as outfile:
    json.dump(cuisine_json,outfile,indent=4,sort_keys=True)

print("Total time of execution: "+get_elapsed_time())


