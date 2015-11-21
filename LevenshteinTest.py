__author__ = 'Crystal'
from Levenshtein import distance
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
str1 = "Meats"
str3 = ['Meat soup','Meatloaf','Meats']
print(process.extract(str1,str3))
