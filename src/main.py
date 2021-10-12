from tables import generate_order
from flask import Flask, request
from multiprocessing import Process
import time, requests

d_hall = Flask(__name__)


@d_hall.route('/distribution', methods=['POST'])
def distribution():
	data = request.json
	print('Ready order:', flush=False)
	print(data, flush=True)

	return 'None'


def send_random_orders():
	id = 0
	while True:
		time.sleep(3)
		# print(generate_order(), flush=False)
		# print(type(generate_order()), flush=False)
		id += 1
		requests.post('http://localhost:5000/order', json=generate_order(id))


if __name__ == '__main__':
	p = Process(target=send_random_orders)
	p.start()
	d_hall.run(host='localhost', port=5050, use_reloader=False)
	p.join()
