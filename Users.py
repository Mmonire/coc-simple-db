import random
from faker import Faker
from datetime import datetime, timedelta

# ایجاد یک نمونه Faker برای نام‌های کاربری و تاریخ‌های واقعی‌تر
fake = Faker()

# محدوده زمانی برای تاریخ ثبت‌نام (10 سال گذشته تا الآن)
end_date = datetime.now()
start_date = end_date - timedelta(days=365 * 10)


def generate_random_user(user_id):
    # تولید تاریخ ثبت‌نام تصادفی
    random_days = random.randint(0, 365 * 10)
    signup_date = start_date + timedelta(days=random_days)

    return {
        "UserID": user_id,
        "Username": fake.user_name(),
        "Level": random.randint(1, 200),
        "Gold": random.randint(1000, 20000000),
        "Elixir": random.randint(1000, 20000000),
        "DarkElixir": random.randint(0, 500000),
        "Trophy": random.randint(0, 6000),
        "TownHallLevel": random.randint(1, 16),
        "SignupDate": signup_date.strftime('%Y-%m-%d %H:%M:%S')
    }


# تولید 15000 کاربر رندوم
users = [generate_random_user(i) for i in range(1, 15001)]

# تولید دستورات SQL
sql_inserts = []
for user in users:
    sql = (
        f"INSERT INTO Users (UserID, Username, Level, Gold, Elixir, DarkElixir, Trophy, TownHallLevel, SignupDate) "
        f"VALUES ({user['UserID']}, '{user['Username']}', {user['Level']}, {user['Gold']}, "
        f"{user['Elixir']}, {user['DarkElixir']}, {user['Trophy']}, {user['TownHallLevel']}, "
        f"'{user['SignupDate']}');"
    )
    sql_inserts.append(sql)

# نمایش نمونه‌ای از دستورات
for i in range(5):  # نمایش 5 دستور نمونه
    print(sql_inserts[i])

# ذخیره در فایل
with open('SQLQueryUsers.sql', 'w') as f:
    f.write('\n'.join(sql_inserts))

print("\nفایل random_users_with_signup.sql با موفقیت ایجاد شد!")