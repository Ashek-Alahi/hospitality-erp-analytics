# SAP S/4HANA-Inspired ERP Analytics Architecture

The following Mermaid diagram provides a text-based architecture view that can be reviewed directly in GitHub.

```mermaid
flowchart LR
    subgraph Data["Synthetic / anonymized CSV data"]
        C[Customers]
        V[Vendors]
        S[Sales Revenue]
        I[Customer Invoices]
        P[Customer Payments]
        CC[Cost Center Budget Actual]
        PR[Procurement]
        INV[Inventory Movements]
    end

    subgraph ERP["SAP S/4HANA-inspired module layer"]
        FI[FI: AR, revenue trend, cash collections]
        CO[CO: budget vs actual, profitability]
        SD[SD: channel, category, customer segment revenue]
        MM[MM: spend, vendor delivery, reorder alerts]
    end

    subgraph Analytics["Analytics and reporting layer"]
        PY[Python pipeline and validation]
        SQL[SQLite-compatible schema and import guidance]
        FC[Baseline forecasting]
        KPI[KPI summary]
        DASH[HTML dashboard and SVG charts]
        DOC[Markdown business reports]
    end

    C --> S
    C --> I
    I --> P
    V --> PR
    S --> SD
    S --> FI
    I --> FI
    P --> FI
    CC --> CO
    PR --> MM
    INV --> MM
    FI --> PY
    CO --> PY
    SD --> PY
    MM --> PY
    PY --> FC
    PY --> KPI
    PY --> DASH
    PY --> DOC
    Data --> SQL
```

## Architecture Notes

- The repository uses flat CSV files instead of a live ERP database so reviewers can inspect every input and output in GitHub.
- `scripts/validate_data.py` checks required files, columns, dates, non-negative values, foreign-key consistency, and blocked binary extensions before the analytics pipeline runs.
- `scripts/analytics_pipeline.py` regenerates Markdown reports, CSV summaries, SVG charts, forecasting outputs, and the HTML dashboard.
- The architecture is intentionally lightweight and portfolio-oriented; it demonstrates ERP analytics workflow design rather than SAP system administration or SAP implementation work.
