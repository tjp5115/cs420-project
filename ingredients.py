__author__ = 'Tyler Paulsen'
import json
import timeit
from Cuisine import Cuisine

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
        
for recipe in data:
        name = recipe['cuisine'].strip()
        if not cuisine.has_key(name):
                cuisine[name] = Cuisine(name)

        for ingredient in recipe['ingredients']:
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


