troops_data = [
    # نیروهای معمولی (Elixir)
    {"Name": "Barbarian",
     "HitPoints": 300,
     "Damage": 50,
     "DamageType": "GroundToGround", "Capacity": 1, "Resource": "Elixir"},

    {"Name": "Archer",
     "HitPoints": 125,
     "Damage": 40,
     "DamageType": "GroundToBoth", "Capacity": 1, "Resource": "Elixir"},

    {"Name": "Giant",
     "HitPoints": 2000,
     "Damage": 80,
     "DamageType": "GroundToGround", "Capacity": 5, "Resource": "Elixir"},

    # نیروهای اکسیر تیره (Dark Elixir)
    {"Name": "Minion",
     "HitPoints": 180,
     "Damage": 60,
     "DamageType": "AirToBoth", "Capacity": 2, "Resource": "DarkElixir"},

    {"Name": "Hog Rider",
     "HitPoints": 800,
     "Damage": 200,
     "DamageType": "GroundToGround", "Capacity": 5, "Resource": "DarkElixir"},

    {"Name": "Valkyrie",
     "HitPoints": 1200,
     "Damage": 180,
     "DamageType": "GroundToGround", "Capacity": 8, "Resource": "DarkElixir"},

    # نیروهای سوپر (Super Troops)
    {"Name": "Super Barbarian",
     "HitPoints": 1500,
     "Damage": 200,
     "DamageType": "GroundToGround", "Capacity": 1, "Resource": "DarkElixir"},

    {"Name": "Super Archer",
     "HitPoints": 300,
     "Damage": 80,
     "DamageType": "GroundToBoth", "Capacity": 1, "Resource": "DarkElixir"},

    # نیروهای جدید اضافه شده
    {"Name": "Wizard",
     "HitPoints": 130,
     "Damage": 150,
     "DamageType": "GroundToBoth", "Capacity": 4, "Resource": "Elixir"},

    {"Name": "Golem",
     "HitPoints": 4500,
     "Damage": 120,
     "DamageType": "GroundToGround", "Capacity": 30, "Resource": "DarkElixir"},

    {"Name": "Witch",
     "HitPoints": 400,
     "Damage": 100,
     "DamageType": "GroundToBoth", "Capacity": 12, "Resource": "DarkElixir"},
]


def generate_all_troops_data():
    all_troops = []
    troop_id = 1

    for troop in troops_data:
        all_troops.append({
            "TroopID": troop_id,
            "Name": troop["Name"],
            "HitPoint": troop["HitPoints"],
            "Damage": troop["Damage"],
            "DamageType": troop["DamageType"],
            "Capacity": troop["Capacity"],
            "Resource": troop["Resource"]
        })
        troop_id += 1

    return all_troops


# تولید تمام حالت‌های ممکن
all_troops = generate_all_troops_data()

# تولید دستورات SQL
sql_inserts = []
for troop in all_troops:
    sql = f"INSERT INTO Troops (TroopID, Name, HitPoint, Damage, DamageType, Capacity, Resource) VALUES ({troop['TroopID']}, '{troop['Name']}', {troop['HitPoint']}, {troop['Damage']}, '{troop['DamageType']}', {troop['Capacity']}, '{troop['Resource']}');"
    sql_inserts.append(sql)

for sql in sql_inserts:
    print(sql)