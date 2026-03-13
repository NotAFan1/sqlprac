import random

QUESTIONS = [
    {
        "id": "q11",
        "difficulty": "easy",
        "topic": "count",
        "prompt": "Return a single column `total_orders` representing the total number of rows in the `orders` table.",
        "expected_sql": """
    SELECT COUNT(*) AS total_orders
    FROM orders;
    """.strip(),
        "required_patterns": [
            {"label": "count rows", "pattern": r"count\s*\("},
            {"label": "from orders", "pattern": r"from\s+orders"}
        ],
        "concepts": ["COUNT"],
        "explanation": "Counts how many orders exist."
    },

    {
        "id": "q12",
        "difficulty": "medium",
        "topic": "grouping",
        "prompt": "Return the columns `state` and `customer_count`. Each row should represent a state.",
        "expected_sql": """
    SELECT state, COUNT(*) AS customer_count
    FROM customers
    GROUP BY state;
    """.strip(),
        "required_patterns": [
            {"label": "from customers", "pattern": r"from\s+customers"},
            {"label": "group by state", "pattern": r"group\s+by\s+.*state"},
            {"label": "count rows", "pattern": r"count\s*\("}
        ],
        "concepts": ["GROUP BY", "COUNT"],
        "explanation": "Counts customers per state."
    },

    {
        "id": "q13",
        "difficulty": "medium",
        "topic": "joins",
        "prompt": "Return the columns `order_id`, `first_name`, `last_name`, and `order_date`.",
        "expected_sql": """
    SELECT o.order_id, c.first_name, c.last_name, o.order_date
    FROM orders o
    JOIN customers c
    ON o.customer_id = c.customer_id;
    """.strip(),
        "required_patterns": [
            {"label": "join customers", "pattern": r"join\s+customers"},
            {"label": "customer_id join", "pattern": r"customer_id"}
        ],
        "concepts": ["JOIN"],
        "explanation": "Shows who placed each order."
    },

    {
        "id": "q14",
        "difficulty": "medium",
        "topic": "joins",
        "prompt": "Return the columns `product_name` and `supplier_name`.",
        "expected_sql": """
    SELECT p.product_name, s.supplier_name
    FROM products p
    JOIN product_suppliers ps
    ON p.product_id = ps.product_id
    JOIN suppliers s
    ON ps.supplier_id = s.supplier_id;
    """.strip(),
        "required_patterns": [
            {"label": "join product_suppliers", "pattern": r"join\s+product_suppliers"},
            {"label": "join suppliers", "pattern": r"join\s+suppliers"}
        ],
        "concepts": ["JOIN"],
        "explanation": "Shows which suppliers provide each product."
    },

    {
        "id": "q15",
        "difficulty": "medium",
        "topic": "aggregation",
        "prompt": "Return the columns `customer_id` and `total_orders`. Each row should represent a customer.",
        "expected_sql": """
    SELECT customer_id, COUNT(order_id) AS total_orders
    FROM orders
    GROUP BY customer_id;
    """.strip(),
        "required_patterns": [
            {"label": "group by customer", "pattern": r"group\s+by\s+.*customer_id"},
            {"label": "count orders", "pattern": r"count\s*\("}
        ],
        "concepts": ["GROUP BY", "COUNT"],
        "explanation": "Counts how many orders each customer has placed."
    },

    {
        "id": "q16",
        "difficulty": "hard",
        "topic": "aggregation",
        "prompt": "Return the columns `category` and `total_revenue`. Only include rows where `status = 'completed'`.",
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
        "required_patterns": [
            {"label": "join order_items", "pattern": r"join\s+order_items"},
            {"label": "join products", "pattern": r"join\s+products"},
            {"label": "sum revenue", "pattern": r"sum\s*\("}
        ],
        "concepts": ["JOIN", "SUM", "GROUP BY"],
        "explanation": "Computes revenue by category for completed orders."
    },

    {
        "id": "q17",
        "difficulty": "hard",
        "topic": "aggregation",
        "prompt": "Return the columns `first_name`, `last_name`, and `total_spent`. Only include rows where `status = 'completed'`. Order the results by `total_spent` in descending order and return the first 5 rows.",
        "expected_sql": """
    SELECT c.first_name, c.last_name, SUM(o.total_amount) AS total_spent
    FROM customers c
    JOIN orders o
    ON c.customer_id = o.customer_id
    WHERE o.status = 'completed'
    GROUP BY c.customer_id
    ORDER BY total_spent DESC
    LIMIT 5;
    """.strip(),
        "required_patterns": [
            {"label": "join orders", "pattern": r"join\s+orders"},
            {"label": "sum totals", "pattern": r"sum\s*\("},
            {"label": "limit results", "pattern": r"limit\s+5"}
        ],
        "concepts": ["JOIN", "SUM", "GROUP BY", "LIMIT"],
        "explanation": "Finds the highest-spending customers."
    },
    {
        "id": "q19",
        "difficulty": "hard",
        "topic": "having",
        "prompt": "Return the columns `product_name` and `review_count`. Only include rows where `review_count` is greater than 3. Order the results by `review_count` in descending order.",
        "expected_sql": """
    SELECT p.product_name, COUNT(r.review_id) AS review_count
    FROM products p
    JOIN reviews r
    ON p.product_id = r.product_id
    GROUP BY p.product_id
    HAVING COUNT(r.review_id) > 3
    ORDER BY review_count DESC;
    """.strip(),
        "required_patterns": [
            {"label": "join reviews", "pattern": r"join\s+reviews"},
            {"label": "count reviews", "pattern": r"count\s*\("},
            {"label": "having clause", "pattern": r"having\s+"}
        ],
        "concepts": ["JOIN", "GROUP BY", "HAVING", "COUNT"],
        "explanation": "Counts reviews per product and filters products with more than 3 reviews."
    },
    {
        "id": "q20",
        "difficulty": "hard",
        "topic": "joins_having_aggregation",
        "prompt": "Return the columns `state`, `customer_count`, and `avg_total_spent`. Each row should represent a state. Only include rows where `customer_count` is greater than 3. Order the results by `avg_total_spent` in descending order.",
        "expected_sql": """
    SELECT c.state, COUNT(DISTINCT c.customer_id) AS customer_count, ROUND(AVG(customer_totals.total_spent), 2) AS avg_total_spent
    FROM customers c
    JOIN (
        SELECT customer_id, SUM(total_amount) AS total_spent
        FROM orders
        WHERE status = 'completed'
        GROUP BY customer_id
    ) customer_totals
    ON c.customer_id = customer_totals.customer_id
    GROUP BY c.state
    HAVING COUNT(DISTINCT c.customer_id) > 3
    ORDER BY avg_total_spent DESC;
    """.strip(),
        "required_patterns": [
            {"label": "join derived customer totals", "pattern": r"join\s*\("},
            {"label": "group by state", "pattern": r"group\s+by\s+.*state"},
            {"label": "having customer count condition", "pattern": r"having\s+.*count\s*\("},
            {"label": "completed filter", "pattern": r"status\s*=\s*['\"]completed['\"]"}
        ],
        "concepts": ["JOIN", "SUBQUERY", "GROUP BY", "HAVING", "AVG", "SUM"],
        "explanation": "Computes customer spending first, then aggregates those customer totals by state."
    },
    {
        "id": "q21",
        "difficulty": "hard",
        "topic": "left_join_case_aggregation",
        "prompt": "Return the columns `employee_id`, `first_name`, `last_name`, `shipment_count`, and `shipping_tier`. Each row should represent an employee. Order the results by `shipment_count` in descending order.",
        "expected_sql": """
    SELECT e.employee_id, e.first_name, e.last_name,
        COUNT(s.shipment_id) AS shipment_count,
        CASE
            WHEN COUNT(s.shipment_id) >= 20 THEN 'High'
            WHEN COUNT(s.shipment_id) >= 10 THEN 'Medium'
            ELSE 'Low'
        END AS shipping_tier
    FROM employees e
    LEFT JOIN shipments s
    ON e.employee_id = s.employee_id
    GROUP BY e.employee_id, e.first_name, e.last_name
    ORDER BY shipment_count DESC;
    """.strip(),
        "required_patterns": [
            {"label": "left join shipments", "pattern": r"left\s+join\s+shipments"},
            {"label": "count shipments", "pattern": r"count\s*\(\s*.*shipment_id.*\)"},
            {"label": "case expression", "pattern": r"case\s+when"}
        ],
        "concepts": ["LEFT JOIN", "GROUP BY", "COUNT", "CASE"],
        "explanation": "Counts shipments per employee and assigns a label based on shipment volume."
    },
    {
        "id": "q22",
        "difficulty": "hard",
        "topic": "multi_join_distinct_having",
        "prompt": "Return the columns `supplier_name`, `product_count`, and `avg_price`. Each row should represent a supplier. Only include rows where `product_count` is at least 2. Order the results by `product_count` in descending order, then by `supplier_name` in ascending order.",
        "expected_sql": """
    SELECT s.supplier_name,
        COUNT(DISTINCT p.product_id) AS product_count,
        ROUND(AVG(p.price), 2) AS avg_price
    FROM suppliers s
    JOIN product_suppliers ps
    ON s.supplier_id = ps.supplier_id
    JOIN products p
    ON ps.product_id = p.product_id
    GROUP BY s.supplier_id, s.supplier_name
    HAVING COUNT(DISTINCT p.product_id) >= 2
    ORDER BY product_count DESC, supplier_name ASC;
    """.strip(),
        "required_patterns": [
            {"label": "join product_suppliers", "pattern": r"join\s+product_suppliers"},
            {"label": "join products", "pattern": r"join\s+products"},
            {"label": "count distinct products", "pattern": r"count\s*\(\s*distinct\s+.*product_id"},
            {"label": "having clause", "pattern": r"having\s+"}
        ],
        "concepts": ["JOIN", "COUNT DISTINCT", "AVG", "GROUP BY", "HAVING"],
        "explanation": "Aggregates product coverage and average price per supplier."
    },
    {
        "id": "q23",
        "difficulty": "hard",
        "topic": "subquery_top_per_group",
        "prompt": "Return the columns `category`, `product_name`, and `price`. Include only the product or products with the highest `price` within each category. Order the results by `category` in ascending order.",
        "expected_sql": """
    SELECT p.category, p.product_name, p.price
    FROM products p
    JOIN (
        SELECT category, MAX(price) AS max_price
        FROM products
        GROUP BY category
    ) mx
    ON p.category = mx.category
    AND p.price = mx.max_price
    ORDER BY p.category ASC;
    """.strip(),
        "required_patterns": [
            {"label": "subquery with max price", "pattern": r"select\s+category\s*,\s*max\s*\(\s*price\s*\)"},
            {"label": "join subquery", "pattern": r"join\s*\("},
            {"label": "match on category and price", "pattern": r"price\s*=\s*.*max_price"}
        ],
        "concepts": ["SUBQUERY", "MAX", "JOIN", "GROUP BY"],
        "explanation": "Finds the most expensive product in each category, including ties."
    },
    {
        "id": "q24",
        "difficulty": "hard",
        "topic": "cte_multi_stage_aggregation",
        "prompt": "Return the columns `customer_id`, `first_name`, `last_name`, `completed_orders`, and `avg_completed_order_value`. Each row should represent a customer. Only include rows where `completed_orders` is at least 2. Order the results by `avg_completed_order_value` in descending order.",
        "expected_sql": """
    WITH customer_stats AS (
        SELECT c.customer_id, c.first_name, c.last_name,
            COUNT(o.order_id) AS completed_orders,
            AVG(o.total_amount) AS avg_completed_order_value
        FROM customers c
        JOIN orders o
        ON c.customer_id = o.customer_id
        WHERE o.status = 'completed'
        GROUP BY c.customer_id, c.first_name, c.last_name
    )
    SELECT customer_id, first_name, last_name, completed_orders,
        ROUND(avg_completed_order_value, 2) AS avg_completed_order_value
    FROM customer_stats
    WHERE completed_orders >= 2
    ORDER BY avg_completed_order_value DESC;
    """.strip(),
        "required_patterns": [
            {"label": "cte usage", "pattern": r"with\s+customer_stats\s+as"},
            {"label": "completed filter", "pattern": r"status\s*=\s*['\"]completed['\"]"},
            {"label": "count orders", "pattern": r"count\s*\(\s*.*order_id.*\)"},
            {"label": "average total amount", "pattern": r"avg\s*\(\s*.*total_amount.*\)"}
        ],
        "concepts": ["CTE", "JOIN", "WHERE", "GROUP BY", "COUNT", "AVG"],
        "explanation": "Builds per-customer completed-order stats, then filters and sorts them."
    },
    {
        "id": "q25",
        "difficulty": "hard",
        "topic": "left_join_coalesce_inventory",
        "prompt": "Return the columns `warehouse_name`, `state`, `product_count`, and `total_stock`. Each row should represent a warehouse. Include warehouses even if they have no inventory rows. Order the results by `total_stock` in descending order.",
        "expected_sql": """
    SELECT w.warehouse_name, w.state,
        COUNT(DISTINCT i.product_id) AS product_count,
        COALESCE(SUM(i.stock_quantity), 0) AS total_stock
    FROM warehouses w
    LEFT JOIN inventory i
    ON w.warehouse_id = i.warehouse_id
    GROUP BY w.warehouse_id, w.warehouse_name, w.state
    ORDER BY total_stock DESC;
    """.strip(),
        "required_patterns": [
            {"label": "left join inventory", "pattern": r"left\s+join\s+inventory"},
            {"label": "coalesce sum", "pattern": r"coalesce\s*\(\s*sum\s*\("},
            {"label": "group by warehouse", "pattern": r"group\s+by\s+.*warehouse"}
        ],
        "concepts": ["LEFT JOIN", "COALESCE", "SUM", "COUNT DISTINCT", "GROUP BY"],
        "explanation": "Summarizes warehouse inventory while keeping warehouses with no stock rows."
    },
    {
        "id": "q26",
        "difficulty": "hard",
        "topic": "returns_multi_join_aggregation",
        "prompt": "Return the columns `category`, `return_count`, and `total_refund_amount`. Each row should represent a category. Only include returned items. Order the results by `total_refund_amount` in descending order.",
        "expected_sql": """
    SELECT p.category,
        COUNT(r.return_id) AS return_count,
        ROUND(SUM(r.refund_amount), 2) AS total_refund_amount
    FROM returns r
    JOIN order_items oi
    ON r.order_item_id = oi.order_item_id
    JOIN products p
    ON oi.product_id = p.product_id
    GROUP BY p.category
    ORDER BY total_refund_amount DESC;
    """.strip(),
        "required_patterns": [
            {"label": "join order_items", "pattern": r"join\s+order_items"},
            {"label": "join products", "pattern": r"join\s+products"},
            {"label": "count returns", "pattern": r"count\s*\(\s*.*return_id.*\)"},
            {"label": "sum refund", "pattern": r"sum\s*\(\s*.*refund_amount.*\)"}
        ],
        "concepts": ["JOIN", "COUNT", "SUM", "GROUP BY"],
        "explanation": "Traces returns back to product categories and aggregates refund activity."
    },
    {
        "id": "q27",
        "difficulty": "hard",
        "topic": "case_having_payments",
        "prompt": "Return the columns `payment_method`, `successful_payment_count`, `failed_payment_count`, and `total_paid_amount`. Each row should represent a payment method. Order the results by `total_paid_amount` in descending order.",
        "expected_sql": """
    SELECT payment_method,
        SUM(CASE WHEN payment_status = 'paid' THEN 1 ELSE 0 END) AS successful_payment_count,
        SUM(CASE WHEN payment_status <> 'paid' THEN 1 ELSE 0 END) AS failed_payment_count,
        ROUND(SUM(CASE WHEN payment_status = 'paid' THEN amount ELSE 0 END), 2) AS total_paid_amount
    FROM payments
    GROUP BY payment_method
    ORDER BY total_paid_amount DESC;
    """.strip(),
        "required_patterns": [
            {"label": "case when used", "pattern": r"case\s+when"},
            {"label": "group by payment method", "pattern": r"group\s+by\s+.*payment_method"},
            {"label": "sum conditional amount", "pattern": r"sum\s*\(\s*case\s+when\s+.*amount"}
        ],
        "concepts": ["CASE", "SUM", "GROUP BY"],
        "explanation": "Builds multiple aggregates per payment method using conditional logic."
    }
]
def get_question_by_id(question_id: str):
    return next((q for q in QUESTIONS if q["id"] == question_id), None)

def get_random_question(difficulty: str | None = None):
    pool = QUESTIONS
    if difficulty:
        pool = [q for q in QUESTIONS if q["difficulty"] == difficulty.lower()]
    return random.choice(pool) if pool else None