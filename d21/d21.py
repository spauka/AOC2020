import re
from collections import defaultdict
from typing import List

class Food:
    def __init__(self, ingredients: List, allergens: List):
        self.ingredients = set(ingredients)
        self.allergens = set(allergens)

    FORMAT = re.compile(r"^((?:(?:[a-z]+) ?)+)\(contains ((?:(?:[a-z]+)(?:, )?)+)\)")
    @classmethod
    def parse(cls, inp):
        match = Food.FORMAT.match(inp)
        if match is None:
            raise ValueError(f"Could not parse input {inp}.")
        ingredients, allergens = match.groups()
        ingredients = ingredients.split()
        allergens = re.split(", ", allergens)
        return Food(ingredients, allergens)

food = []
with open("input") as f:
    for line in f:
        food.append(Food.parse(line.strip()))

# Part 1
allergens = {}
ingredients = set()
possible_allergens = set()
for f in food:
    ingredients.update(f.ingredients)
    for allergen in f.allergens:
        if allergen in allergens:
            allergens[allergen].intersection_update(f.ingredients)
        else:
            allergens[allergen] = f.ingredients.copy()
for allergen in allergens:
    possible_allergens.update(allergens[allergen])
impossible_allergens = ingredients - possible_allergens

count = 0
for f in food:
    count += len(f.ingredients & impossible_allergens)
print(f"Part 1: {count}")

matched_allergen = []
while any(len(x) for x in allergens.values()):
    for allergen in allergens:
        if len(allergens[allergen]) == 1:
            ingredient = allergens[allergen].pop()
            matched_allergen.append((allergen, ingredient))
            for poss_ingredients in allergens.values():
                poss_ingredients.discard(ingredient)
matched_allergen.sort()
print("Part 2:", ",".join(ingredient for _, ingredient in matched_allergen))
