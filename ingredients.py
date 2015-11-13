__author__ = 'Crystal'
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import operator
import json
def trim():
        sorted_x = sorted(ingred.items(), key=lambda x:x[1])
        print(len(sorted_x))
        for i in sorted_x:
                if i[1] > 1:
                        break
                del ingred[i[0]]
        print(len(ingred))

with open('train.json')as data_file:
        data = json.load(data_file)
indian = []
for da in data:
        if da['cuisine'] == 'indian':
                indian.append(da)
ingred = dict()
c = 0
for recipe in indian:
        for ingredient in recipe['ingredients']:
                c += 1
                # trim the list to fuzzy search every so often.
                if c % 1000 == 0 and len(ingred) > 100:
                        print("c=",c)
                        trim()

                choice = process.extract(ingredient,ingred.keys())
                #print(ingredient + " " +str(choice))
                if len(choice) == 0:
                        ingred[ingredient] = 1
                elif choice[0][1] > 90:
                        ingred[choice[0][0]] += 1
                else:
                        ingred[ingredient] = 1

print(c)
print(ingred)
sorted_x = sorted(ingred.items(), key=lambda x:x[1],reverse=True)
for x in sorted_x:
        print(x)
