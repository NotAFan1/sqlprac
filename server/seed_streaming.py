import os
import random
import sqlite3
from faker import Faker

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

DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS show_cast;
DROP TABLE IF EXISTS actors;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS watch_history;
DROP TABLE IF EXISTS episodes;
DROP TABLE IF EXISTS seasons;
DROP TABLE IF EXISTS show_genres;
DROP TABLE IF EXISTS shows;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS profiles;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS subscription_plans;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    country TEXT NOT NULL,
    signup_date TEXT NOT NULL,
    birth_year INTEGER NOT NULL
);

CREATE TABLE subscription_plans (
    plan_id INTEGER PRIMARY KEY,
    plan_name TEXT NOT NULL,
    monthly_price REAL NOT NULL,
    max_devices INTEGER NOT NULL,
    video_quality TEXT NOT NULL
);

CREATE TABLE subscriptions (
    subscription_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    status TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (plan_id) REFERENCES subscription_plans(plan_id)
);

CREATE TABLE profiles (
    profile_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    profile_name TEXT NOT NULL,
    is_kids_profile INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE genres (
    genre_id INTEGER PRIMARY KEY,
    genre_name TEXT NOT NULL UNIQUE
);

CREATE TABLE shows (
    show_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    release_year INTEGER NOT NULL,
    country TEXT NOT NULL,
    content_type TEXT NOT NULL,
    age_rating TEXT NOT NULL
);

CREATE TABLE show_genres (
    show_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (show_id, genre_id),
    FOREIGN KEY (show_id) REFERENCES shows(show_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

CREATE TABLE seasons (
    season_id INTEGER PRIMARY KEY,
    show_id INTEGER NOT NULL,
    season_number INTEGER NOT NULL,
    release_year INTEGER NOT NULL,
    FOREIGN KEY (show_id) REFERENCES shows(show_id)
);

CREATE TABLE episodes (
    episode_id INTEGER PRIMARY KEY,
    season_id INTEGER NOT NULL,
    episode_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    FOREIGN KEY (season_id) REFERENCES seasons(season_id)
);

CREATE TABLE watch_history (
    watch_id INTEGER PRIMARY KEY,
    profile_id INTEGER NOT NULL,
    episode_id INTEGER NOT NULL,
    watched_at TEXT NOT NULL,
    minutes_watched INTEGER NOT NULL,
    completed INTEGER NOT NULL,
    FOREIGN KEY (profile_id) REFERENCES profiles(profile_id),
    FOREIGN KEY (episode_id) REFERENCES episodes(episode_id)
);

CREATE TABLE ratings (
    rating_id INTEGER PRIMARY KEY,
    profile_id INTEGER NOT NULL,
    show_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    rating_date TEXT NOT NULL,
    FOREIGN KEY (profile_id) REFERENCES profiles(profile_id),
    FOREIGN KEY (show_id) REFERENCES shows(show_id)
);

CREATE TABLE actors (
    actor_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE show_cast (
    show_id INTEGER NOT NULL,
    actor_id INTEGER NOT NULL,
    role_name TEXT NOT NULL,
    PRIMARY KEY (show_id, actor_id),
    FOREIGN KEY (show_id) REFERENCES shows(show_id),
    FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    subscription_id INTEGER NOT NULL,
    payment_date TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_method TEXT NOT NULL,
    payment_status TEXT NOT NULL,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id)
);
""")

countries = [
    "USA", "Canada", "UK", "India", "Australia",
    "Germany", "France", "Japan", "Brazil", "South Korea"
]

age_ratings = ["G", "PG", "PG-13", "TV-14", "TV-MA", "R"]
content_types = ["Movie", "Series", "Documentary", "Mini Series"]
payment_methods = ["credit_card", "debit_card", "paypal", "apple_pay"]
payment_statuses = ["paid", "failed", "refunded"]
subscription_statuses = ["active", "cancelled", "expired"]

genre_names = [
    "Drama", "Comedy", "Action", "Thriller", "Sci-Fi",
    "Romance", "Documentary", "Fantasy", "Crime", "Animation"
]

plan_data = [
    (1, "Basic", 7.99, 1, "HD"),
    (2, "Standard", 12.99, 2, "Full HD"),
    (3, "Premium", 18.99, 4, "4K"),
]

show_words_1 = [
    "Shadow", "Golden", "Silent", "Broken", "Crystal", "Midnight",
    "Neon", "Fallen", "Hidden", "Electric", "Dark", "Silver"
]
show_words_2 = [
    "City", "Point", "Hearts", "Empire", "Signal", "Tides",
    "Horizon", "Archive", "Echo", "Road", "Line", "Storm"
]

role_names = [
    "Lead", "Supporting", "Detective", "Host", "Narrator",
    "Captain", "Professor", "Agent", "Parent", "Friend"
]

# Users
users = []
for user_id in range(1, 101):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}{user_id}@example.com"
    country = random.choice(countries)
    signup_date = str(fake.date_between(start_date="-3y", end_date="-30d"))
    birth_year = random.randint(1965, 2012)
    users.append((user_id, first_name, last_name, email, country, signup_date, birth_year))

cur.executemany("""
INSERT INTO users (user_id, first_name, last_name, email, country, signup_date, birth_year)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", users)

# Subscription plans
cur.executemany("""
INSERT INTO subscription_plans (plan_id, plan_name, monthly_price, max_devices, video_quality)
VALUES (?, ?, ?, ?, ?)
""", plan_data)

# Subscriptions
subscriptions = []
subscription_id = 1
for user in users:
    user_id = user[0]
    plan_id = random.choice([1, 2, 2, 3])
    start_date = fake.date_between(start_date="-2y", end_date="-60d")
    status = random.choices(subscription_statuses, weights=[0.7, 0.15, 0.15], k=1)[0]

    if status == "active":
        end_date = None
    else:
        end_date = str(fake.date_between(start_date=start_date, end_date="today"))

    subscriptions.append((
        subscription_id,
        user_id,
        plan_id,
        str(start_date),
        end_date,
        status
    ))
    subscription_id += 1

cur.executemany("""
INSERT INTO subscriptions (subscription_id, user_id, plan_id, start_date, end_date, status)
VALUES (?, ?, ?, ?, ?, ?)
""", subscriptions)

# Profiles
profiles = []
profile_id = 1
for user in users:
    user_id = user[0]
    num_profiles = random.choice([1, 2, 2, 3, 4])
    for i in range(num_profiles):
        if i == 0:
            profile_name = user[1]
        else:
            profile_name = fake.first_name()
        is_kids_profile = 1 if random.random() < 0.15 else 0
        profiles.append((profile_id, user_id, profile_name, is_kids_profile))
        profile_id += 1

cur.executemany("""
INSERT INTO profiles (profile_id, user_id, profile_name, is_kids_profile)
VALUES (?, ?, ?, ?)
""", profiles)

# Genres
genres = [(i + 1, genre) for i, genre in enumerate(genre_names)]
cur.executemany("""
INSERT INTO genres (genre_id, genre_name)
VALUES (?, ?)
""", genres)

# Shows
shows = []
for show_id in range(1, 51):
    title = f"{random.choice(show_words_1)} {random.choice(show_words_2)}"
    release_year = random.randint(2010, 2025)
    country = random.choice(countries)
    content_type = random.choices(content_types, weights=[0.45, 0.35, 0.1, 0.1], k=1)[0]
    age_rating = random.choice(age_ratings)
    shows.append((show_id, title, release_year, country, content_type, age_rating))

cur.executemany("""
INSERT INTO shows (show_id, title, release_year, country, content_type, age_rating)
VALUES (?, ?, ?, ?, ?, ?)
""", shows)

# Show genres
show_genres = []
for show in shows:
    show_id = show[0]
    chosen_genres = random.sample(range(1, len(genres) + 1), k=random.choice([1, 2, 2, 3]))
    for genre_id in chosen_genres:
        show_genres.append((show_id, genre_id))

cur.executemany("""
INSERT INTO show_genres (show_id, genre_id)
VALUES (?, ?)
""", show_genres)

# Seasons
seasons = []
season_id = 1
for show in shows:
    show_id = show[0]
    content_type = show[4]
    release_year = show[2]

    if content_type in ["Movie", "Documentary"]:
        num_seasons = 1
    elif content_type == "Mini Series":
        num_seasons = random.choice([1, 1, 2])
    else:
        num_seasons = random.randint(2, 5)

    for season_number in range(1, num_seasons + 1):
        seasons.append((
            season_id,
            show_id,
            season_number,
            min(release_year + season_number - 1, 2025)
        ))
        season_id += 1

cur.executemany("""
INSERT INTO seasons (season_id, show_id, season_number, release_year)
VALUES (?, ?, ?, ?)
""", seasons)

# Episodes
episodes = []
episode_id = 1
for season in seasons:
    season_id_val = season[0]
    show_id = season[1]
    show = next(s for s in shows if s[0] == show_id)
    content_type = show[4]

    if content_type == "Movie":
        num_episodes = 1
    elif content_type == "Documentary":
        num_episodes = random.randint(1, 3)
    elif content_type == "Mini Series":
        num_episodes = random.randint(4, 8)
    else:
        num_episodes = random.randint(6, 12)

    for ep_num in range(1, num_episodes + 1):
        ep_title = f"Episode {ep_num}" if content_type != "Movie" else show[1]
        duration = random.randint(22, 58) if content_type == "Series" else random.randint(45, 120)
        episodes.append((
            episode_id,
            season_id_val,
            ep_num,
            ep_title,
            duration
        ))
        episode_id += 1

cur.executemany("""
INSERT INTO episodes (episode_id, season_id, episode_number, title, duration_minutes)
VALUES (?, ?, ?, ?, ?)
""", episodes)

# Actors
actors = []
for actor_id in range(1, 81):
    actors.append((
        actor_id,
        fake.first_name(),
        fake.last_name(),
        random.randint(1955, 2005),
        random.choice(countries)
    ))

cur.executemany("""
INSERT INTO actors (actor_id, first_name, last_name, birth_year, country)
VALUES (?, ?, ?, ?, ?)
""", actors)

# Show cast
show_cast_rows = []
for show in shows:
    show_id = show[0]
    chosen_actors = random.sample(range(1, 81), k=random.randint(3, 6))
    for actor_id in chosen_actors:
        show_cast_rows.append((
            show_id,
            actor_id,
            random.choice(role_names)
        ))

cur.executemany("""
INSERT INTO show_cast (show_id, actor_id, role_name)
VALUES (?, ?, ?)
""", show_cast_rows)

# Watch history
watch_history = []
watch_id = 1
all_episode_ids = [ep[0] for ep in episodes]

for profile in profiles:
    profile_id_val = profile[0]
    num_watches = random.randint(8, 35)
    chosen_episodes = random.sample(all_episode_ids, k=min(num_watches, len(all_episode_ids)))

    for episode_id_val in chosen_episodes:
        ep = next(e for e in episodes if e[0] == episode_id_val)
        duration = ep[4]
        completed = 1 if random.random() < 0.65 else 0
        minutes_watched = duration if completed else random.randint(5, max(5, duration - 1))
        watched_at = str(fake.date_between(start_date="-1y", end_date="today"))

        watch_history.append((
            watch_id,
            profile_id_val,
            episode_id_val,
            watched_at,
            minutes_watched,
            completed
        ))
        watch_id += 1

cur.executemany("""
INSERT INTO watch_history (watch_id, profile_id, episode_id, watched_at, minutes_watched, completed)
VALUES (?, ?, ?, ?, ?, ?)
""", watch_history)

# Ratings
ratings = []
rating_id = 1
profile_ids = [p[0] for p in profiles]

for show in shows:
    show_id = show[0]
    num_ratings = random.randint(5, 20)
    chosen_profiles = random.sample(profile_ids, k=min(num_ratings, len(profile_ids)))
    for profile_id_val in chosen_profiles:
        ratings.append((
            rating_id,
            profile_id_val,
            show_id,
            random.randint(2, 5),
            str(fake.date_between(start_date="-1y", end_date="today"))
        ))
        rating_id += 1

cur.executemany("""
INSERT INTO ratings (rating_id, profile_id, show_id, rating, rating_date)
VALUES (?, ?, ?, ?, ?)
""", ratings)

# Payments
payments = []
payment_id = 1

for sub in subscriptions:
    subscription_id_val = sub[0]
    plan_id = sub[2]
    start_date = sub[3]
    status = sub[5]
    plan = next(p for p in plan_data if p[0] == plan_id)
    amount = plan[2]

    num_payments = random.randint(1, 6) if status == "active" else random.randint(1, 4)

    for _ in range(num_payments):
        pay_status = random.choices(payment_statuses, weights=[0.8, 0.1, 0.1], k=1)[0]
        pay_amount = amount if pay_status == "paid" else (0.0 if pay_status == "failed" else amount)
        payments.append((
            payment_id,
            subscription_id_val,
            str(fake.date_between(start_date="-2y", end_date="today")),
            round(pay_amount, 2),
            random.choice(payment_methods),
            pay_status
        ))
        payment_id += 1

cur.executemany("""
INSERT INTO payments (payment_id, subscription_id, payment_date, amount, payment_method, payment_status)
VALUES (?, ?, ?, ?, ?, ?)
""", payments)

conn.commit()

tables = [
    "users", "subscription_plans", "subscriptions", "profiles", "genres",
    "shows", "show_genres", "seasons", "episodes", "watch_history",
    "ratings", "actors", "show_cast", "payments"
]

print("Created db.sqlite")
for table in tables:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"{table}: {cur.fetchone()[0]}")

conn.close()
