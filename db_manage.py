import sqlite3 as sql

conn = sql.connect("yoyo_pizza.db")
cur = conn.cursor()
# cur.execute("""create table pizza_menu(id INTEGER PRIMARY KEY,
#         pizza Varchar(25) NOT NULL,  pizza_type VARCHAR(15) NOT NULL,
#         crust_type VARCHAR(15) NOT NULL, cost INTEGER);""")
# cur.execute("""create table orders(id INTEGER PRIMARY KEY,
#         order_id Varchar(25) NOT NULL,  created_at timestamp NOT NULL, delivery_time timestamp ,
#         order_status varchar(15), order_total REAL);""")
# menu = [
#     ("Paneer Supreme", "veg", "small", 200),
#     ("Paneer Supreme", "veg", "medium", 250),
#     ("Paneer Supreme", "veg", "large", 350),
#     ("Veggie Supreme", "veg", "small", 170),
#     ("Veggie Supreme", "veg", "medium", 250),
#     ("Veggie Supreme", "veg", "large", 360),
#     ("Veg Exotica", "veg", "small", 240),
#     ("Veg Exotica", "veg", "medium", 330),
#     ("Veg Exotica", "veg", "large", 420),
#     ("Chicken Supreme", "non-veg", "small", 280),
#     ("Chicken Supreme", "non-veg", "medium", 380),
#     ("Chicken Supreme", "non-veg", "large", 480),
#     ("Pepper Chicken", "non-veg", "small", 295),
#     ("Pepper Chicken", "non-veg", "medium", 350),
#     ("Pepper Chicken", "non-veg", "large", 410),
#     ("Chicken Italiano", "non-veg", "small", 280),
#     ("Chicken Italiano", "non-veg", "medium", 390),
#     ("Chicken Italiano", "non-veg", "large", 420),
# ]
# cur.executemany("insert into pizza_menu(pizza, pizza_type, crust_type, cost) VALUES (?, ?, ?, ?);",menu);
# a = cur.execute("select * from pizza_menu where crust_type = :crust_type", {"crust_type": "small"})
# a = cur.execute("select sum(cost)==1080 from pizza_menu where id in (17,16,15)")
# print(a.fetchone())
# print(cur.execute(f"select * from pizza_menu where id in ({','.join(['?']*3)});", ['1','2','3']).fetchall())
# print(cur.execute("select * from orders").fetchall())
conn.commit()
conn.close()
