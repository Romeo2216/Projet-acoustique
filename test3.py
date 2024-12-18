from itertools import product

range1 = range(0, 4)


# Générer les combinaisons sans miroirs et sans les paires (a, a)
combinaisons = [(a, b) for a, b in product(range1, range1) if a <= b and a != b]

print(combinaisons)