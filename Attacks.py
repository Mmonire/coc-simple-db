import random
import pandas as pd

# تنظیمات اولیه
NUM_ATTACKS = 250000
NUM_USERS = 15000
MAX_ATTACK_DURATION = 180  # 3 دقیقه حداکثر زمان حمله

# قوانین بازی برای ستاره‌ها و درصد تخریب
STAR_RULES = {
    0: {"min_destruction": 0, "max_destruction": 49, "prob": 0.2},
    1: {"min_destruction": 50, "max_destruction": 74, "prob": 0.3},
    2: {"min_destruction": 75, "max_destruction": 99, "prob": 0.4},
    3: {"min_destruction": 100, "max_destruction": 100, "prob": 0.1}
}

# تولید داده‌های حمله با قوانین واقعی بازی
attacks = []
for attack_id in range(1, NUM_ATTACKS + 1):
    # انتخاب تصادفی کاربران
    offender = random.randint(1, NUM_USERS)
    defender = random.randint(1, NUM_USERS)
    while defender == offender:
        defender = random.randint(1, NUM_USERS)

    # تعیین تعداد ستاره‌ها بر اساس احتمالات تعریف شده
    stars = random.choices(
        list(STAR_RULES.keys()),
        weights=[rule["prob"] for rule in STAR_RULES.values()]
    )[0]

    # تعیین درصد تخریب بر اساس تعداد ستاره‌ها
    rule = STAR_RULES[stars]
    castle_destroyed = random.uniform(rule["min_destruction"], rule["max_destruction"])
    castle_destroyed = round(castle_destroyed, 2)

    # زمان حمله (هر ستاره بیشتر = زمان بیشتر)
    base_duration = random.randint(30, MAX_ATTACK_DURATION)
    attack_duration = min(MAX_ATTACK_DURATION, base_duration + stars * 20)

    attacks.append({
        "AttackID": attack_id,
        "UserID_Offender": offender,
        "UserID_Defender": defender,
        "Castle_Destroyed": castle_destroyed,
        "Stars_achieved": stars,
        "Attack_Duration": attack_duration
    })

# تولید دستورات SQL
sql_inserts = []
for attack in attacks:
    sql = f"""INSERT INTO Attacks (AttackID, UserID_Offender, UserID_Defender, Castle_Destroyed, Stars_achieved, Attack_Time) VALUES ({attack['AttackID']}, {attack['UserID_Offender']}, {attack['UserID_Defender']}, {attack['Castle_Destroyed']}, {attack['Stars_achieved']}, {attack['Attack_Duration']});"""
    sql_inserts.append(sql)

# ذخیره در فایل
with open('SQLQueryAttacks.sql', 'w') as f:
    f.write('\n'.join(sql_inserts))

# تحلیل داده‌ها
df = pd.DataFrame(attacks)

# محاسبه آمار پیشرفته
stats = {
    "تعداد کل رکوردها": len(attacks),
    "توزیع ستاره‌ها": dict(
        df['Stars_achieved'].value_counts(normalize=True).sort_index().apply(lambda x: f"{x * 100:.1f}%")),
    "میانگین درصد تخریب به ازای هر ستاره": {
        stars: f"{df[df['Stars_achieved'] == stars]['Castle_Destroyed'].mean():.1f}%"
        for stars in sorted(df['Stars_achieved'].unique())
    },
    "میانگین زمان حمله به ازای هر ستاره": {
        stars: f"{df[df['Stars_achieved'] == stars]['Attack_Duration'].mean():.1f} ثانیه"
        for stars in sorted(df['Stars_achieved'].unique())
    },
    "رابطه درصد تخریب و ستاره‌ها": "\n" + pd.crosstab(
        pd.cut(df['Castle_Destroyed'], bins=[0, 50, 75, 100, 101], labels=['0-49%', '50-74%', '75-99%', '100%']),
        df['Stars_achieved']
    ).to_string()
}

print("آمار تولید داده‌ها با قوانین واقعی بازی:")
for key, value in stats.items():
    if isinstance(value, dict):
        print(f"\n{key}:")
        for k, v in value.items():
            print(f"  {k} ستاره: {v}")
    else:
        print(f"\n{key}: {value}")

print("\nنمونه رکوردهای تولید شده:")
for i in range(3):
    print(sql_inserts[i])