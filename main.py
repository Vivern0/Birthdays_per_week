from datetime import date, datetime, timedelta


def get_birthdays_per_week(users):
    if not users:
        return {}

    cur_date = date.today()
    cur_week_day = cur_date.weekday()
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    res = {}
    # Якщо ми починаємо з понеділка, зсуваємо перевірку на 2 дні назад
    i1 = 2 if cur_week_day == 0 else 0
    i2 = 5 if cur_week_day == 0 else 7
    # Обробляємо users в циклі for
    for user in users:
        # Дата народження користувача в цьому році
        next_birthday = user['birthday'].replace(year=cur_date.year)

        # Якщо день народження вже минув у цьому році, то переносимо його на наступний рік
        if next_birthday < cur_date:
            next_birthday = next_birthday.replace(year=cur_date.year+1)

        # Перевірка чи день народження входить в діапазон нашої тижня
        if (cur_date-timedelta(days=i1)) <= next_birthday <= (cur_date+timedelta(days=i2)):
            user_week_day = week_days[next_birthday.weekday()]
            res.setdefault(user_week_day, [])
            res[user_week_day].append(user['name'])

    # Якщо день народження випав на вихідний, додаємо його в наступний після них понеділок
    for d, n in res.items():
        if d in ("Saturday", "Sunday"):
            res.setdefault("Monday", [])
            for name in reversed(n):
                res['Monday'].insert(0, name)
            res[d] = []

    res = {k: v for k, v in res.items() if len(v)}
    return res


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
