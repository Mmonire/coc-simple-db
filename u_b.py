import random
import pandas as pd

# تنظیمات اولیه
NUM_USERS = 15000
NUM_BUILDINGS = 137
MIN_BUILDINGS_PER_USER = 2
MAX_BUILDINGS_PER_USER = 25
MAP_WIDTH = 50  # عرض محدوده بازی
MAP_HEIGHT = 50  # ارتفاع محدوده بازی

# تولید داده‌ها
user_buildings = []
user_building_id = 1

for user_id in range(1, NUM_USERS + 1):
    # تعداد ساختمان‌های این کاربر (به صورت تصادفی)
    num_buildings = random.randint(MIN_BUILDINGS_PER_USER, MAX_BUILDINGS_PER_USER)

    # انتخاب تصادفی ساختمان‌ها برای این کاربر (با امکان تکرار)
    buildings = [random.randint(1, NUM_BUILDINGS) for _ in range(num_buildings)]

    for building_id in buildings:
        # موقعیت‌های تصادفی با فاصله مناسب
        x = random.randint(0, MAP_WIDTH - 1)
        y = random.randint(0, MAP_HEIGHT - 1)

        user_buildings.append({
            "UserBuildingID": user_building_id,
            "UserID": user_id,
            "BuildingID": building_id,
            "XCoordinate": x,
            "YCoordinate": y
        })
        user_building_id += 1

# تبدیل به DataFrame برای مشاهده بهتر
df = pd.DataFrame(user_buildings)

# تولید دستورات SQL
sql_inserts = []
for row in user_buildings:
    sql = f"INSERT INTO UserBuildings (UserBuildingID, UserID, BuildingID, XCoordinate, YCoordinate) VALUES ({row['UserBuildingID']}, {row['UserID']}, {row['BuildingID']}, {row['XCoordinate']}, {row['YCoordinate']});"
    sql_inserts.append(sql)

# ذخیره در فایل
with open('user_buildings_inserts_with_duplicates.sql', 'w') as f:
    f.write('\n'.join(sql_inserts))

# نمایش اطلاعات آماری
print(f"تعداد کل رکوردهای تولید شده: {len(user_buildings)}")
print(f"تعداد کاربران: {NUM_USERS}")
print(f"تعداد ساختمان‌ها: {NUM_BUILDINGS}")
print(f"میانگین ساختمان‌ها به ازای هر کاربر: {len(user_buildings) / NUM_USERS:.2f}")

# نمونه خروجی
print("\nنمونه رکوردهای تولید شده:")
print(df.head().to_string(index=False))