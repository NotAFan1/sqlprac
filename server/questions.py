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
    },
    {
    "id": "q16",
    "difficulty": "hard",
    "topic": "aggregation",
    "prompt": "Return the columns `country` and `user_count`. Each row should represent a country. Only include countries with more than 5 users.",
    "expected_sql": """
    SELECT country, COUNT(user_id) AS user_count
    FROM users
    GROUP BY country
    HAVING COUNT(user_id) > 5;
    """.strip(),
    "required_patterns":[
    {"label":"group by country","pattern":r"group\s+by\s+.*country"},
    {"label":"having","pattern":r"having\s+"}
    ],
    "concepts":["GROUP BY","HAVING","COUNT"],
    "explanation":"Counts users per country and filters countries with more than five users."
    },

    {
    "id": "q17",
    "difficulty": "hard",
    "topic": "join_aggregation",
    "prompt": "Return the columns `plan_name` and `active_subscriptions`. Only include subscriptions where `status = 'active'`.",
    "expected_sql": """
    SELECT sp.plan_name, COUNT(s.subscription_id) AS active_subscriptions
    FROM subscription_plans sp
    JOIN subscriptions s
    ON sp.plan_id = s.plan_id
    WHERE s.status = 'active'
    GROUP BY sp.plan_name;
    """.strip(),
    "required_patterns":[
    {"label":"join subscriptions","pattern":r"join\s+subscriptions"},
    {"label":"status active","pattern":r"status\s*=\s*['\"]active['\"]"}
    ],
    "concepts":["JOIN","GROUP BY","COUNT"],
    "explanation":"Counts active subscriptions per plan."
    },

    {
    "id": "q18",
    "difficulty": "hard",
    "topic": "multi_join",
    "prompt": "Return the columns `title` and `genre_name` for each show and its genre.",
    "expected_sql": """
    SELECT s.title, g.genre_name
    FROM shows s
    JOIN show_genres sg
    ON s.show_id = sg.show_id
    JOIN genres g
    ON sg.genre_id = g.genre_id;
    """.strip(),
    "required_patterns":[
    {"label":"join show_genres","pattern":r"join\s+show_genres"},
    {"label":"join genres","pattern":r"join\s+genres"}
    ],
    "concepts":["JOIN"],
    "explanation":"Links shows to their genres through the bridge table."
    },

    {
    "id": "q19",
    "difficulty": "hard",
    "topic": "aggregation",
    "prompt": "Return the columns `show_id` and `rating_count`. Only include shows with more than 10 ratings.",
    "expected_sql": """
    SELECT show_id, COUNT(rating_id) AS rating_count
    FROM ratings
    GROUP BY show_id
    HAVING COUNT(rating_id) > 10;
    """.strip(),
    "required_patterns":[
    {"label":"group by show","pattern":r"group\s+by\s+.*show_id"},
    {"label":"having","pattern":r"having\s+"}
    ],
    "concepts":["GROUP BY","HAVING"],
    "explanation":"Finds shows that have received many ratings."
    },

    {
    "id": "q20",
    "difficulty": "hard",
    "topic": "avg_rating",
    "prompt": "Return the columns `title` and `avg_rating`. Round the average rating to 2 decimals.",
    "expected_sql": """
    SELECT s.title, ROUND(AVG(r.rating),2) AS avg_rating
    FROM shows s
    JOIN ratings r
    ON s.show_id = r.show_id
    GROUP BY s.title;
    """.strip(),
    "required_patterns":[
    {"label":"avg rating","pattern":r"avg\s*\("},
    {"label":"round","pattern":r"round\s*\("}
    ],
    "concepts":["AVG","ROUND","GROUP BY"],
    "explanation":"Calculates the average rating for each show."
    },

    {
    "id": "q21",
    "difficulty": "hard",
    "topic": "episodes",
    "prompt": "Return the columns `title` and `episode_count` representing how many episodes each show has.",
    "expected_sql": """
    SELECT s.title, COUNT(e.episode_id) AS episode_count
    FROM shows s
    JOIN seasons se
    ON s.show_id = se.show_id
    JOIN episodes e
    ON se.season_id = e.season_id
    GROUP BY s.title;
    """.strip(),
    "required_patterns":[
    {"label":"join seasons","pattern":r"join\s+seasons"},
    {"label":"join episodes","pattern":r"join\s+episodes"}
    ],
    "concepts":["JOIN","GROUP BY","COUNT"],
    "explanation":"Counts total episodes per show."
    },

    {
    "id": "q22",
    "difficulty": "hard",
    "topic": "watch_history",
    "prompt": "Return the columns `profile_id` and `total_minutes_watched`.",
    "expected_sql": """
    SELECT profile_id, SUM(minutes_watched) AS total_minutes_watched
    FROM watch_history
    GROUP BY profile_id;
    """.strip(),
    "required_patterns":[
    {"label":"sum minutes","pattern":r"sum\s*\("}
    ],
    "concepts":["SUM","GROUP BY"],
    "explanation":"Calculates total watch time per profile."
    },

    {
    "id": "q23",
    "difficulty": "hard",
    "topic": "completed_watch",
    "prompt": "Return the columns `profile_id` and `completed_count` representing how many episodes each profile completed.",
    "expected_sql": """
    SELECT profile_id, COUNT(watch_id) AS completed_count
    FROM watch_history
    WHERE completed = 1
    GROUP BY profile_id;
    """.strip(),
    "required_patterns":[
    {"label":"completed filter","pattern":r"completed\s*=\s*1"},
    {"label":"count","pattern":r"count\s*\("}
    ],
    "concepts":["WHERE","GROUP BY","COUNT"],
    "explanation":"Counts completed episodes per profile."
    },

    {
    "id": "q24",
    "difficulty": "hard",
    "topic": "actors",
    "prompt": "Return the columns `title` and `actor_count` representing how many actors appear in each show.",
    "expected_sql": """
    SELECT s.title, COUNT(sc.actor_id) AS actor_count
    FROM shows s
    JOIN show_cast sc
    ON s.show_id = sc.show_id
    GROUP BY s.title;
    """.strip(),
    "required_patterns":[
    {"label":"join show_cast","pattern":r"join\s+show_cast"},
    {"label":"count","pattern":r"count\s*\("}
    ],
    "concepts":["JOIN","GROUP BY","COUNT"],
    "explanation":"Counts actors per show."
    },

    {
    "id": "q25",
    "difficulty": "hard",
    "topic": "subquery",
    "prompt": "Return the columns `title` and `release_year` for shows released after the average release year.",
    "expected_sql": """
    SELECT title, release_year
    FROM shows
    WHERE release_year >
    (
    SELECT AVG(release_year)
    FROM shows
    );
    """.strip(),
    "required_patterns":[
    {"label":"avg release year","pattern":r"avg\s*\(\s*release_year"},
    {"label":"subquery","pattern":r"select\s+avg"}
    ],
    "concepts":["SUBQUERY","AVG"],
    "explanation":"Finds shows newer than the average release year."
    },

    {
    "id": "q26",
    "difficulty": "hard",
    "topic": "left_join",
    "prompt": "Return the columns `title` and `rating_count`. Include shows even if they have no ratings.",
    "expected_sql": """
    SELECT s.title, COUNT(r.rating_id) AS rating_count
    FROM shows s
    LEFT JOIN ratings r
    ON s.show_id = r.show_id
    GROUP BY s.title;
    """.strip(),
    "required_patterns":[
    {"label":"left join ratings","pattern":r"left\s+join\s+ratings"},
    {"label":"count","pattern":r"count\s*\("}
    ],
    "concepts":["LEFT JOIN","GROUP BY"],
    "explanation":"Shows ratings per show including shows with zero ratings."
    },

    {
    "id": "q27",
    "difficulty": "hard",
    "topic": "payments",
    "prompt": "Return the columns `payment_method` and `total_amount` representing the total amount paid using each method.",
    "expected_sql": """
    SELECT payment_method, SUM(amount) AS total_amount
    FROM payments
    WHERE payment_status = 'paid'
    GROUP BY payment_method;
    """.strip(),
    "required_patterns":[
    {"label":"sum","pattern":r"sum\s*\("},
    {"label":"paid filter","pattern":r"payment_status\s*=\s*['\"]paid['\"]"}
    ],
    "concepts":["SUM","GROUP BY","WHERE"],
    "explanation":"Calculates revenue per payment method."
    },

    {
    "id": "q28",
    "difficulty": "hard",
    "topic": "country_content",
    "prompt": "Return the columns `country` and `show_count` representing how many shows were produced in each country.",
    "expected_sql": """
    SELECT country, COUNT(show_id) AS show_count
    FROM shows
    GROUP BY country;
    """.strip(),
    "required_patterns":[
    {"label":"group by country","pattern":r"group\s+by\s+.*country"}
    ],
    "concepts":["GROUP BY","COUNT"],
    "explanation":"Counts shows by production country."
    },

    {
    "id": "q29",
    "difficulty": "hard",
    "topic": "profile_counts",
    "prompt": "Return the columns `user_id` and `profile_count` representing how many profiles each user has.",
    "expected_sql": """
    SELECT user_id, COUNT(profile_id) AS profile_count
    FROM profiles
    GROUP BY user_id;
    """.strip(),
    "required_patterns":[
    {"label":"group by user","pattern":r"group\s+by\s+.*user_id"}
    ],
    "concepts":["GROUP BY","COUNT"],
    "explanation":"Counts profiles per user account."
    },

    {
    "id": "q30",
    "difficulty": "hard",
    "topic": "most_watched_show",
    "prompt": "Return the columns `show_id` and `total_minutes` representing total minutes watched per show.",
    "expected_sql": """
    SELECT se.show_id, SUM(w.minutes_watched) AS total_minutes
    FROM watch_history w
    JOIN episodes e
    ON w.episode_id = e.episode_id
    JOIN seasons se
    ON e.season_id = se.season_id
    GROUP BY se.show_id;
    """.strip(),
    "required_patterns":[
    {"label":"sum minutes","pattern":r"sum\s*\("},
    {"label":"join episodes","pattern":r"join\s+episodes"}
    ],
    "concepts":["JOIN","SUM","GROUP BY"],
    "explanation":"Calculates total watch time per show."
    }


]
def get_question_by_id(question_id: str):
    return next((q for q in QUESTIONS if q["id"] == question_id), None)

def get_random_question(difficulty: str | None = None):
    pool = QUESTIONS
    if difficulty:
        pool = [q for q in QUESTIONS if q["difficulty"] == difficulty.lower()]
    return random.choice(pool) if pool else None