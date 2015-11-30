__author__ = 'Alexander Bobowski'
from Cuisine import Cuisine
import json
import math
from fuzzywuzzy import process

global G_TOTAL_RECIPES
global G_DEBUG
G_DEBUG = False

# Opens the list of cleaned ingredients, returns the map of cuisines
def open_cuisines():
    filename = "Ingredients_Cleaned.json"
    cuisines = []
    # Why?  What does this do? No idea.
    limit = 10
    with open(filename) as data_file:
        data = json.load(data_file)
    for i in range(len(data)):
        cuisines.append(Cuisine().init_json(data[i]))
        cuisines[i].trim_limit(limit)
    return cuisines

# Match a provided ingredient with an ingredient included in the cuisine
# provided
# Returns none if no good match, matched ingredient otherwise
def match_ingredient(ingredient, cuisine):
    G_ING_SIMILARITY_THRESHOLD = 80
    match = process.extract(ingredient, cuisine.ingredients.keys(), limit=1)
    if match[0][1] >= G_ING_SIMILARITY_THRESHOLD:
        return match[0][0]
    else:
        if G_DEBUG:
            print("No match for '" + ingredient + "', '" + match[0][0] + \
                  "' closest (" + str(match[0][1]) + ")")
        return None
        
# Classify a recipe as a specific cuisine
def bayes_classify(recipe, cuisines):
    # Pick cuisine with highest relative probability
    best = 0
    best_cuisine = None
    # Check every cuisine
    for cuisine in cuisines:
        # Compute relative probability
        relative_prob = float(cuisine.num_recipes) / float(G_TOTAL_RECIPES)
        for ingredient in recipe['ingredients']:
            # Find closest matching ingredient
            ing_match = match_ingredient(ingredient, cuisine)
            # If no good match for ingredient, fudge it so relative probability
            # doesn't go to zero
            if ing_match == None:
                relative_prob = relative_prob * float(1)/float(cuisine.num_recipes)
            # Otherwise, use the real number:
            # recipes containing  ingredient in cuisine / recipes in cuisine
            else:
                relative_prob = relative_prob * \
                    (float(cuisine.ingredients[ing_match]) / cuisine.num_recipes)
        # Keep track of what has the highest relative probability
        if relative_prob > best:
            best = relative_prob
            best_cuisine = cuisine
    return best_cuisine

def main():
    # You could compute this each time from the list of cuisines, but that's
    # unnecessary redundacy.  To safe some computation time, make it global
    global G_TOTAL_RECIPES
    # Name of the training data, this really should be validation data, not
    # the training data
    G_TRAIN_FILE = "train.json"
    train_data = None
    # Load the cuisines from the training data
    cuisines = open_cuisines()
    # Compute total number of recipes from number of recipes in each cuisine
    G_TOTAL_RECIPES = 0
    for cuisine in cuisines:
        G_TOTAL_RECIPES += cuisine.num_recipes
    # Open this as training data, but its being used as validation data
    with open(G_TRAIN_FILE) as data_file:
        train_data = json.load(data_file)

    # Keep track of our score
    correct = 0
    incorrect = 0
    # this really should be run on validation data, not training data
    for unclassified in train_data:
        # Find the cuisine that matches best with naive bayesian analysis
        match = bayes_classify(unclassified, cuisines)
        if G_DEBUG:
            print("T: " + unclassified['cuisine'] + "\tP: " + match.name)
        if match.name == unclassified['cuisine']:
            correct += 1
        else:
            incorrect += 1
        total = correct + incorrect
        if total % 10 == 0:
            print(str(correct + incorrect) + "|\tc:" + str(correct) + "\ti:" +\
                  str(incorrect) + "\tr: " + \
                  str(float(correct) / (correct + incorrect)))

if __name__ == "__main__":
    main()
