#!/usr/bin/env python3
"""
Generate hourly transaction data for January 2024 and write to data/data.csv

Columns: date,day,hour,number_of_transactions,total_amount

This script is deterministic (seeded) so repeated runs produce the same output.
"""
import csv
import datetime
import random
import os


OUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "data.csv")


def hourly_base_transactions(hour: int) -> float:
    # Return a random base value between 1_000 and 1_000_000 (integer)
    # This ignores the old hour-based shape and is purely random each call.
    return float(random.randint(1000, 10000))

def hourly_avg_value(hour: int) -> float:
    # Average transaction value varies a bit by hour
    # Return a random base value between 1_000 and 1_000_000 (integer)
    # This ignores the old hour-based shape and is purely random each call.
    return float(random.randint(1000, 1000000))


def generate_month(year: int, month: int):
    start = datetime.date(year, month, 1)
    # find last day
    if month == 12:
        end = datetime.date(year + 1, 1, 1)
    else:
        end = datetime.date(year, month + 1, 1)

    random.seed(0)

    rows = []
    cur = start
    while cur < end:
        day_name = cur.strftime("%A")
        weekday = cur.weekday()  # 0=Mon .. 6=Sun
        # weekend multiplier (slightly different patterns)
        weekend = 1.0 if weekday < 5 else 1.1
        for hour in range(24):
            base = hourly_base_transactions(hour)
            # small random fluctuation
            tx = int(max(0, round(random.gauss(base * weekend, base * 0.25))))
            # average transaction value with small noise
            avg = hourly_avg_value(hour) * (1 + random.uniform(-0.1, 0.1))
            total = round(tx * avg, 2)
            rows.append({
                "date": cur.isoformat(),
                "day": day_name,
                "hour": hour,
                "number_of_transactions": tx,
                "total_amount": f"{total:.2f}",
            })
        cur += datetime.timedelta(days=1)

    # write CSV (overwrite)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "day", "hour", "number_of_transactions", "total_amount"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


if __name__ == "__main__":
    # Generate January 2024
    generate_month(2024, 1)
    print(f"Wrote hourly data for 2024-01 to {OUT_PATH}")
