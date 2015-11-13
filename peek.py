__author__ = 'Crystal'
import operator
import json
with open("train.json") as data_file:
    data = json.load(data_file)
counterCuis = dict()
counterIngre = dict()
for item in data:
    cuisine = item['cuisine']
    if counterCuis.get(cuisine) == None:
        counterCuis[cuisine] = 1
    else:
        counterCuis[cuisine] += 1
    for ing in item['ingredients']:
        if counterIngre.get(ing) == None:
            counterIngre[ing] = 1
        else:
            counterIngre[ing] += 1



print(len(counterCuis))
print(counterCuis)
print("**")
print(len(counterIngre))
print(sorted(counterIngre.items(), key=operator.itemgetter(1)))
rofl = dict()
