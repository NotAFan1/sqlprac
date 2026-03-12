import os
import random
import sqlite3
from faker import Faker
from datetime import date

fake = Faker()
random.seed(42)
Faker.seed(42)

DB_PATH = "db.sqlite"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS returns;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS warehouses;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS shipments;
DROP TABLE IF EXISTS product_suppliers;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS discounts;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    state TEXT NOT NULL,
    city TEXT NOT NULL,
    signup_date TEXT NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    price REAL NOT NULL
);

CREATE TABLE suppliers (
    supplier_id INTEGER PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    country TEXT NOT NULL,
    rating REAL NOT NULL
);

CREATE TABLE product_suppliers (
    product_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    PRIMARY KEY (product_id, supplier_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    department TEXT NOT NULL,
    role TEXT NOT NULL,
    hire_date TEXT NOT NULL,
    salary REAL NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    total_amount REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE shipments (
    shipment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    shipment_date TEXT NOT NULL,
    carrier TEXT NOT NULL,
    shipping_cost REAL NOT NULL,
    delivery_status TEXT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    payment_date TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_status TEXT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    review_date TEXT NOT NULL,
    review_text TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE warehouses (
    warehouse_id INTEGER PRIMARY KEY,
    warehouse_name TEXT NOT NULL,
    state TEXT NOT NULL
);

CREATE TABLE inventory (
    warehouse_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    stock_quantity INTEGER NOT NULL,
    reorder_level INTEGER NOT NULL,
    PRIMARY KEY (warehouse_id, product_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE discounts (
    discount_id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    percent_off REAL NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL
);

CREATE TABLE returns (
    return_id INTEGER PRIMARY KEY,
    order_item_id INTEGER NOT NULL,
    return_date TEXT NOT NULL,
    reason TEXT NOT NULL,
    refund_amount REAL NOT NULL,
    FOREIGN KEY (order_item_id) REFERENCES order_items(order_item_id)
);
""")

states = ["CA", "NY", "TX", "WA", "FL", "IL", "AZ", "CO"]
cities_by_state = {
    "CA": ["Los Angeles", "San Diego", "San Jose", "Sacramento"],
    "NY": ["New York", "Buffalo", "Albany", "Rochester"],
    "TX": ["Austin", "Dallas", "Houston", "San Antonio"],
    "WA": ["Seattle", "Tacoma", "Spokane"],
    "FL": ["Miami", "Orlando", "Tampa"],
    "IL": ["Chicago", "Naperville", "Springfield"],
    "AZ": ["Phoenix", "Tucson", "Mesa"],
    "CO": ["Denver", "Boulder", "Aurora"],
}

categories = {
    "Electronics": ["Keyboard", "Mouse", "Monitor", "Headphones", "Webcam", "Speaker"],
    "Office": ["Notebook", "Pen Pack", "Stapler", "Desk Organizer", "Printer Paper"],
    "Home": ["Lamp", "Blanket", "Mug", "Storage Bin", "Chair Cushion"],
    "Fitness": ["Yoga Mat", "Dumbbell", "Resistance Band", "Foam Roller"],
    "Books": ["Novel", "Cookbook", "Textbook", "Planner"],
    "Gaming": ["Controller", "Gaming Mousepad", "Desk Mat", "USB Hub"],
}

payment_methods = ["credit_card", "debit_card", "paypal", "apple_pay"]
payment_statuses = ["paid", "failed", "refunded"]
order_statuses = ["completed", "pending", "cancelled"]
carriers = ["UPS", "FedEx", "USPS", "DHL"]
delivery_statuses = ["delivered", "in_transit", "processing", "delayed"]
departments = ["Operations", "Shipping", "Support", "Sales"]
roles = ["Associate", "Manager", "Coordinator", "Specialist"]
return_reasons = ["Damaged", "Wrong item", "No longer needed", "Late delivery", "Defective"]
supplier_countries = ["USA", "China", "Germany", "Mexico", "Canada", "Japan"]

# Customers
customers = []
for customer_id in range(1, 61):
    state = random.choice(states)
    city = random.choice(cities_by_state[state])
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}{customer_id}@example.com"
    signup_date = str(fake.date_between(start_date="-3y", end_date="-30d"))
    customers.append((customer_id, first_name, last_name, email, state, city, signup_date))

cur.executemany("""
INSERT INTO customers (customer_id, first_name, last_name, email, state, city, signup_date)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", customers)

# Products
products = []
product_id = 1
for category, subcats in categories.items():
    for _ in range(6):
        subcategory = random.choice(subcats)
        name = f"{fake.color_name()} {subcategory}"
        price = round(random.uniform(8, 500), 2)
        products.append((product_id, name, category, subcategory, price))
        product_id += 1

cur.executemany("""
INSERT INTO products (product_id, product_name, category, subcategory, price)
VALUES (?, ?, ?, ?, ?)
""", products)

# Suppliers
suppliers = []
for supplier_id in range(1, 13):
    suppliers.append((
        supplier_id,
        fake.company(),
        random.choice(supplier_countries),
        round(random.uniform(3.2, 5.0), 1)
    ))

cur.executemany("""
INSERT INTO suppliers (supplier_id, supplier_name, country, rating)
VALUES (?, ?, ?, ?)
""", suppliers)

# Product suppliers
product_suppliers = []
for p in products:
    pid = p[0]
    chosen = random.sample(range(1, 13), k=random.choice([1, 2, 2, 3]))
    for sid in chosen:
        product_suppliers.append((pid, sid))

cur.executemany("""
INSERT INTO product_suppliers (product_id, supplier_id)
VALUES (?, ?)
""", product_suppliers)

# Employees
employees = []
for employee_id in range(1, 16):
    employees.append((
        employee_id,
        fake.first_name(),
        fake.last_name(),
        random.choice(departments),
        random.choice(roles),
        str(fake.date_between(start_date="-6y", end_date="-90d")),
        round(random.uniform(42000, 98000), 2)
    ))

cur.executemany("""
INSERT INTO employees (employee_id, first_name, last_name, department, role, hire_date, salary)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", employees)

# Warehouses
warehouses = [
    (1, "West Hub", "CA"),
    (2, "Central Hub", "TX"),
    (3, "East Hub", "NY"),
    (4, "Mountain Hub", "CO"),
]
cur.executemany("""
INSERT INTO warehouses (warehouse_id, warehouse_name, state)
VALUES (?, ?, ?)
""", warehouses)

# Inventory
inventory = []
for warehouse_id, _, _ in warehouses:
    for p in products:
        product_id = p[0]
        stock_quantity = random.randint(0, 250)
        reorder_level = random.randint(10, 40)
        inventory.append((warehouse_id, product_id, stock_quantity, reorder_level))

cur.executemany("""
INSERT INTO inventory (warehouse_id, product_id, stock_quantity, reorder_level)
VALUES (?, ?, ?, ?)
""", inventory)

# Discounts
discount_categories = random.sample(list(categories.keys()), k=4)
discounts = []
for discount_id, category in enumerate(discount_categories, start=1):
    start_date = fake.date_between(start_date="-180d", end_date="-30d")
    end_date = fake.date_between(start_date=start_date, end_date="+60d")
    discounts.append((
        discount_id,
        category,
        round(random.choice([5, 10, 15, 20, 25]), 2),
        str(start_date),
        str(end_date)
    ))

cur.executemany("""
INSERT INTO discounts (discount_id, category, percent_off, start_date, end_date)
VALUES (?, ?, ?, ?, ?)
""", discounts)

# Orders and order_items
orders = []
order_items = []
order_id = 1
order_item_id = 1

for _ in range(180):
    customer_id = random.randint(1, 60)
    order_date = str(fake.date_between(start_date="-2y", end_date="today"))
    status = random.choices(order_statuses, weights=[0.65, 0.2, 0.15], k=1)[0]

    num_items = random.randint(1, 4)
    chosen_products = random.sample(products, k=num_items)

    current_items = []
    total_amount = 0.0

    for p in chosen_products:
        product_id = p[0]
        base_price = p[4]
        quantity = random.randint(1, 5)

        # small price variation to simulate sale pricing
        unit_price = round(base_price * random.uniform(0.85, 1.05), 2)
        total_amount += quantity * unit_price

        current_items.append((order_item_id, order_id, product_id, quantity, unit_price))
        order_item_id += 1

    if status == "cancelled":
        total_amount = 0.0

    orders.append((order_id, customer_id, order_date, status, round(total_amount, 2)))
    order_items.extend(current_items)
    order_id += 1

cur.executemany("""
INSERT INTO orders (order_id, customer_id, order_date, status, total_amount)
VALUES (?, ?, ?, ?, ?)
""", orders)

cur.executemany("""
INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price)
VALUES (?, ?, ?, ?, ?)
""", order_items)

# Shipments for completed and some pending orders
shipments = []
shipment_id = 1
for oid, _, order_date, status, total_amount in orders:
    if status == "completed":
        shipment_date = str(fake.date_between(start_date=date.fromisoformat(order_date), end_date="today"))
        shipments.append((
            shipment_id,
            oid,
            random.randint(1, 15),
            shipment_date,
            random.choice(carriers),
            round(random.uniform(4.99, 24.99), 2),
            random.choices(delivery_statuses, weights=[0.6, 0.15, 0.15, 0.1], k=1)[0]
        ))
        shipment_id += 1
    elif status == "pending" and random.random() < 0.25:
        shipment_date = str(fake.date_between(start_date=date.fromisoformat(order_date), end_date="today"))
        shipments.append((
            shipment_id,
            oid,
            random.randint(1, 15),
            shipment_date,
            random.choice(carriers),
            round(random.uniform(4.99, 24.99), 2),
            "processing"
        ))
        shipment_id += 1

cur.executemany("""
INSERT INTO shipments (shipment_id, order_id, employee_id, shipment_date, carrier, shipping_cost, delivery_status)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", shipments)

# Payments
payments = []
payment_id = 1
for oid, _, order_date, status, total_amount in orders:
    if status == "cancelled":
        payments.append((
            payment_id,
            oid,
            order_date,
            random.choice(payment_methods),
            0.0,
            "failed"
        ))
    else:
        pay_status = "paid" if status == "completed" else random.choice(["paid", "failed"])
        amount = total_amount if pay_status == "paid" else 0.0
        payments.append((
            payment_id,
            oid,
            order_date,
            random.choice(payment_methods),
            round(amount, 2),
            pay_status
        ))
    payment_id += 1

cur.executemany("""
INSERT INTO payments (payment_id, order_id, payment_date, payment_method, amount, payment_status)
VALUES (?, ?, ?, ?, ?, ?)
""", payments)

# Reviews
reviews = []
review_id = 1
completed_order_product_pairs = []

for oi_id, oid, pid, quantity, unit_price in order_items:
    status = next(o[3] for o in orders if o[0] == oid)
    customer_id = next(o[1] for o in orders if o[0] == oid)
    if status == "completed":
        completed_order_product_pairs.append((customer_id, pid))

sample_pairs = random.sample(completed_order_product_pairs, k=min(120, len(completed_order_product_pairs)))

for customer_id, product_id in sample_pairs:
    reviews.append((
        review_id,
        customer_id,
        product_id,
        random.randint(2, 5),
        str(fake.date_between(start_date="-1y", end_date="today")),
        fake.sentence(nb_words=10)
    ))
    review_id += 1

cur.executemany("""
INSERT INTO reviews (review_id, customer_id, product_id, rating, review_date, review_text)
VALUES (?, ?, ?, ?, ?, ?)
""", reviews)

# Returns - only from completed orders
returns = []
return_id = 1
completed_items = []
for item in order_items:
    oi_id, oid, pid, qty, unit_price = item
    status = next(o[3] for o in orders if o[0] == oid)
    if status == "completed":
        completed_items.append(item)

for oi_id, oid, pid, qty, unit_price in random.sample(completed_items, k=min(35, len(completed_items))):
    refund_qty = random.randint(1, qty)
    refund_amount = round(refund_qty * unit_price, 2)
    returns.append((
        return_id,
        oi_id,
        str(fake.date_between(start_date="-180d", end_date="today")),
        random.choice(return_reasons),
        refund_amount
    ))
    return_id += 1

cur.executemany("""
INSERT INTO returns (return_id, order_item_id, return_date, reason, refund_amount)
VALUES (?, ?, ?, ?, ?)
""", returns)

conn.commit()

# Quick counts
tables = [
    "customers", "products", "suppliers", "product_suppliers", "employees",
    "orders", "order_items", "shipments", "payments", "reviews",
    "warehouses", "inventory", "discounts", "returns"
]

print("Created db.sqlite")
for table in tables:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"{table}: {cur.fetchone()[0]}")

conn.close()