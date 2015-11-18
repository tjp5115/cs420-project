__author__ = 'Tyler Paulsen'
from Cuisine import Cuisine
import json
import math
from fuzzywuzzy import process


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

similarity_threshold = 80
num_process = 10000.0
limit = 10

file = "Ingredients_Cleaned.json"
cuisines = []
with open(file) as data_file:
    data = json.load(data_file)
for i in range(len(data)):
    cuisines.append(Cuisine().init_json(data[i]))
    cuisines[i].trim_limit(limit)

train_file = "train.json"

with open(train_file) as data_file:
    train_data = json.load(data_file)
count = 0
correct = 0
cuisine_correct = {}
cuisine_incorrect= {}
for unclassified in train_data:
    best = {}
    for ingredient in unclassified['ingredients']:
        best_match = (None,0,0)
        for cuisine in cuisines:
            choice = process.extract(ingredient,cuisine.ingredients.keys())
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

    if count > num_process:
        break
    elif count % 5:
        print(count / num_process)
    count += 1

print(correct)
print("Correct: "+str(sorted(cuisine_correct.items(), key=lambda x:x[0],reverse=True)))
print("Incorrect: "+str(sorted(cuisine_incorrect.items(), key=lambda x:x[0])))

print("total correct: " + str(float(correct)/count))
