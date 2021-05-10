from flask import Flask, render_template, request, jsonify
from utils import get_random_message
import random as r
import sqlite3 as sql
import uuid
import pendulum as p
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route("/menu", methods=["GET"])
def get_menu():
    args = request.args
    print("menu args", args)
    filters = []
    variables = {}
    if request.args.get("pizza_type"):
        filters.append("pizza_type = :pizza_type")
        variables["pizza_type"] = request.args.get("pizza_type")
    if request.args.get("size_type"):
        filters.append("crust_type = :crust_type")
        variables["crust_type"] = request.args.get("size_type")
    if request.args.get("pizza"):
        filters.append("pizza = :pizza")
        variables["pizza"] = request.args.get("pizza")
    if request.args.get("cost"):
        filters.append("cost = :cost")
        variables["cost"] = request.args.get("cost")

    query = f"""select id, pizza, cost from pizza_menu {('where ' + ' and '.join(filters)) if filters else ''}"""
    print(query)
    conn = sql.connect("yoyo_pizza.db")
    cursor = conn.cursor()
    cursor.execute(query, variables)
    data = cursor.fetchall()
    conn.close()
    return jsonify({"result": "success", "data": data})


@app.route("/messages", methods=["POST"])
def messages():
    data = request.get_json()
    print("Data Recieved", data)
    if not ((type(data.get("key")) is str) and (type(data.get("message")) is str)):
        return {"result": "error", "message": "Invalid Request."}
    msg_data = {"messages": "I did not understand what you meant by that."}
    if not data.get("message"):
        if data.get("key") == "size":
            msg_data = get_random_message("size")
        if data.get("key") == "":
            msg_data = get_random_message("Greetings")
    return jsonify({"result": "success", "data": msg_data}), 200


@app.route("/create_bill", methods=["POST"])
def create_bill():
    data = request.get_json()
    print(data)
    purchases = data.get("purchases", {})
    # query_data = [{"id_no": id_no, "cost_each": (value[0] // value[1])} for id_no, value in purchases.items()]
    # print(query_data)
    cost_all = sum([value[0] // value[1] for value in purchases.values() if value[1] > 0])
    total_qty = sum(value[1] for value in purchases.values() if value[1] > 0)
    cost_total = sum(value[0] for value in purchases.values() if value[1] > 0)
    id_list = purchases.keys()
    query = f"""select sum(cost)==? from pizza_menu where id in ({','.join(['?'] * len(id_list))})"""
    conn = sql.connect("yoyo_pizza.db")
    cursor = conn.cursor()
    db_resp = cursor.execute(query, [cost_all, *id_list])
    valid, = db_resp.fetchone()
    print(cost_all, total_qty, cost_total)
    if not bool(valid):
        conn.close()
        return jsonify({"result": "Error", "message": "Invalid request"})
    order_id = uuid.uuid4().hex[:7]
    time_per_pizza = r.randint(3, 5)
    pizza_creation_time = time_per_pizza * total_qty
    delivery_time = 20
    minutes = r.randint(20, delivery_time + pizza_creation_time)
    created_at = p.now("Asia/Kolkata").to_datetime_string()
    delivery_time = p.now("Asia/Kolkata").add(minutes=minutes).to_datetime_string()
    order_status = "recieved"
    order_data = {"order_id": order_id, "delivery_time": delivery_time,
                  "created_at": created_at, "order_status": order_status,
                  "order_total": cost_total}
    cursor.execute("""insert into orders(order_id, delivery_time, created_at, order_status, order_total)
                    values(:order_id, :delivery_time, :created_at, :order_status, :order_total)"""
                   , order_data)
    conn.commit()
    conn.close()
    message = "Thank you for ordering at YoYo Pizza!, <br> " \
              f"Your order with OrderID {order_id} will be delivered in {minutes} minutes"
    return jsonify({"result": "success", "data": {"messages": message, "options": ["Check order status"]}})


@app.route("/get_status", methods=["GET"])
def get_status():
    args = request.args
    order_id = args.get("order_id", "").strip()
    if not order_id:
        return jsonify({"result": "error", "message": "Invalid Request"})
    conn = sql.connect("yoyo_pizza.db")
    cursor = conn.cursor()
    data = cursor.execute("select order_status, created_at, delivery_time from orders where order_id=?",
                          (order_id,)).fetchone()
    if not data:
        return jsonify({"result": "error", "data": {"messages": "Invalid Order Id"}})
    status, created_at, delivery_time = data
    delivery_time = p.parse(delivery_time, tz="Asia/Kolkata")
    created_at = p.parse(created_at, tz="Asia/Kolkata")
    if p.now("Asia/Kolkata") > delivery_time:
        d_time = delivery_time.to_day_datetime_string()
        return jsonify({"result": "success", "data": {"messages": f"That order was delivered on {d_time}"}})
    time_now = p.now("Asia/Kolkata")
    total_minutes = (delivery_time - created_at).minutes
    minutes_passed = (time_now - created_at).minutes
    print(total_minutes, minutes_passed, delivery_time.to_datetime_string(), created_at.to_datetime_string())
    if minutes_passed < 3:
        return jsonify({"result": "success",
                        "data": {"messages": f"That order has been recieved and will be processed within 5 minutes."}})
    if 3 <= minutes_passed <= 18:
        return jsonify({"result": "success",
                        "data": {
                            "messages": f"Order is currently being prepared and will be ready within 20 mins"}})
    if minutes_passed > 18:
        return jsonify({"result": "success",
                        "data": {
                            "messages": f"Order is out for delivery and will reach you within {total_minutes - minutes_passed} minutes"}})

    return jsonify({"result": "success", "data": data})


@app.route("/clear_all_orders", methods=["POST"])
def clear_orders():
    data = request.get_json()
    if not data.get("secret") == os.environ["SECRET_KEY"]:
        return jsonify({"result": "error", "message": "invalid request"})
    try:
        conn = sql.connect("yoyo_pizza.db")
        cur = conn.cursor()
        cur.execute("delete from orders;")
        conn.commit()
        conn.close()
    except Exception:
        return jsonify({"result": "error", "message": "check logs"})
    return jsonify({"result": "success", "message": "done"})


if __name__ == '__main__':
    app.run(debug=True)
