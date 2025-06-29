import random
from faker import Faker

# برای تولید نام‌های رندوم (اختیاری)
fake = Faker()

# لیست ساختمان‌ها با اطلاعات پایه
buildings_data = [
    # منابع (Resource)
    {"Name": "Gold Mine", "Type": "Resource", "MaxLevel": 15,
     "GoldCosts": [150, 1000, 4000, 16000, 50000, 100000, 250000, 500000, 1000000, 2000000, 3000000, 4000000, 5000000,
                   6000000, 7000000], "ElixirCosts": None, "DarkCosts": None, "Width": 3, "Height": 3},
    {"Name": "Elixir Collector", "Type": "Resource", "MaxLevel": 15, "GoldCosts": None,
     "ElixirCosts": [150, 1000, 4000, 16000, 50000, 100000, 250000, 500000, 1000000, 2000000, 3000000, 4000000, 5000000,
                     6000000, 7000000], "DarkCosts": None, "Width": 3, "Height": 3},
    {"Name": "Dark Elixir Drill", "Type": "Resource", "MaxLevel": 9, "GoldCosts": None, "ElixirCosts": None,
     "DarkCosts": [10000, 30000, 70000, 120000, 200000, 300000, 420000, 560000, 720000], "Width": 3, "Height": 3},

    # دفاعی (Defensive)
    {"Name": "Cannon", "Type": "Defensive", "MaxLevel": 20,
     "GoldCosts": [500, 1000, 2000, 4000, 16000, 32000, 64000, 128000, 256000, 512000, 1024000, 2048000, 4096000,
                   8192000, 12288000], "ElixirCosts": None, "DarkCosts": None, "Width": 3, "Height": 3},
    {"Name": "Archer Tower", "Type": "Defensive", "MaxLevel": 22,
     "GoldCosts": [1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 512000, 1024000, 2048000, 4096000,
                   8192000, 16384000], "ElixirCosts": None, "DarkCosts": None, "Width": 3, "Height": 3},
    {"Name": "Wizard Tower", "Type": "Defensive", "MaxLevel": 14, "GoldCosts": None,
     "ElixirCosts": [200000, 400000, 800000, 1200000, 1600000, 2000000, 2400000, 2800000, 3200000, 3600000, 4000000,
                     4500000, 5000000, 5500000], "DarkCosts": None, "Width": 3, "Height": 3},

    {"Name": "Wall", "Type": "Defensive", "MaxLevel": 16, "GoldCosts": [200, 1000, 5000, 10000, 30000, 50000, 100000, 250000, 500000, 1000000,
                  1500000, 2000000, 2500000, 3000000, 3500000, 4000000], "ElixirCosts": [None, None, None, None, None, None, None, None, None, 1000000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000], "DarkCosts": None, "Width": 1, "Height": 1},

    # نظامی (Army)
    {"Name": "Barracks", "Type": "Army", "MaxLevel": 16,
     "GoldCosts": [200, 400, 1000, 2000, 4000, 10000, 20000, 40000, 80000, 160000, 320000, 640000, 1280000, 2560000,
                   5120000, 7000000], "ElixirCosts": None, "DarkCosts": None, "Width": 3, "Height": 3},
    {"Name": "Dark Barracks", "Type": "Army", "MaxLevel": 10, "GoldCosts": None,
     "ElixirCosts": [150000, 300000, 600000, 800000, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000],
     "DarkCosts": None, "Width": 3, "Height": 3},
    {"Name": "Laboratory", "Type": "Army", "MaxLevel": 12, "GoldCosts": None,
     "ElixirCosts": [75000, 150000, 300000, 600000, 1200000, 2400000, 3600000, 4800000, 6000000, 7200000, 8400000,
                     9600000], "DarkCosts": None, "Width": 4, "Height": 4},
]


def generate_all_building_data():
    all_buildings = []
    building_id = 1

    for building in buildings_data:
        # تعیین حداکثر سطح بر اساس طول لیست هزینه‌ها
        max_level = 0
        if building["GoldCosts"]:
            max_level = max(max_level, len(building["GoldCosts"]))
        if building["ElixirCosts"]:
            max_level = max(max_level, len(building["ElixirCosts"]))
        if building["DarkCosts"]:
            max_level = max(max_level, len(building["DarkCosts"]))

        for level in range(1, max_level + 1):
            gold_cost = building["GoldCosts"][level - 1] if building["GoldCosts"] and level <= len(
                building["GoldCosts"]) else None
            elixir_cost = building["ElixirCosts"][level - 1] if building["ElixirCosts"] and level <= len(
                building["ElixirCosts"]) else None
            dark_cost = building["DarkCosts"][level - 1] if building["DarkCosts"] and level <= len(
                building["DarkCosts"]) else None

            all_buildings.append({
                "BuildingID": building_id,
                "Name": building["Name"],
                "UpgradeCost_Gold": gold_cost,
                "UpgradeCost_Elixir": elixir_cost,
                "UpgradeCost_DarkElixir": dark_cost,
                "Width": building["Width"],
                "Height": building["Height"],
                "Level": level,
                "Type": building["Type"]
            })
            building_id += 1

    return all_buildings


# تولید تمام حالت‌های ممکن
all_buildings = generate_all_building_data()

# تولید دستورات SQL
sql_inserts = []
for building in all_buildings:
    sql = f"INSERT INTO Buildings (BuildingID, Name, UpgradeCost_Gold, UpgradeCost_Elixir, UpgradeCost_DarkElixir, Width, Height, Level, Type) VALUES ({building['BuildingID']}, '{building['Name']}', {building['UpgradeCost_Gold'] or '0'}, {building['UpgradeCost_Elixir'] or '0'}, {building['UpgradeCost_DarkElixir'] or '0'}, {building['Width']}, {building['Height']}, {building['Level']}, '{building['Type']}');"
    sql_inserts.append(sql)

# نمایش دستورات SQL
for sql in sql_inserts:
    print(sql)