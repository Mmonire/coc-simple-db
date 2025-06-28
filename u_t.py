import random

# تنظیمات اولیه
NUM_USERS = 15000
NUM_TROOPS = 11
MIN_TROOPS_PER_USER = 3
MAX_TROOPS_PER_USER = 11
MAX_LEVEL = 18  # حداکثر سطح در کلش اف کلنز

# تولید داده‌ها
user_troops = []

for user_id in range(1, NUM_USERS + 1):
    # تعداد نیروهای این کاربر (به صورت تصادفی)
    num_troops = random.randint(MIN_TROOPS_PER_USER, MAX_TROOPS_PER_USER)

    # انتخاب تصادفی نیروها برای این کاربر (بدون تکرار)
    available_troops = list(range(1, NUM_TROOPS + 1))
    selected_troops = random.sample(available_troops, min(num_troops, NUM_TROOPS))

    for troop_id in selected_troops:
        # تولید سطح تصادفی برای نیرو (سطوح بالاتر احتمال کمتری دارند)
        level = random.choices(
            range(1, MAX_LEVEL + 1),
            weights=[MAX_LEVEL - i for i in range(MAX_LEVEL)]  # سطوح پایین تر احتمال بیشتری دارند
        )[0]

        user_troops.append({
            "UserID": user_id,
            "TroopID": troop_id,
            "Level": level
        })

# تولید دستورات SQL
sql_inserts = []
for row in user_troops:
    sql = f"INSERT INTO UserTroops (UserID, TroopID, Level) VALUES ({row['UserID']}, {row['TroopID']}, {row['Level']});"
    sql_inserts.append(sql)

# ذخیره در فایل
with open('SQLQueryUser_t.sql', 'w') as f:
    f.write('\n'.join(sql_inserts))

# محاسبات آماری
total_records = len(user_troops)
avg_troops_per_user = total_records / NUM_USERS
avg_level = sum(row['Level'] for row in user_troops) / total_records

print(f"تعداد کل رکوردهای تولید شده: {total_records:,}")
print(f"تعداد کاربران: {NUM_USERS:,}")
print(f"تعداد نیروها: {NUM_TROOPS}")
print(f"میانگین نیروها به ازای هر کاربر: {avg_troops_per_user:.2f}")
print(f"میانگین سطح نیروها: {avg_level:.2f}")
print(f"فایل user_troops_inserts.sql با موفقیت ایجاد شد!")

# نمایش نمونه‌ای از خروجی
print("\nنمونه رکوردهای تولید شده:")
for i in range(5):
    print(sql_inserts[i])