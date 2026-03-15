import random

QUESTIONS = [

    {
    "id": "q1",
    "difficulty": "easy",
    "topic": "filtering",
    "prompt": "Find the columns `title`, `release_year`, and `country` of all shows released after 2020. Order the results by `release_year` descending.",
    "expected_sql": """
    SELECT title, release_year, country
    FROM shows
    WHERE release_year > 2020
    ORDER BY release_year DESC;
    """.strip(),
    "required_patterns":[
    {"label":"release year filter","pattern":r"where\s+release_year\s*>\s*2020"},
    {"label":"order by release year","pattern":r"order\s+by\s+.*release_year"}
    ],
    "concepts":["WHERE","ORDER BY"],
    "explanation":"Filters shows released after 2020 and sorts them from newest to oldest."
    },

    {
    "id": "q2",
    "difficulty": "easy",
    "topic": "count",
    "prompt": "Return a single column `total_users` representing the number of rows in the `users` table.",
    "expected_sql": """
    SELECT COUNT(*) AS total_users
    FROM users;
    """.strip(),
    "required_patterns":[
    {"label":"count","pattern":r"count\s*\("},
    {"label":"from users","pattern":r"from\s+users"}
    ],
    "concepts":["COUNT"],
    "explanation":"Counts how many users exist in the users table."
    },

    {
    "id": "q3",
    "difficulty": "easy",
    "topic": "filtering",
    "prompt": "Return the columns `first_name`, `last_name`, and `country` for all users from Canada. Order by `last_name` ascending.",
    "expected_sql": """
    SELECT first_name, last_name, country
    FROM users
    WHERE country = 'Canada'
    ORDER BY last_name ASC;
    """.strip(),
    "required_patterns":[
    {"label":"country filter","pattern":r"where\s+country\s*=\s*['\"]canada['\"]"},
    {"label":"order by last name","pattern":r"order\s+by\s+.*last_name"}
    ],
    "concepts":["WHERE","ORDER BY"],
    "explanation":"Shows all users from Canada sorted alphabetically by last name."
    },

    {
    "id": "q4",
    "difficulty": "easy",
    "topic": "filtering",
    "prompt": "Return the columns `plan_name` and `monthly_price` for all subscription plans with a monthly price less than 15. Order by `monthly_price` ascending.",
    "expected_sql": """
    SELECT plan_name, monthly_price
    FROM subscription_plans
    WHERE monthly_price < 15
    ORDER BY monthly_price ASC;
    """.strip(),
    "required_patterns":[
    {"label":"price filter","pattern":r"monthly_price\s*<\s*15"},
    {"label":"order by price","pattern":r"order\s+by\s+.*monthly_price"}
    ],
    "concepts":["WHERE","ORDER BY"],
    "explanation":"Finds lower-priced subscription plans and sorts them from cheapest to most expensive."
    },

    {
    "id": "q5",
    "difficulty": "easy",
    "topic": "count",
    "prompt": "Return a single column `total_profiles` representing the number of rows in the `profiles` table.",
    "expected_sql": """
    SELECT COUNT(*) AS total_profiles
    FROM profiles;
    """.strip(),
    "required_patterns":[
    {"label":"count","pattern":r"count\s*\("},
    {"label":"from profiles","pattern":r"from\s+profiles"}
    ],
    "concepts":["COUNT"],
    "explanation":"Counts how many profiles exist in the profiles table."
    },

    {
    "id": "q6",
    "difficulty": "medium",
    "topic": "grouping",
    "prompt": "Return the columns `country` and `user_count`. Each row should represent a country.",
    "expected_sql": """
    SELECT country, COUNT(*) AS user_count
    FROM users
    GROUP BY country;
    """.strip(),
    "required_patterns":[
    {"label":"group by country","pattern":r"group\s+by\s+.*country"},
    {"label":"count","pattern":r"count\s*\("}
    ],
    "concepts":["GROUP BY","COUNT"],
    "explanation":"Counts how many users belong to each country."
    },

    {
    "id": "q7",
    "difficulty": "medium",
    "topic": "joins",
    "prompt": "Return the columns `profile_name`, `first_name`, and `last_name`.",
    "expected_sql": """
    SELECT p.profile_name, u.first_name, u.last_name
    FROM profiles p
    JOIN users u
    ON p.user_id = u.user_id;
    """.strip(),
    "required_patterns":[
    {"label":"join users","pattern":r"join\s+users"},
    {"label":"user id join","pattern":r"user_id"}
    ],
    "concepts":["JOIN"],
    "explanation":"Shows which user owns each profile."
    },

    {
    "id": "q8",
    "difficulty": "medium",
    "topic": "aggregation",
    "prompt": "Return the columns `content_type` and `show_count`. Each row should represent a content type.",
    "expected_sql": """
    SELECT content_type, COUNT(show_id) AS show_count
    FROM shows
    GROUP BY content_type;
    """.strip(),
    "required_patterns":[
    {"label":"group by content type","pattern":r"group\s+by\s+.*content_type"},
    {"label":"count shows","pattern":r"count\s*\("}
    ],
    "concepts":["GROUP BY","COUNT"],
    "explanation":"Counts how many shows belong to each content type."
    },

    {
    "id": "q9",
    "difficulty": "medium",
    "topic": "joins",
    "prompt": "Return the columns `title` and `genre_name`.",
    "expected_sql": """
    SELECT s.title, g.genre_name
    FROM shows s
    JOIN show_genres sg
    ON s.show_id = sg.show_id
    JOIN genres g
    ON sg.genre_id = g.genre_id;
    """.strip(),
    "required_patterns":[
    {"label":"join show genres","pattern":r"join\s+show_genres"},
    {"label":"join genres","pattern":r"join\s+genres"}
    ],
    "concepts":["JOIN"],
    "explanation":"Shows the genres associated with each show."
    },

    {
    "id": "q10",
    "difficulty": "medium",
    "topic": "aggregation",
    "prompt": "Return the columns `show_id` and `season_count`. Each row should represent a show.",
    "expected_sql": """
    SELECT show_id, COUNT(season_id) AS season_count
    FROM seasons
    GROUP BY show_id;
    """.strip(),
    "required_patterns":[
    {"label":"group by show","pattern":r"group\s+by\s+.*show_id"},
    {"label":"count seasons","pattern":r"count\s*\("}
    ],
    "concepts":["GROUP BY","COUNT"],
    "explanation":"Counts how many seasons each show has."
    },

    {
    "id": "q11",
    "difficulty": "medium",
    "topic": "joins",
    "prompt": "Return the columns `episode_title`, `season_number`, and `show_title`, where `episode_title` is the title of the episode and `show_title` is the title of the show.",
    "expected_sql": """
    SELECT e.title AS episode_title, s.season_number, sh.title AS show_title
    FROM episodes e
    JOIN seasons s
    ON e.season_id = s.season_id
    JOIN shows sh
    ON s.show_id = sh.show_id;
    """.strip(),
    "required_patterns":[
    {"label":"join seasons","pattern":r"join\s+seasons"},
    {"label":"join shows","pattern":r"join\s+shows"}
    ],
    "concepts":["JOIN"],
    "explanation":"Connects episodes to their seasons and shows."
    },

    {
    "id": "q12",
    "difficulty": "medium",
    "topic": "grouping",
    "prompt": "Return the columns `status` and `subscription_count`. Each row should represent a subscription status.",
    "expected_sql": """
    SELECT status, COUNT(subscription_id) AS subscription_count
    FROM subscriptions
    GROUP BY status;
    """.strip(),
    "required_patterns":[
    {"label":"group by status","pattern":r"group\s+by\s+.*status"},
    {"label":"count subscriptions","pattern":r"count\s*\("}
    ],
    "concepts":["GROUP BY","COUNT"],
    "explanation":"Counts how many subscriptions fall under each status."
    },

    {
    "id": "q13",
    "difficulty": "medium",
    "topic": "aggregation",
    "prompt": "Return the columns `show_id` and `avg_rating`. Round `avg_rating` to 2 decimal places.",
    "expected_sql": """
    SELECT show_id, ROUND(AVG(rating), 2) AS avg_rating
    FROM ratings
    GROUP BY show_id;
    """.strip(),
    "required_patterns":[
    {"label":"avg rating","pattern":r"avg\s*\("},
    {"label":"round","pattern":r"round\s*\("},
    {"label":"group by show","pattern":r"group\s+by\s+.*show_id"}
    ],
    "concepts":["AVG","ROUND","GROUP BY"],
    "explanation":"Calculates the average rating for each show."
    },

    {
    "id": "q14",
    "difficulty": "medium",
    "topic": "joins",
    "prompt": "Return the columns `title`, `first_name`, and `last_name` for each show and actor in its cast.",
    "expected_sql": """
    SELECT s.title, a.first_name, a.last_name
    FROM shows s
    JOIN show_cast sc
    ON s.show_id = sc.show_id
    JOIN actors a
    ON sc.actor_id = a.actor_id;
    """.strip(),
    "required_patterns":[
    {"label":"join show cast","pattern":r"join\s+show_cast"},
    {"label":"join actors","pattern":r"join\s+actors"}
    ],
    "concepts":["JOIN"],
    "explanation":"Shows which actors appear in each show."
    },

    {
    "id": "q15",
    "difficulty": "medium",
    "topic": "having",
    "prompt": "Return the columns `payment_method` and `payment_count`. Only include payment methods that appear at least 2 times.",
    "expected_sql": """
    SELECT payment_method, COUNT(payment_id) AS payment_count
    FROM payments
    GROUP BY payment_method
    HAVING COUNT(payment_id) >= 2;
    """.strip(),
    "required_patterns":[
    {"label":"group by payment method","pattern":r"group\s+by\s+.*payment_method"},
    {"label":"having","pattern":r"having\s+"},
    {"label":"count payments","pattern":r"count\s*\("}
    ],
    "concepts":["GROUP BY","COUNT","HAVING"],
    "explanation":"Counts payments by method and filters to methods used at least twice."
    }

]
def get_question_by_id(question_id: str):
    return next((q for q in QUESTIONS if q["id"] == question_id), None)

def get_random_question(difficulty: str | None = None):
    pool = QUESTIONS
    if difficulty:
        pool = [q for q in QUESTIONS if q["difficulty"] == difficulty.lower()]
    return random.choice(pool) if pool else None