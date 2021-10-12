""" order example
{
"id": 1,
"items": [ 3, 4, 4, 2 ],
"priority": 3 ,
"max_wait": 45
}
"""

import random
import json
import time

food_list = json.load(open('./data/foods.json', 'r'))
# order_id = 1


def generate_order(id=1):
	items=random.randint(1, 5)
	priority=random.randint(1, 5)
	table_id=random.randint(1, 5)
	waiter_id=random.randint(1, 3)

	for i in range(items):
		if type(items) is int:
			items = [random.randint(1, 10)]
		else:
			items.append(random.randint(1, 10))

	max_wait = 0
	for i in items:
		ii = food_list[i - 1]['preparation-time'] * 1.3
		if ii > max_wait:
			max_wait = ii

	order = dict(
		order_id=id,
		table_id=table_id,
		waiter_id=waiter_id,
		items=items,
		priority=priority,
		max_wait=max_wait,
		pick_up_time=time.time()
	)

	# print(order)
	return order



