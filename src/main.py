from table import Table
from flask import Flask, request
import time
import requests
import threading
import random
import time
import json
from waiter import Waiter

d_hall = Flask(__name__)
number_of_tables = 10
number_of_waiters = 5
tables = []
waiters = []
food_list = json.load(open('./data/foods.json', 'r'))
lock = threading.Lock()
ready_to_serve = []
TIME_UNIT = 1


@d_hall.route('/distribution', methods=['POST'])
def distribution():
    data = request.json
    order = json.loads(data)
    ready_to_serve.append(order)
    print("Hey Waiter " + str(order["waiter_id"]) +
          "! Your order is ready to be served at " + str(order["table_id"]))
    return 'None'


def take_order(id, waiter_id, table_id):
    items = random.randint(1, 5)
    priority = random.randint(1, 5)

    for i in range(items):
        if type(items) is int:
            items = [random.randint(1, 10)]
        else:
            items.append(random.randint(1, 10))

    max_wait = 0
    for i in items:
        ii = food_list[i - 1]['preparation-time'] * 1.3 * TIME_UNIT
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


def send_order(waiter_id, table_id):
    order_id = 0
    order_id += 1
    requests.post('http://172.17.0.2:5000/order',
                  json=take_order(order_id, waiter_id, table_id))


def wait_tables(waiter_id):
    while True:
        if(waiters[waiter_id].is_free == True):
            for order in ready_to_serve:
                if(order["waiter_id"] == waiter_id):
                    waiters[waiter_id].is_free = False
                    time.sleep(random.randint(2, 5) * TIME_UNIT)
                    print("Max waiting time : " + str(order["max_wait"]) + " and the order took : " + str(
                        (time.time() - order["pick_up_time"]) * TIME_UNIT))
                    print("Waiter ID: " + str(order["waiter_id"]) +
                          " serving food in Table ID: " + str(order["table_id"]))

                    ready_to_serve.remove(order)
                    waiters[waiter_id].is_free = True
                    tables[order["table_id"]].status = "Free"
            print("Waiter ID: " + str(waiter_id) +
                  " checks for any table that needs order taken")
            all_tables_free = True
            for i in range(0, number_of_tables):
                if(tables[i].status == "Waiting_To_Order"):
                    tables[i].status = "Waiting_To_Be_Served"
                    waiters[waiter_id].is_free = False
                    print("Waiter ID: " + str(waiter_id) +
                          " is busy, taking order from Table ID: " + str(i))
                    # Waiter picking order
                    time.sleep(random.randint(2, 4) * TIME_UNIT)
                    send_order(waiter_id, i)
                    waiters[waiter_id].is_free = True
                    all_tables_free = False
            if(all_tables_free):
                print("Waiter ID: " + str(waiter_id) +
                      ". No tables filled at the moment, so he/she'll wait.")
                time.sleep(5 * TIME_UNIT)


def fill_tables():
    while True:
        for i in range(0, number_of_tables):
            if(tables[i].status == "Free"):
                tables[i].status = "Waiting_To_Order"
                print("Table ID: " + str(i) +
                      " is occupied now and waiting to be taken order from.")
                time.sleep(5 * TIME_UNIT)


def run_server():
    d_hall.run(host='0.0.0.0', port=5050)


if __name__ == '__main__':
    threading.Thread(target=run_server).start()
    print("******Welcome to Restaurant******")
    print("Number of tables available : " + str(number_of_tables) +
          " Number of waiters available " + str(number_of_waiters))

    for i in range(0, number_of_tables):
        tables.append(Table(i, "Free"))

    for i in range(0, number_of_waiters):
        waiters.append(Waiter(i, True))
        threading.Thread(target=wait_tables, args=(i,)).start()

    fill_tables()
