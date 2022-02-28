import random

items = ['Bottle', 'Butter', 'Cheese', 'Cookies', 'Coffee',
         'Cream', 'Detergent', 'Diaper', 'Dips', 'Doughs',
         'Eggs', 'Gloves', 'Icecream', 'Juice', 'Meat',
         'Milk', 'Nuts', 'Popcorn', 'Pretzels', 'ProteinShake',
         'Shirt', 'Shoes', 'Soap', 'Soda', 'Tea', 'Umbrella',
         'Watch', 'Water', 'Wine', 'Yogurt']

for i in range(1, 21):
    trans_len = random.randint(1, 6)
    items_set = set()
    while len(items_set) != trans_len:
        items_set.add(random.choice(items))
    print(f'{i} {items_set}')
