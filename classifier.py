__author__ = 'Alexander Bobowski'
from Cuisine import Cuisine
import json
import math
import sys
from fuzzywuzzy import process

global G_TOTAL_RECIPES
global G_DEBUG
G_DEBUG = False

# Opens the list of cleaned ingredients, returns the map of cuisines
# @return    A list of all cusisines represented in the data
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
# @ingredient  Esseintailly the search query, find the ingredient in the
#              recipe closest to this
# @cuisine     Cuisine to search within
# @return      none if no good match, matched ingredient otherwise
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
# @recipe     a recipe instance from JSON
# @cuisines   all of the Cuisine instances
# @return     what bayesian analysis determines to be the most likely  cuisine
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

# Load a list of ingredients into a list
# @return    list of ingredients from "ingredients" file
def load_ingredients():
    ingredients = []
    with open("ingredients") as ingred_list:
        for line in ingred_list:
            ingredients.append(line.split(",")[0])
    return ingredients

# Define the distance between two recipes.
# The Jaccard coefficient is used for this
# @rec1         recipe 1
# @rec2         recipe 2
# @ingredients  list of all recognized ingredients
# @return       Jaccard distance
def dist(rec1, rec2, ingredients):
    # These are "normalized ingredient lists", in which every ingredient in the
    # recipe is matched to an ingredient recognized when building the cuisines
    # This is just done in order to ensure that there's a solid, exhaustive
    # list of ingredients
    for rec in [rec1, rec2]:
        if 'normalized_ing' not in rec:
            normalized_ing = []
            for ingredient in rec['ingredients']:
                normalized_ing.append(process.extract(ingredient,\
                        ingredients, limit=1)[0][0])
            rec['normalized_ing'] = normalized_ing
    # This is actually the total number of same items
    intersect =  len(set(rec1['normalized_ing']) & set(rec2['normalized_ing']))
    # This is the Jaccard coefficient
    return 1 - (float(intersect) / (len(rec1['normalized_ing']) + \
                                    len(rec2['normalized_ing']) - intersect))

# This classifies a point based on how many 
# @k               Value of k to use - number of points to comapre to
# @unknown_recipe  Recipe to be classified
# @train_data      All of the recipes used in training
# @ingred          A list of all the ingredients, used for matching
# @return          The cuisine the recipe is determined to belong to
def knn_classify(k, unknown_recipe, train_data, ingred):
    count = 0
    k_closest = [("", float("inf"))] * k
    for known_recipe in train_data:
        # Create a list with k tuples of ("", inf)
        # Keep track of progress on classifying the recipe
        count += 1
        if count >= len(train_data)/78 and G_DEBUG:
            sys.stdout.write(".")
            sys.stdout.flush()
            count = 0

        distance = dist(known_recipe, unknown_recipe, ingred)
        # This retains only the k closest points, replaces the furthest point
        # when a closer one is found
        k_closest = sorted(k_closest, key=lambda item : item[1], reverse=True)
        if k_closest[0][1] > distance:
            k_closest[0] = (known_recipe["cuisine"], distance)

    if G_DEBUG:
        print
            
    # This creates a count of how many times each class was seen
    count = {}
    for item in [x[0] for x in k_closest]:
        if item not in count:
            count[item] = 1
        else:
            count[item] += 1
    # This returns the item in the in the "count" dictionary with the largest
    # associated value, which is how we're classifying the point
    return sorted(count, key=count.get, reverse=True)[0]

# This function provides k nearest neighbor analyis
# @k           Value of k to use - number of points to examine
# @train_data  The training data - a list of recipes with a known cuisine
# @test_data   Data to classify
def knn_analysis(k, train_data, test_data):
    # Get a standardized list of ingredients to use for each recipe
    ingred = load_ingredients()
    # Keep count of how we're doing
    correct = 0
    incorrect = 0
    # Classify each point in test data
    for unclassified in test_data:
        # use the classifier to determine what cuisine the recipe belongs to
        match = knn_classify(k, unclassified, train_data, ingred)
        if match == unclassified['cuisine']:
            correct += 1
        else:
            incorrect += 1
        # Print out results
        if G_DEBUG:
            print("T: " + unclassified['cuisine'] + "\tP: " + match)
        total = correct + incorrect
        # Every 10 classifications, print out the tally
        rate = float(correct) / float(correct + incorrect)
        if total % 10 == 0:
            print(str(correct + incorrect) + "|\tc:" + str(correct) + "\ti:" +\
              str(incorrect) + "\tr: " + \
              str(float(correct) / (correct + incorrect)))

# Perform bayesian analysis on the data provided = try to classify each recipe
# @data  training data used to calculate probabilities
def bayesian_analysis(data):
    # You could compute this each time from the list of cuisines, but that's
    # unnecessary redundacy.  To safe some computation time, make it global
    global G_TOTAL_RECIPES
    # Load the cuisines from the training data
    cuisines = open_cuisines()
    # Compute total number of recipes from number of recipes in each cuisine
    G_TOTAL_RECIPES = 0
    for cuisine in cuisines:
        G_TOTAL_RECIPES += cuisine.num_recipes
    # Keep track of our score
    correct = 0
    incorrect = 0
    # this really should be run on validation data, not training data
    for unclassified in data:
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

def main():
    # Name of the training data, this really should be validation data, not
    # the training data
    G_TRAIN_FILE = "train.json"
    train_data = None
    # Open this as training data, but its being used as validation data
    with open(G_TRAIN_FILE) as data_file:
        train_data = json.load(data_file)
    ans = None
    while ans != "b" and ans != "k":
        ans = raw_input("Type of analysis to perform: (b)ayesian, (k)-nn: ")
    if ans == "b":
        bayesian_analysis(train_data)
    elif ans == "k":
        k = int(raw_input("enter k (integer): "))
        #[:len(train_data) * .9],
        #[len(train_data) * .9:])
        knn_analysis(k, train_data[:1000],train_data[1001:1100])

if __name__ == "__main__":
    main()
