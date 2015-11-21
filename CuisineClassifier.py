__author__ = 'Tyler Paulsen'
from Cuisine import Cuisine
import json
import random
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

def evaluate_choice(choice,best_choice,cuisine):
    c1 = cuisine.ingredient_percent(choice[0])
    c2 = best_choice[4].ingredient_percent(best_choice[3])
    if c1 < c2:
        return best_choice
    else:
        return (cuisine.name ,choice[1],cuisine.ingredient_percent(choice[0])*choice[1],choice[0],cuisine)

def best_choice(choice,cuisine):
    best = choice[0]
    i = 0
    while best[1] == choice[i][1] and len(choice) < i:
        if cuisine.ingredient_percent(best[0]) < cuisine.ingredient_percent(choice[i][0]):
            best = choice[i]
        i += 1
    return best

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
    for unclassified in random.sample(train_data, int(num_process)):
        best = {}
        for ingredient in unclassified['ingredients']:
            best_match = (None,0,0)
            for cuisine in cuisines:
                choice = process.extract(ingredient,cuisine.ingredients.keys(),scorer=fuzz.QRatio,)
                if choice[0][1] < similarity_threshold:
                    continue
                choice = best_choice(choice,cuisine)
                if choice[1] == best_match[1]:
                    best_match = evaluate_choice(choice,best_match,cuisine)
                if choice[1] > best_match[1]:
                    best_match = (cuisine.name ,choice[1],cuisine.ingredient_percent(choice[0])*choice[1],choice[0],cuisine)

            #print(str(best_choice )+ " : " + ingredient)
            #print(best_match)
            if best_match[0] == None:
                continue
            if best.has_key(best_match[0]):
                best[best_match[0]] += best_match[2]
            else:
                best[best_match[0]] = best_match[2]

        best = sorted(best.items(), key=lambda x:x[1],reverse=True)
        #print(best)
        if len(best) == 0:
            continue
        classification = best[0][0]
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
        #else:
            #print(str(best[0])+ " != "+ unclassified['cuisine'])
        count += 1

    print("Correct: "+str(sorted(cuisine_correct)))
    print("Incorrect: "+str(sorted(cuisine_incorrect)))
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
