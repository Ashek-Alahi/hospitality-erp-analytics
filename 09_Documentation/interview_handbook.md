# Interview Handbook

## A. 30-second explanation
This is a SAP S/4HANA-inspired hospitality ERP analytics prototype using deterministic synthetic data. It connects FI, CO, SD, MM, forecasting, SQL, Python automation, tests, reports, and a static dashboard to show how hotel management can review revenue, cash collection, cost control, procurement, inventory, and planning signals.

## B. 1-minute explanation
I built this as a portfolio project to demonstrate ERP and business analytics thinking. The data is synthetic and deterministic, so anyone can run `python run_all.py` and reproduce the outputs. The project generates FI receivables and collection KPIs, CO cost-center variance and profitability, SD hospitality KPIs and revenue segmentation, MM vendor and inventory exceptions, simple forecast baselines, SQL-ready data, Markdown reports, SVG charts, tests, and an HTML dashboard. It is not a real SAP implementation.

## C. 3-minute explanation
The business scenario is a fictional hotel group with disconnected reporting across finance, sales, procurement, inventory, and cost control. I modeled ERP-style master and transaction CSV data, validated it, and built a Python pipeline that creates module-level analytics and executive reporting. FI connects invoices, payments, AR aging, and collection rate. CO compares budget and actual cost centers and calculates operating profit margin. SD analyzes revenue by category, channel, segment, occupancy, ADR, and RevPAR. MM reviews purchase spend, vendor delays, and reorder alerts. Forecasting compares simple baseline methods with MAPE and MAE. The dashboard and action register summarize what management should review first. The key strength is business interpretation and defensible scope honesty, not pretending to be a live SAP project.

## Recruiter questions and answers
1. **Tell me about this project.** It is an ERP analytics portfolio project for hospitality using synthetic data and a reproducible Python pipeline.
2. **Why did you build it?** To demonstrate accounting, ERP, SAP-inspired process knowledge, Python, SQL, testing, and business reporting together.
3. **Was this academic or personal?** It is a portfolio project built to demonstrate job-ready analytics capabilities.
4. **Did you use real data?** No. The data is deterministic synthetic/anonymized data.
5. **What was your role?** I designed the scenario, data model, pipeline, KPIs, reports, tests, and documentation.
6. **Which tools did you use?** Python standard library, pytest, SQL files, Markdown, SVG, and static HTML.
7. **Which output should I review first?** Start with the README, dashboard, final project report, and executive action register.
8. **How is this related to ERP?** It maps transactions and master data to FI, CO, SD, MM, and analytics reporting concepts.
9. **How is this related to business analytics?** It converts process data into KPIs, controls, exceptions, and management actions.
10. **What is the limitation?** It is not a real SAP implementation and uses simplified synthetic data.

## ERP/business analyst questions and answers
1. **What business problem does this project solve?** Disconnected hotel reporting across revenue, receivables, costs, procurement, and inventory.
2. **Which ERP modules are represented?** FI, CO, SD, MM, and analytics/forecasting.
3. **How does FI connect with SD?** SD revenue creates commercial activity; FI invoices and payments show whether that activity becomes cash.
4. **How does MM support hotel operations?** It monitors vendors, spend, delivery delays, and stock risk for operating supplies.
5. **Why is AR aging important?** It ranks open receivables by overdue exposure for collection action.
6. **Why is cost center variance important?** It shows departments where actual spend differs from budget.
7. **What is the difference between revenue and cash collection?** Revenue records sales activity; cash collection records payment received.
8. **How would management use this dashboard?** To identify KPIs, exceptions, and owners requiring action.
9. **What controls are visible in this project?** AR aging, collection rate, variance review, vendor delay monitoring, reorder alerts, and forecast error review.
10. **How would this be different in a real SAP implementation?** It would use configured organizational structures, real master data, authorizations, posting logic, SAP tables/APIs, workflows, and controlled deployment.

## Technical/project defense questions and answers
1. **How does the data pipeline work?** `run_all.py` generates data, validates it, calculates module outputs, writes reports, and updates the dashboard.
2. **How is synthetic data generated?** Python scripts create deterministic CSV files with repeatable business patterns.
3. **How is data validated?** Validation checks required files, required columns, basic values, and blocked binary file types.
4. **Why did you avoid binary dashboard files?** Text-based artifacts are easier to review on GitHub and align with the project rules.
5. **How do tests verify the project?** Pytest runs the pipeline and checks key outputs, formulas, documentation, and binary restrictions.
6. **How are KPIs calculated?** Transparent formulas are documented in the KPI formula catalog and implemented in Python.
7. **Why are simple forecasts used?** Baseline models are easier to explain and appropriate for a portfolio prototype.
8. **What would you improve in a real company version?** Add real governed data sources, access controls, dimensional modeling, production orchestration, and business sign-off.
9. **What part is not production-grade?** Forecasting, data volume, controls, integrations, and deployment are simplified.
10. **How did you avoid overclaiming?** The README, dashboard, and documentation explicitly state the prototype scope and synthetic data basis.

## What I should NOT claim
- Do not claim real SAP implementation.
- Do not claim real company data.
- Do not claim production deployment.
- Do not claim Power BI dashboard if no `.pbix` is included.
- Do not claim advanced ML.
- Do not claim direct SAP table extraction.
