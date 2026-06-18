from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from scripts.generate_synthetic_data import ROOMS_AVAILABLE
from scripts.reporting.common import md_table, write_csv


def group_sum(rows, key, value):
    grouped=defaultdict(float)
    for row in rows: grouped[row[key]] += float(row[value])
    return [{key:k, value:round(v,2)} for k,v in sorted(grouped.items(), key=lambda x:-x[1])]


def calculate_hospitality_kpis(sales):
    total_revenue=sum(float(r["net_revenue"]) for r in sales); rooms_sold=sum(float(r["rooms_sold"]) for r in sales); room_rev=sum(float(r["net_revenue"]) for r in sales if r["revenue_category"]=="Rooms"); months=sorted({r["sale_date"][:7] for r in sales})
    occ=rooms_sold/(ROOMS_AVAILABLE*30*len(months))*100; adr=room_rev/rooms_sold; revpar=room_rev/(ROOMS_AVAILABLE*30*len(months))
    return total_revenue, rooms_sold, room_rev, months, occ, adr, revpar


def calculate_revenue_by_channel(sales): return group_sum(sales,"channel","net_revenue")
def calculate_revenue_by_segment(sales, customers):
    vals=defaultdict(float)
    for row in sales: vals[customers[row["customer_id"]]["segment"]] += float(row["net_revenue"])
    return [{"segment":k,"net_revenue":round(v,2)} for k,v in sorted(vals.items(), key=lambda x:-x[1])]


def write_sd_outputs(root:Path, sales, customers, svg_bar):
    total, rooms, room_rev, months, occ, adr, revpar=calculate_hospitality_kpis(sales)
    category=group_sum(sales,"revenue_category","net_revenue"); channel=calculate_revenue_by_channel(sales); segments=calculate_revenue_by_segment(sales,customers); hospitality=[{"kpi":"Occupancy rate pct","value":round(occ,2)},{"kpi":"ADR","value":round(adr,2)},{"kpi":"RevPAR","value":round(revpar,2)}]
    write_csv(root/"05_SD_Module/outputs/revenue_by_category.csv",category); write_csv(root/"05_SD_Module/outputs/revenue_by_channel.csv",channel); write_csv(root/"05_SD_Module/outputs/customer_segment_revenue.csv",segments); write_csv(root/"05_SD_Module/outputs/hospitality_kpis.csv",hospitality)
    svg_bar(root/"05_SD_Module/outputs/revenue_by_channel.svg","Revenue by Sales Channel",[r["channel"] for r in channel],[r["net_revenue"] for r in channel],"#059669")
    from scripts.analytics_pipeline import write_report
    write_report(root/"05_SD_Module/outputs/sd_report.md","SD Analysis Report",[("Key findings",f"Occupancy is {occ:.1f}%, ADR is {adr:,.2f}, and RevPAR is {revpar:,.2f}."),("Hospitality KPIs",md_table(hospitality)),("Revenue by channel",md_table(channel)),("Revenue by segment",md_table(segments)),("Business meaning","Channel and segment mix should guide pricing, promotion timing, and direct-booking strategy."),("ERP/SAP relevance","This is SD-inspired order/billing analytics connected to customer master segments and revenue categories."),("Limitations","No reservations system integration, cancellations, commissions, loyalty tiering, or daily room type inventory is included.")])
    return {"total_revenue":total,"occupancy_rate":occ,"adr":adr,"revpar":revpar,"category":category,"channel":channel,"segments":segments}
