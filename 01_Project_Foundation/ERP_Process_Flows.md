# ERP Process Flows

These Mermaid diagrams describe SAP S/4HANA-inspired process logic represented by the prototype. They are conceptual only and do not show a live SAP system.

## Order-to-cash / revenue-to-cash flow
```mermaid
flowchart LR
A[Customer demand] --> B[Revenue transaction]
B --> C[Customer invoice]
C --> D[Incoming payment]
D --> E[Collection KPI]
E --> F[Executive dashboard]
```
Revenue is tracked separately from cash collection so management can see whether sales activity becomes cash.

## Invoice-to-cash flow
```mermaid
flowchart LR
A[Invoice issued] --> B[Due date monitored]
B --> C{Paid?}
C -- Yes --> D[Cleared invoice]
C -- No --> E[AR aging bucket]
E --> F[Collection action]
```
FI analysis highlights open receivables and overdue exposure.

## Procure-to-pay flow
```mermaid
flowchart LR
A[Operational need] --> B[Purchase order concept]
B --> C[Vendor delivery]
C --> D[Goods receipt timing]
D --> E[Vendor performance KPI]
```
MM reporting focuses on supplier reliability and spend visibility.

## Inventory replenishment flow
```mermaid
flowchart LR
A[Inventory movement] --> B[Closing stock]
B --> C{At or below reorder point?}
C -- Yes --> D[Reorder alert]
C -- No --> E[Monitor]
D --> F[Management action register]
```
Reorder alerts identify items that can affect guest service levels.

## Cost center budget review flow
```mermaid
flowchart LR
A[Budget] --> C[Variance calculation]
B[Actual cost] --> C
C --> D{Unfavorable variance?}
D -- Yes --> E[Department review]
D -- No --> F[Continue monitoring]
```
CO analysis supports department accountability and margin protection.

## Executive KPI reporting flow
```mermaid
flowchart LR
A[Validated CSV data] --> B[Module calculations]
B --> C[KPI summary]
B --> D[Exception reports]
C --> E[HTML dashboard]
D --> E
E --> F[Executive actions]
```
The dashboard consolidates module-level outputs into management reporting.
