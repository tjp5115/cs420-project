__author__ = 'Tyler Paulsen'
from Cuisine import Cuisine
import json
import random
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

# evaluate the choice, and return the best one.
# the best one is the choice that has the most weight in the list of ingredients
def evaluate_choice(choice,best_choice,cuisine):
    c1 = cuisine.ingredient_percent(choice[0])
    c2 = best_choice[4].ingredient_percent(best_choice[3])
    if c1 < c2:
        return best_choice
    else:
        return (cuisine.name ,choice[1],cuisine.ingredient_percent(choice[0])*choice[1],choice[0],cuisine)

# returns the best choice from the extracted list of similar words
def best_choice(choice,cuisine):
    best = choice[0]
    i = 0
    # loops through the top percentages that are the same i.e. al;l the 90% similar words
    while best[1] == choice[i][1] and len(choice) < i:
        # get the ingredient with the most weight in the list.
        if cuisine.ingredient_percent(best[0]) < cuisine.ingredient_percent(choice[i][0]):
            best = choice[i]
        i += 1
    return best

# classify the list by what cuisine is the best choice for a given ingredient
# a weight is added up for each cuisine, and the highest one is the winner.
# @num_process - number of cuisines fromt he test set to process
# @similarity_threshold - how similar should two ingredients be in order to add it to the classifiers score
# @limit - number of ingredients to limit each cuisine's number of ingredients by.
def classify(num_process, similarity_threshold, limit):
    train_file = "train.json"
    with open(train_file) as data_file:
        train_data = json.load(data_file)
    file = "Ingredients_cleaned.json"
    cuisines = []
    with open(file) as data_file:
        data = json.load(data_file)
    for i in range(len(data)):
        cuisines.append(Cuisine().init_json(data[i]))
        cuisines[i].trim_limit(limit)
    count = 0
    correct = 0
    cuisine_correct = {}
    cuisine_incorrect= {}
    # get a random sample of data of the size given
    for unclassified in random.sample(train_data, int(num_process)):
        best = {}
        # loop through all the ingredients for the unclassified cuisine
        for ingredient in unclassified['ingredients']:
            best_match = (None,0,0)
            # loop through each cuisines we have classified, and use their bag of words to classify them.
            for cuisine in cuisines:
                # find the best match to the ingredient
                choice = process.extract(ingredient,cuisine.ingredients.keys(),scorer=fuzz.QRatio)
                # do not continue to process if it is not above the thresold
                if choice[0][1] < similarity_threshold:
                    continue
                # get the best choice -- read method call comments
                choice = best_choice(choice,cuisine)
                # if two ingredients are the same for two cuisines, take the best match -- read method call comments
                if choice[1] == best_match[1]:
                    best_match = evaluate_choice(choice,best_match,cuisine)
                # add a new best match if the similarity is greater.
                if choice[1] > best_match[1]:
                    best_match = (cuisine.name ,choice[1],cuisine.ingredient_percent(choice[0])*choice[1],choice[0],cuisine)

            # if there is no best match, continue
            if best_match[0] == None:
                continue
            # add to a cuisine's score ((% of ingredients in cuisine) * (% of similarity from fuzzywuzzy))
            if best.has_key(best_match[0]):
                best[best_match[0]] += best_match[2]
            else:
                best[best_match[0]] = best_match[2]

        # get the cuisine with the highest score
        best = sorted(best.items(), key=lambda x:x[1],reverse=True)
        # if there was no best score, continue
        if len(best) == 0:
            continue
        classification = best[0][0]

        # bookkeeping.
        # see if we classified correctly
        if classification == unclassified['cuisine']:
            if cuisine_correct.has_key(classification):
                cuisine_correct[classification] += 1
            else:
                cuisine_correct[classification] = 1
            correct += 1
        else:
            if cuisine_incorrect.has_key(classification):
                cuisine_incorrect[classification] += 1
            else:
                cuisine_incorrect[classification] = 1
        count += 1

    cuisine_misclassification = {}
    # get the misclassification rate of the run.
    for cuisine in cuisine_correct:
        correct = 0.0
        incorrect = 0.0
        if cuisine_correct.has_key(cuisine):
            correct = float( cuisine_correct[cuisine] )

        if cuisine_incorrect.has_key(cuisine):
            incorrect = cuisine_incorrect[cuisine]
        cuisine_misclassification[cuisine] = incorrect / (correct + incorrect)

    print("Correct: "+str(sorted(cuisine_correct.items(), key=lambda x:x[1])))
    print("Incorrect: "+str(sorted(cuisine_incorrect.items(), key=lambda x:x[1],reverse=True)))
    print("misclassification: " + str(sorted(cuisine_misclassification.items(), key=lambda x:x[1])))
    print("total correct: " + str(float(correct)/count))
    return float(correct)/count
"""
# used to find the best similarity / limit to use.
# 85% similarity @ a limit of 31 ingredients was the best choice
correct = 0
for similarity in range(10,100,5):
    for lim in range(1,50,5):
        p = classify(1000,similarity,lim)
        if p > correct:
            print("best found",similarity,lim,p)
            best_thresholds = (similarity,lim)
            correct = p
"""
print("")
print(classify(1000,85,31))
