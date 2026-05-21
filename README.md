# Sales Performance Dashboard

An end-to-end business intelligence and AI-powered sales analytics project built on the Superstore dataset. This project includes an interactive Streamlit web app with Prophet-based sales forecasting and a Power BI executive dashboard.

---

## Live Demo

- **Streamlit App:** [salesdash-eqrgynfdg3ax5hnyezjr7d.streamlit.app](https://salesdash-eqrgynfdg3ax5hnyezjr7d.streamlit.app)
- **Power BI Dashboard:** Available in this repo as `Sales Dashboard.pptx`

---

## Project Overview

This project analyzes 9,994 sales transactions (2014–2017) across regions, categories, and customer segments to surface actionable business insights and forecast future revenue using machine learning.

### Key Findings
- **18.7% of orders are loss-making** — primarily driven by excessive discounting in the Central region
- **Central region averages a 24% discount rate** vs 10.9% in the West, resulting in a -10.41% average profit margin
- **Tables and Bookcases** are the worst-performing sub-categories, losing $17,725 and $3,472 respectively despite significant revenue
- **Any discount above 20% results in average losses** — orders discounted 61–90% lose $1.22 per dollar of margin
- **Copiers, Phones, and Paper** are the most profitable sub-categories
- Revenue grew from $484K (2014) to $733K (2017), with consistent year-over-year profit growth

---

## Features

### Streamlit Dashboard
- **8 KPI cards** — Total Revenue, Profit, Margin %, Orders, Customers, Loss Orders, Loss Rate, Avg Ship Duration
- **Dynamic sidebar filters** — filter all visuals by Year, Region, and Category simultaneously
- **Sales & Profit by Region** — clustered bar chart
- **Yearly Trend** — line chart showing revenue and profit growth 2014–2017
- **Sub-Category Profit Breakdown** — horizontal bar chart with color gradient
- **Discount Impact Analysis** — shows how discount bands affect profit margin
- **AI Sales Forecasting** — Facebook Prophet model with adjustable forecast horizon (30–365 days) and confidence intervals
- **Loss Orders Analysis** — charts and table of the 20 worst-performing orders

### Power BI Dashboard
- Executive-style layout with KPI cards, slicers, and matrix table
- Region vs Category profit matrix with conditional formatting (red = loss, green = profit)
- DAX measures for Total Sales, Total Profit, Profit Margin %, and Loss Orders
- Drilldown-capable visuals for regional and category analysis

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Data cleaning, EDA, feature engineering |
| Pandas | Data manipulation and transformation |
| Plotly | Interactive charts in Streamlit |
| Streamlit | Web app framework and deployment |
| Prophet | AI-powered sales forecasting |
| Power BI | Executive BI dashboard |
| DAX | Custom measures and calculations |
| Git/GitHub | Version control |

---

## Dataset

**Source:** [Superstore Sales Dataset — Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

| Field | Description |
|---|---|
| 9,994 rows | Individual order line items |
| 21 columns | Order details, customer info, product info, financials |
| Date range | January 2014 – December 2017 |
| Geography | United States (4 regions, 49 states) |

---

## Project Structure

```
salesdash/
├── app.py                        # Streamlit dashboard application
├── requirements.txt              # Python dependencies
├── Sales Dashboard.pptx          # Power BI dashboard export
├── dashboard_preview.png         # Dashboard screenshot
└── data/
    ├── superstore_cleaned.csv    # Cleaned dataset used by the app
    └── store.csv                 # Original raw dataset
```

---

## Setup & Installation

### Prerequisites
- Python 3.9 or higher
- pip

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/Asteroid12/salesdash.git
cd salesdash
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the Streamlit app**
```bash
streamlit run app.py
```

**4. Open in browser**
```
http://localhost:8501
```

---

## Data Cleaning & Feature Engineering

The raw dataset was cleaned and enriched in Google Colab before being used in the dashboard:

- Converted `Order Date` and `Ship Date` from string to datetime
- Fixed `Postal Code` from integer to string type
- Extracted `Year`, `Month`, `Month Name`, and `Quarter` from Order Date
- Engineered `Profit Margin %` = (Profit / Sales) × 100
- Engineered `Ship Duration` = Ship Date − Order Date in days
- Created `Is Loss` boolean flag for orders where Profit < 0
- Created `Discount Band` categorical feature grouping discounts into 5 bands

---

## Author

**Amogh Iyengar**  
MS Information Technology Management — Applied Data Science & AI  
Illinois Institute of Technology  
[LinkedIn](https://linkedin.com/in/amoghi) | [GitHub](https://github.com/Asteroid12)
