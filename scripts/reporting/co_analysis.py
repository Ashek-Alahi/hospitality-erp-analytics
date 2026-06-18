from __future__ import annotations
from collections import defaultdict
from pathlib import Path
from scripts.reporting.common import md_table, write_csv


def calculate_cost_center_variance(costs):
    cc = defaultdict(lambda: [0.0, 0.0, ""])
    for row in costs:
        cc[row["cost_center_id"]][0] += float(row["budget_amount"]); cc[row["cost_center_id"]][1] += float(row["actual_amount"]); cc[row["cost_center_id"]][2] = row["cost_center_name"]
    rows=[]
    for cc_id, values in cc.items():
        variance = values[1]-values[0]
        rows.append({"cost_center_id":cc_id,"cost_center_name":values[2],"budget_amount":round(values[0],2),"actual_amount":round(values[1],2),"variance":round(variance,2),"variance_pct":round(variance/values[0]*100,2)})
    return sorted(rows, key=lambda r:r["variance"], reverse=True)


def calculate_profitability(total_revenue, costs):
    total_cost=sum(float(r["actual_amount"]) for r in costs); profit=total_revenue-total_cost; margin=profit/total_revenue*100
    return ([{"metric":"Net revenue","amount":round(total_revenue,2)},{"metric":"Operating cost","amount":round(total_cost,2)},{"metric":"Operating profit","amount":round(profit,2)},{"metric":"Operating profit margin pct","amount":round(margin,2)}], profit, margin)


def write_co_outputs(root:Path, costs, total_revenue, svg_bar):
    rows=calculate_cost_center_variance(costs); profitability, profit, margin=calculate_profitability(total_revenue,costs)
    write_csv(root/"04_CO_Module/outputs/cost_center_variance.csv", rows); write_csv(root/"04_CO_Module/outputs/profitability_summary.csv", profitability)
    svg_bar(root/"04_CO_Module/outputs/cost_center_actuals.svg", "Actual Cost by Cost Center", [r["cost_center_name"] for r in rows], [r["actual_amount"] for r in rows], "#7c3aed")
    from scripts.analytics_pipeline import write_report
    write_report(root/"04_CO_Module/outputs/co_report.md", "CO Analysis Report", [("Key findings", f"Operating profit margin is {margin:.1f}%. Highest unfavorable variance: {rows[0]['cost_center_name']} at {rows[0]['variance_pct']:.1f}%."),("Budget variance ranking", md_table(rows)), ("Management recommendations", "Review departments with positive variance first and document corrective actions without reducing service quality."),("ERP/SAP relevance", "The analysis resembles CO cost center planning versus actual postings and profitability review."),("Limitations", "No allocation cycles, internal orders, activity types, or product/customer profitability ledgers are modeled.")])
    return {"cc_rows":rows,"profitability":profitability,"operating_profit":profit,"margin":margin}
