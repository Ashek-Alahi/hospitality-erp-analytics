from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "02_Data" / "raw"
PROCESSED = ROOT / "02_Data" / "processed"
SEED = 4224
ROOMS_AVAILABLE = 120


def month_range(start_year=2024, start_month=1, months=24):
    y, m = start_year, start_month
    for _ in range(months):
        yield y, m, date(y, m, 1)
        m += 1
        if m == 13:
            y += 1
            m = 1


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def copy_to_raw_and_processed(filename: str, rows: list[dict[str, object]]) -> None:
    write_csv(RAW / filename.replace("_clean", ""), rows)
    write_csv(PROCESSED / filename, rows)


def generate_calendar() -> list[dict[str, object]]:
    rows = []
    current = date(2024, 1, 1)
    end = date(2025, 12, 31)
    while current <= end:
        rows.append({
            "date": current.isoformat(), "year": current.year, "month": current.month,
            "month_name": current.strftime("%B"), "quarter": f"Q{((current.month - 1) // 3) + 1}",
            "day_of_week": current.strftime("%A"), "is_weekend": str(current.weekday() >= 5),
        })
        current += timedelta(days=1)
    return rows


def generate_data() -> None:
    random.seed(SEED)
    customers = [
        {"customer_id": "C001", "customer_name": "Northstar Corporate Travel", "segment": "Corporate", "region": "Northeast"},
        {"customer_id": "C002", "customer_name": "Blue Harbor Events", "segment": "Group/Event", "region": "Southeast"},
        {"customer_id": "C003", "customer_name": "Leisure Direct Guests", "segment": "Leisure", "region": "National"},
        {"customer_id": "C004", "customer_name": "Online Travel Agencies", "segment": "OTA", "region": "Digital"},
        {"customer_id": "C005", "customer_name": "Government Conferences", "segment": "Government", "region": "Midwest"},
        {"customer_id": "C006", "customer_name": "Airline Crew Contracts", "segment": "Crew/Contract", "region": "West"},
    ]
    vendors = [
        {"vendor_id": "V001", "vendor_name": "FreshFields Produce", "category": "Food & Beverage", "on_time_delivery_pct": 82},
        {"vendor_id": "V002", "vendor_name": "LinenPro Services", "category": "Housekeeping", "on_time_delivery_pct": 88},
        {"vendor_id": "V003", "vendor_name": "GuestTech Supplies", "category": "Maintenance", "on_time_delivery_pct": 74},
        {"vendor_id": "V004", "vendor_name": "Beverage Central", "category": "Food & Beverage", "on_time_delivery_pct": 91},
        {"vendor_id": "V005", "vendor_name": "EcoAmenity Co", "category": "Guest Supplies", "on_time_delivery_pct": 69},
    ]
    sales = []
    invoices = []
    payments = []
    costs = []
    procurement = []
    inventory = []
    cost_centers = [("CC100", "Rooms"), ("CC200", "Food & Beverage"), ("CC300", "Housekeeping"), ("CC400", "Maintenance"), ("CC500", "Sales & Marketing"), ("CC600", "Administration")]
    items = [("I001", "Bath linen", "Housekeeping", 260, 180), ("I002", "Coffee beans", "Food & Beverage", 90, 75), ("I003", "Guest shampoo", "Guest Supplies", 360, 240), ("I004", "HVAC filters", "Maintenance", 60, 45), ("I005", "Bottled water", "Food & Beverage", 420, 300)]
    stock = {i[0]: i[3] for i in items}
    inv_id = pay_id = po_id = sale_id = 1
    season = {1: .72, 2: .75, 3: .82, 4: .78, 5: .80, 6: .88, 7: .95, 8: .93, 9: .84, 10: .86, 11: .76, 12: .90}
    for idx, (year, mon, first_day) in enumerate(month_range()):
        period = f"{year}-{mon:02d}"
        occ = min(.96, max(.58, season[mon] + random.uniform(-.04, .04) + idx * .003))
        rooms_sold = int(ROOMS_AVAILABLE * 30 * occ)
        adr = 145 + (mon in [6,7,8,12]) * 32 + (mon in [1,2]) * -12 + idx * 1.4 + random.uniform(-7, 7)
        room_revenue = rooms_sold * adr
        revenue_split = [("Rooms", .73), ("Food & Beverage", .16), ("Events", .07), ("Other", .04)]
        channel_split = [("Direct", .32), ("OTA", .28), ("Corporate Contract", .22), ("Group Sales", .18)]
        for category, cat_pct in revenue_split:
            for channel, chan_pct in channel_split:
                customer = random.choice(customers)
                amount = room_revenue * cat_pct * chan_pct * random.uniform(.96, 1.04)
                sale_date = first_day + timedelta(days=random.randint(0, 27))
                sales.append({"sale_id": f"S{sale_id:05d}", "sale_date": sale_date.isoformat(), "customer_id": customer["customer_id"], "channel": channel, "revenue_category": category, "net_revenue": round(amount, 2), "rooms_sold": round(rooms_sold * chan_pct if category == "Rooms" else 0)})
                if category in {"Rooms", "Events"}:
                    invoice_amount = round(amount * random.uniform(.88, 1.0), 2)
                    due = sale_date + timedelta(days=30)
                    invoices.append({"invoice_id": f"INV{inv_id:05d}", "customer_id": customer["customer_id"], "invoice_date": sale_date.isoformat(), "due_date": due.isoformat(), "invoice_amount": invoice_amount, "status": "Open"})
                    # purposeful overdue/open records, including all aging buckets at 2025-12-31
                    if not (year == 2025 and mon in [8, 9, 10, 11, 12] and inv_id % 3 == 0):
                        delay = random.choice([-5, 0, 4, 12, 25, 45])
                        paid = invoice_amount * random.choice([1, 1, 1, .65, .8])
                        payments.append({"payment_id": f"PAY{pay_id:05d}", "invoice_id": f"INV{inv_id:05d}", "payment_date": (due + timedelta(days=delay)).isoformat(), "payment_amount": round(paid, 2)})
                        pay_id += 1
                    inv_id += 1
                sale_id += 1
        for cc_id, cc_name in cost_centers:
            base = {"Rooms": 79000, "Food & Beverage": 42000, "Housekeeping": 30000, "Maintenance": 21000, "Sales & Marketing": 24000, "Administration": 27000}[cc_name]
            budget = base * (1 + idx * .002)
            variance_factor = random.uniform(.94, 1.08)
            if cc_name in ["Food & Beverage", "Maintenance"] and mon in [7, 8, 12]:
                variance_factor += .10
            if cc_name == "Administration" and mon in [2, 3, 4]:
                variance_factor -= .08
            costs.append({"period": period, "cost_center_id": cc_id, "cost_center_name": cc_name, "budget_amount": round(budget, 2), "actual_amount": round(budget * variance_factor, 2)})
        for vendor in vendors:
            ordered = first_day + timedelta(days=random.randint(1, 20))
            promised = ordered + timedelta(days=random.randint(3, 8))
            delay = random.choice([0, 0, 1, 2, 4, 7]) if vendor["vendor_id"] in ["V003", "V005"] else random.choice([-1, 0, 0, 1, 2])
            procurement.append({"po_id": f"PO{po_id:05d}", "vendor_id": vendor["vendor_id"], "order_date": ordered.isoformat(), "promised_date": promised.isoformat(), "received_date": (promised + timedelta(days=delay)).isoformat(), "category": vendor["category"], "purchase_amount": round(random.uniform(3000, 16000), 2), "quantity": random.randint(20, 240)})
            po_id += 1
        for item_id, item_name, category, _, reorder_point in items:
            opening = stock[item_id]
            received = random.randint(30, 160)
            issued = random.randint(55, 190) + int(occ * 35)
            closing = max(0, opening + received - issued)
            if item_id in ["I002", "I005"] and mon in [7, 8, 12]:
                closing = min(closing, reorder_point - random.randint(5, 35))
            inventory.append({"period": period, "item_id": item_id, "item_name": item_name, "category": category, "opening_stock": opening, "received_qty": received, "issued_qty": issued, "closing_stock": closing, "reorder_point": reorder_point})
            stock[item_id] = closing
    copy_to_raw_and_processed("calendar_clean.csv", generate_calendar())
    for name, rows in [("customers_clean.csv", customers), ("vendors_clean.csv", vendors), ("sales_revenue_clean.csv", sales), ("customer_invoices_clean.csv", invoices), ("customer_payments_clean.csv", payments), ("cost_center_budget_actual_clean.csv", costs), ("procurement_vendor_clean.csv", procurement), ("inventory_movements_clean.csv", inventory)]:
        copy_to_raw_and_processed(name, rows)


if __name__ == "__main__":
    generate_data()
    print(f"Generated deterministic synthetic data with seed {SEED}.")
