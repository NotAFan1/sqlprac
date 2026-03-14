import random

QUESTIONS = [

    {
    "id": "q1",
    "difficulty": "easy",
    "topic": "filtering",
    "prompt": "Find the columns `first_name`, `last_name`, and `state` of all customers who live in California. Order the results alphabetically by `last_name`.",
    "expected_sql": """
    SELECT first_name, last_name, state
    FROM customers
    WHERE state = 'CA'
    ORDER BY last_name ASC;
    """.strip(),
    "required_patterns":[
    {"label":"filter california","pattern":r"where\s+state\s*=\s*['\"]ca['\"]"},
    {"label":"order by last name","pattern":r"order\s+by\s+.*last_name"}
    ],
    "concepts":["WHERE","ORDER BY"],
    "explanation":"Filters customers living in California and sorts them alphabetically by last name."
    },

    {
    "id": "q2",
    "difficulty": "easy",
    "topic": "count",
    "prompt": "Return a single column `total_customers` representing the number of rows in the `customers` table.",
    "expected_sql": """
    SELECT COUNT(*) AS total_customers
    FROM customers;
    """.strip(),
    "required_patterns":[
    {"label":"count","pattern":r"count\s*\("},
    {"label":"from customers","pattern":r"from\s+customers"}
    ],
    "concepts":["COUNT"],
    "explanation":"Counts how many customers exist."
    },

    {
    "id": "q3",
    "difficulty": "easy",
    "topic": "filtering",
    "prompt": "Return the columns `product_name` and `price` for all products with a price greater than 100. Order by `price` descending.",
    "expected_sql": """
    SELECT product_name, price
    FROM products
    WHERE price > 100
    ORDER BY price DESC;
    """.strip(),
    "required_patterns":[
    {"label":"price filter","pattern":r"price\s*>\s*100"},
    {"label":"order price","pattern":r"order\s+by\s+.*price"}
    ],
    "concepts":["WHERE","ORDER BY"],
    "explanation":"Shows expensive products sorted from highest to lowest price."
    },

    {
    "id": "q4",
    "difficulty": "medium",
    "topic": "grouping",
    "prompt": "Return the columns `state` and `customer_count`. Each row should represent a state.",
    "expected_sql": """
    SELECT state, COUNT(*) AS customer_count
    FROM customers
    GROUP BY state;
    """.strip(),
    "required_patterns":[
    {"label":"group by state","pattern":r"group\s+by\s+.*state"},
    {"label":"count","pattern":r"count\s*\("}
    ],
    "concepts":["GROUP BY","COUNT"],
    "explanation":"Counts customers per state."
    },

    {
    "id": "q5",
    "difficulty": "medium",
    "topic": "joins",
    "prompt": "Return the columns `order_id`, `first_name`, `last_name`, and `order_date`.",
    "expected_sql": """
    SELECT o.order_id, c.first_name, c.last_name, o.order_date
    FROM orders o
    JOIN customers c
    ON o.customer_id = c.customer_id;
    """.strip(),
    "required_patterns":[
    {"label":"join customers","pattern":r"join\s+customers"},
    {"label":"customer id","pattern":r"customer_id"}
    ],
    "concepts":["JOIN"],
    "explanation":"Shows which customer placed each order."
    },

    {
    "id": "q6",
    "difficulty": "medium",
    "topic": "aggregation",
    "prompt": "Return the columns `category` and `product_count`. Each row should represent a category.",
    "expected_sql": """
    SELECT category, COUNT(product_id) AS product_count
    FROM products
    GROUP BY category;
    """.strip(),
    "required_patterns":[
    {"label":"group category","pattern":r"group\s+by\s+.*category"},
    {"label":"count product","pattern":r"count\s*\("}
    ],
    "concepts":["GROUP BY","COUNT"],
    "explanation":"Counts how many products exist in each category."
    },

    {
    "id": "q7",
    "difficulty": "medium",
    "topic": "aggregation",
    "prompt": "Return the columns `customer_id` and `total_orders`. Each row should represent a customer.",
    "expected_sql": """
    SELECT customer_id, COUNT(order_id) AS total_orders
    FROM orders
    GROUP BY customer_id;
    """.strip(),
    "required_patterns":[
    {"label":"group by customer","pattern":r"group\s+by\s+.*customer_id"},
    {"label":"count orders","pattern":r"count\s*\("}
    ],
    "concepts":["GROUP BY","COUNT"],
    "explanation":"Counts orders per customer."
    },

    {
    "id": "q8",
    "difficulty": "medium",
    "topic": "joins",
    "prompt": "Return the columns `product_name`, `supplier_name`.",
    "expected_sql": """
    SELECT p.product_name, s.supplier_name
    FROM products p
    JOIN product_suppliers ps
    ON p.product_id = ps.product_id
    JOIN suppliers s
    ON ps.supplier_id = s.supplier_id;
    """.strip(),
    "required_patterns":[
    {"label":"join product suppliers","pattern":r"join\s+product_suppliers"},
    {"label":"join suppliers","pattern":r"join\s+suppliers"}
    ],
    "concepts":["JOIN"],
    "explanation":"Shows which supplier provides each product."
    },

    {
    "id": "q9",
    "difficulty": "hard",
    "topic": "aggregation",
    "prompt": "Return the columns `category` and `total_revenue`. Only include orders where `status = 'completed'`.",
    "expected_sql": """
    SELECT p.category, SUM(oi.quantity * oi.unit_price) AS total_revenue
    FROM orders o
    JOIN order_items oi
    ON o.order_id = oi.order_id
    JOIN products p
    ON oi.product_id = p.product_id
    WHERE o.status = 'completed'
    GROUP BY p.category;
    """.strip(),
    "required_patterns":[
    {"label":"join order_items","pattern":r"join\s+order_items"},
    {"label":"sum revenue","pattern":r"sum\s*\("},
    {"label":"completed filter","pattern":r"status\s*=\s*['\"]completed['\"]"}
    ],
    "concepts":["JOIN","SUM","GROUP BY"],
    "explanation":"Calculates revenue per category from completed orders."
    },

    {
    "id": "q10",
    "difficulty": "hard",
    "topic": "having",
    "prompt": "Return the columns `category` and `avg_price`. Only include rows where `avg_price` is greater than 50. Round `avg_price` to 2 decimal places.",
    "expected_sql": """
    SELECT category, ROUND(AVG(price),2) AS avg_price
    FROM products
    GROUP BY category
    HAVING AVG(price) > 50;
    """.strip(),
    "required_patterns":[
    {"label":"having","pattern":r"having\s+"},
    {"label":"avg price","pattern":r"avg\s*\("},
    {"label":"round","pattern":r"round\s*\("}
    ],
    "concepts":["GROUP BY","HAVING","AVG"],
    "explanation":"Filters categories whose average product price is above 50."
    },

    {
    "id": "q11",
    "difficulty": "hard",
    "topic": "left_join",
    "prompt": "Return the columns `employee_id`, `first_name`, `last_name`, and `shipment_count`. Include employees even if they have no shipments.",
    "expected_sql": """
    SELECT e.employee_id, e.first_name, e.last_name, COUNT(s.shipment_id) AS shipment_count
    FROM employees e
    LEFT JOIN shipments s
    ON e.employee_id = s.employee_id
    GROUP BY e.employee_id, e.first_name, e.last_name;
    """.strip(),
    "required_patterns":[
    {"label":"left join shipments","pattern":r"left\s+join\s+shipments"},
    {"label":"count shipments","pattern":r"count\s*\("}
    ],
    "concepts":["LEFT JOIN","GROUP BY","COUNT"],
    "explanation":"Counts shipments per employee including employees with none."
    },

    {
    "id": "q12",
    "difficulty": "hard",
    "topic": "subquery",
    "prompt": "Return the columns `product_name` and `price`. Only include products with a price greater than the average product price.",
    "expected_sql": """
    SELECT product_name, price
    FROM products
    WHERE price > (
    SELECT AVG(price)
    FROM products
    );
    """.strip(),
    "required_patterns":[
    {"label":"subquery avg","pattern":r"avg\s*\(\s*price"},
    {"label":"nested select","pattern":r"select\s+avg"}
    ],
    "concepts":["SUBQUERY","AVG"],
    "explanation":"Finds products priced above the overall average."
    },

    {
    "id": "q13",
    "difficulty": "hard",
    "topic": "distinct_having",
    "prompt": "Return the columns `supplier_name` and `product_count`. Only include suppliers that supply at least 2 products.",
    "expected_sql": """
    SELECT s.supplier_name, COUNT(DISTINCT ps.product_id) AS product_count
    FROM suppliers s
    JOIN product_suppliers ps
    ON s.supplier_id = ps.supplier_id
    GROUP BY s.supplier_id, s.supplier_name
    HAVING COUNT(DISTINCT ps.product_id) >= 2;
    """.strip(),
    "required_patterns":[
    {"label":"count distinct","pattern":r"count\s*\(\s*distinct"},
    {"label":"having","pattern":r"having\s+"}
    ],
    "concepts":["COUNT DISTINCT","GROUP BY","HAVING"],
    "explanation":"Counts products per supplier and filters suppliers with at least two."
    },

    {
    "id": "q14",
    "difficulty": "hard",
    "topic": "case",
    "prompt": "Return the columns `product_name`, `price`, and `price_tier` where price_tier is 'High' if price >= 100, 'Medium' if price >= 50, otherwise 'Low'.",
    "expected_sql": """
    SELECT product_name, price,
    CASE
    WHEN price >= 100 THEN 'High'
    WHEN price >= 50 THEN 'Medium'
    ELSE 'Low'
    END AS price_tier
    FROM products;
    """.strip(),
    "required_patterns":[
    {"label":"case when","pattern":r"case\s+when"}
    ],
    "concepts":["CASE"],
    "explanation":"Categorizes products based on price."
    },

    {
    "id": "q15",
    "difficulty": "hard",
    "topic": "coalesce",
    "prompt": "Return the columns `warehouse_name`, `state`, and `total_stock`. Warehouses with no inventory should show 0.",
    "expected_sql": """
    SELECT w.warehouse_name, w.state,
    COALESCE(SUM(i.stock_quantity),0) AS total_stock
    FROM warehouses w
    LEFT JOIN inventory i
    ON w.warehouse_id = i.warehouse_id
    GROUP BY w.warehouse_id, w.warehouse_name, w.state;
    """.strip(),
    "required_patterns":[
    {"label":"coalesce","pattern":r"coalesce"},
    {"label":"left join inventory","pattern":r"left\s+join\s+inventory"}
    ],
    "concepts":["COALESCE","LEFT JOIN","SUM"],
    "explanation":"Ensures warehouses without stock show 0 instead of NULL."
    },

    {
    "id": "q16",
    "difficulty": "hard",
    "topic": "top_per_group",
    "prompt": "Return the columns `category`, `product_name`, and `price`. Only include the most expensive product in each category.",
    "expected_sql": """
    SELECT p.category, p.product_name, p.price
    FROM products p
    JOIN (
    SELECT category, MAX(price) AS max_price
    FROM products
    GROUP BY category
    ) mx
    ON p.category = mx.category
    AND p.price = mx.max_price;
    """.strip(),
    "required_patterns":[
    {"label":"max price subquery","pattern":r"max\s*\(\s*price"},
    {"label":"join subquery","pattern":r"join\s*\("}
    ],
    "concepts":["SUBQUERY","MAX","JOIN"],
    "explanation":"Finds the highest priced product per category."
    },

    {
    "id": "q17",
    "difficulty": "hard",
    "topic": "cte",
    "prompt": "Return the columns `customer_id`, `total_spent`. Only include completed orders.",
    "expected_sql": """
    WITH customer_totals AS (
    SELECT customer_id, SUM(total_amount) AS total_spent
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
    )
    SELECT customer_id, total_spent
    FROM customer_totals;
    """.strip(),
    "required_patterns":[
    {"label":"cte","pattern":r"with\s+"},
    {"label":"sum","pattern":r"sum\s*\("}
    ],
    "concepts":["CTE","SUM","GROUP BY"],
    "explanation":"Uses a CTE to compute spending per customer."
    },

    {
    "id": "q18",
    "difficulty": "hard",
    "topic": "multi_join",
    "prompt": "Return the columns `product_name` and `total_quantity_sold`.",
    "expected_sql": """
    SELECT p.product_name, SUM(oi.quantity) AS total_quantity_sold
    FROM products p
    JOIN order_items oi
    ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name;
    """.strip(),
    "required_patterns":[
    {"label":"join order_items","pattern":r"join\s+order_items"},
    {"label":"sum quantity","pattern":r"sum\s*\("}
    ],
    "concepts":["JOIN","SUM","GROUP BY"],
    "explanation":"Counts total units sold per product."
    },

    {
    "id": "q19",
    "difficulty": "hard",
    "topic": "reviews",
    "prompt": "Return the columns `product_name` and `review_count`. Only include products with more than 3 reviews.",
    "expected_sql": """
    SELECT p.product_name, COUNT(r.review_id) AS review_count
    FROM products p
    JOIN reviews r
    ON p.product_id = r.product_id
    GROUP BY p.product_id, p.product_name
    HAVING COUNT(r.review_id) > 3;
    """.strip(),
    "required_patterns":[
    {"label":"join reviews","pattern":r"join\s+reviews"},
    {"label":"having","pattern":r"having\s+"}
    ],
    "concepts":["JOIN","GROUP BY","HAVING"],
    "explanation":"Filters products with many reviews."
    },

    {
    "id": "q20",
    "difficulty": "hard",
    "topic": "returns",
    "prompt": "Return the columns `category` and `total_refund_amount`. Round the refund amount to 2 decimal places.",
    "expected_sql": """
    SELECT p.category, ROUND(SUM(r.refund_amount),2) AS total_refund_amount
    FROM returns r
    JOIN order_items oi
    ON r.order_item_id = oi.order_item_id
    JOIN products p
    ON oi.product_id = p.product_id
    GROUP BY p.category;
    """.strip(),
    "required_patterns":[
    {"label":"join order_items","pattern":r"join\s+order_items"},
    {"label":"sum refund","pattern":r"sum\s*\("},
    {"label":"round","pattern":r"round\s*\("}
    ],
    "concepts":["JOIN","SUM","ROUND"],
    "explanation":"Aggregates refund totals by product category."
    },

    {
    "id": "q21",
    "difficulty": "hard",
    "topic": "case",
    "prompt": "Return the columns `payment_method`, `successful_payments`, and `failed_payments`.",
    "expected_sql": """
    SELECT payment_method,
    SUM(CASE WHEN payment_status = 'paid' THEN 1 ELSE 0 END) AS successful_payments,
    SUM(CASE WHEN payment_status <> 'paid' THEN 1 ELSE 0 END) AS failed_payments
    FROM payments
    GROUP BY payment_method;
    """.strip(),
    "required_patterns":[
    {"label":"case when","pattern":r"case\s+when"}
    ],
    "concepts":["CASE","GROUP BY"],
    "explanation":"Counts successful vs failed payments."
    },

    {
    "id": "q22",
    "difficulty": "hard",
    "topic": "nested_avg",
    "prompt": "Return the columns `first_name`, `last_name`, and `total_spent` for customers whose total spending is greater than the average customer spending.",
    "expected_sql": """
    SELECT c.first_name, c.last_name, SUM(o.total_amount) AS total_spent
    FROM customers c
    JOIN orders o
    ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
    HAVING SUM(o.total_amount) >
    (
    SELECT AVG(total_spent)
    FROM (
    SELECT SUM(total_amount) AS total_spent
    FROM orders
    GROUP BY customer_id
    ) t
    );
    """.strip(),
    "required_patterns":[
    {"label":"nested query","pattern":r"select\s+avg"},
    {"label":"having","pattern":r"having\s+"}
    ],
    "concepts":["SUBQUERY","HAVING","AVG","SUM"],
    "explanation":"Finds customers spending more than the average customer."
    },

    {
    "id": "q23",
    "difficulty": "hard",
    "topic": "inventory",
    "prompt": "Return the columns `warehouse_name` and `product_count` representing how many products are stocked in each warehouse.",
    "expected_sql": """
    SELECT w.warehouse_name, COUNT(DISTINCT i.product_id) AS product_count
    FROM warehouses w
    LEFT JOIN inventory i
    ON w.warehouse_id = i.warehouse_id
    GROUP BY w.warehouse_name;
    """.strip(),
    "required_patterns":[
    {"label":"count distinct","pattern":r"count\s*\(\s*distinct"}
    ],
    "concepts":["COUNT DISTINCT","LEFT JOIN"],
    "explanation":"Counts distinct products stored in each warehouse."
    },

    {
    "id": "q24",
    "difficulty": "hard",
    "topic": "review_avg",
    "prompt": "Return the columns `product_name` and `avg_rating`. Round avg_rating to 2 decimals.",
    "expected_sql": """
    SELECT p.product_name, ROUND(AVG(r.rating),2) AS avg_rating
    FROM products p
    JOIN reviews r
    ON p.product_id = r.product_id
    GROUP BY p.product_name;
    """.strip(),
    "required_patterns":[
    {"label":"avg rating","pattern":r"avg\s*\("},
    {"label":"round","pattern":r"round\s*\("}
    ],
    "concepts":["AVG","ROUND","GROUP BY"],
    "explanation":"Calculates average product rating."
    },

    {
    "id": "q25",
    "difficulty": "hard",
    "topic": "complex_join",
    "prompt": "Return the columns `state` and `total_revenue`. Only include completed orders. Round revenue to 2 decimals.",
    "expected_sql": """
    SELECT c.state, ROUND(SUM(o.total_amount),2) AS total_revenue
    FROM customers c
    JOIN orders o
    ON c.customer_id = o.customer_id
    WHERE o.status = 'completed'
    GROUP BY c.state;
    """.strip(),
    "required_patterns":[
    {"label":"join orders","pattern":r"join\s+orders"},
    {"label":"completed filter","pattern":r"status\s*=\s*['\"]completed['\"]"},
    {"label":"sum","pattern":r"sum\s*\("}
    ],
    "concepts":["JOIN","SUM","GROUP BY"],
    "explanation":"Calculates revenue generated per state from completed orders."
    }

]
def get_question_by_id(question_id: str):
    return next((q for q in QUESTIONS if q["id"] == question_id), None)

def get_random_question(difficulty: str | None = None):
    pool = QUESTIONS
    if difficulty:
        pool = [q for q in QUESTIONS if q["difficulty"] == difficulty.lower()]
    return random.choice(pool) if pool else None