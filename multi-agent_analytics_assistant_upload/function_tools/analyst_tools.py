import pandas as pd
import json
from crewai.tools import tool

@tool("Profile DataFrame")
def profile_dataframe(file_path: str) -> str:
    """Profile a local CSV or DataFrame."""
    try:
        df = pd.read_csv(file_path)
        return json.dumps({
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_rows": int(df.duplicated().sum())
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool("Suggest KPI Metrics")
def suggest_kpi_metrics(domain: str) -> str:
    """Suggest KPIs based on dataset columns and business domain."""
    kpis = {
        "ecommerce": ["Total revenue", "Average order value", "Repeat purchase rate", "Order cancellation rate", "Monthly active customers"],
        "finance": ["Net Profit Margin", "Gross Margin", "Operating Cash Flow"],
        "saas": ["Monthly Recurring Revenue (MRR)", "Churn Rate", "Customer Acquisition Cost (CAC)"]
    }
    return json.dumps({"recommended_kpis": kpis.get(domain.lower(), ["Total Users", "Active Sessions", "Conversion Rate"])})

@tool("Generate Dashboard Layout")
def generate_dashboard_layout(dashboard_name: str) -> str:
    """Suggest a dashboard structure."""
    return json.dumps({
        "dashboard_name": dashboard_name,
        "sections": ["Revenue Overview", "Customer Segments", "Product Performance", "Churn Indicators"]
    })

@tool("Validate SQL Safety")
def validate_sql_safety(query: str) -> str:
    """Check whether a SQL query is safe."""
    query_upper = query.upper()
    blocked_keywords = ["DELETE", "UPDATE", "DROP", "ALTER", "INSERT"]
    
    if any(keyword in query_upper for keyword in blocked_keywords):
        return json.dumps({"safe": False, "reason": "Query contains blocked modification commands."})
    if "SELECT *" in query_upper:
        return json.dumps({"safe": True, "warning": "SELECT * is used. Consider specifying columns for performance."})
    return json.dumps({"safe": True, "message": "Query is read-only and safe."})