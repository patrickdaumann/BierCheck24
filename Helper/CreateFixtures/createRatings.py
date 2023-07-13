import json
import random
from datetime import datetime
from faker import Faker

def generate_entry(user_id, beer_id, pk):
    fake = Faker()
    entry = {
        "model": "Rating.Rating",
        "pk": pk,
        "fields": {
            "beer": beer_id,
            "user": user_id,
            "Color": fake.random_int(min=5, max=10),
            "Entry": fake.random_int(min=5, max=10),
            "body": fake.random_int(min=5, max=10),
            "finish": fake.random_int(min=5, max=10),
            "carbonation": fake.random_int(min=5, max=10),
            "acidity": fake.random_int(min=5, max=10),
            "bitterness": fake.random_int(min=5, max=10),
            "drinkability": fake.random_int(min=5, max=10),
            "price": random.randint(1, 3),
            "recommended": fake.boolean(chance_of_getting_true=80),
            "created_at": fake.date_time_this_year().isoformat()
        }
    }
    print(entry)
    return entry

def generate_entries():
    entries = []
    pk = 1
    for user_id in range(20, 1001):
        beer_ids = random.sample(range(1, 15), 5)
        for beer_id in beer_ids:
            entries.append(generate_entry(user_id, beer_id, pk))
            pk += 1
    return entries

def write_to_file(filename, entries):
    with open(filename, 'w') as f:
        json.dump(entries, f)

def main():
    filename = './Rating/fixtures/Ratings_gen.json'
    entries = generate_entries()
    write_to_file(filename, entries)

if __name__ == "__main__":
    main()
