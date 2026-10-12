from mcp.server.fastmcp import FastMCP
import pandas as pd
import duckdb
import json

# Initialize the MCP Server
mcp = FastMCP("analytics_mcp_server")

@mcp.tool()
def mcp_profile_csv(file_path: str) -> str:
    """Read a CSV file and return profiling information."""
    try:
        df = pd.read_csv(file_path)
        return json.dumps({
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicates": int(df.duplicated().sum()),
            "data_types": df.dtypes.astype(str).to_dict()
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def mcp_run_duckdb_query(query: str, csv_path: str) -> str:
    """Run safe SQL queries on local CSV files using DuckDB."""
    blocked_commands = ["DELETE", "UPDATE", "DROP", "ALTER", "INSERT", "MERGE", "TRUNCATE", "CREATE"]
    if any(cmd in query.upper() for cmd in blocked_commands):
        return json.dumps({"error": "Only read-only SELECT queries are allowed for safety."})
    try:
        conn = duckdb.connect(database=':memory:')
        conn.execute(f"CREATE TABLE data AS SELECT * FROM read_csv_auto('{csv_path}')")
        result = conn.execute(query).df()
        return result.to_json(orient="records")
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def mcp_validate_sql(query: str) -> str:
    """Validate SQL query safety before execution."""
    query_upper = query.upper()
    if not query_upper.startswith("SELECT"):
        return json.dumps({"status": "invalid", "reason": "Query is not read-only."})
    if "LIMIT" not in query_upper:
        return json.dumps({"status": "warning", "reason": "Query has no LIMIT clause."})
    if "SELECT *" in query_upper:
        return json.dumps({"status": "warning", "reason": "Query avoids specifying columns (SELECT *)."})
    return json.dumps({"status": "valid", "reason": "Query passes basic static safety checks."})

@mcp.tool()
def mcp_detect_data_quality_issues(file_path: str) -> str:
    """Detect common data quality problems."""
    try:
        df = pd.read_csv(file_path)
        return json.dumps({
            "missing_values_total": int(df.isnull().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "constant_columns": [col for col in df.columns if df[col].nunique() <= 1]
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def mcp_generate_kpi_catalog(domain: str) -> str:
    """Generate a KPI catalog from dataset columns and business domain."""
    return json.dumps({
        "domain": domain,
        "kpis": [{
            "name": "Conversion Rate",
            "formula": "orders / sessions",
            "grain": "daily",
            "business_use": "Tracks funnel effectiveness"
        }]
    })

@mcp.tool()
def mcp_recommend_ml_use_cases(columns: str) -> str:
    """Recommend ML use cases based on dataset columns."""
    return json.dumps({
        "ml_use_cases": [{
            "use_case": "churn prediction",
            "problem_type": "classification",
            "business_value": "Reduce customer loss"
        }]
    })

if __name__ == "__main__":
    mcp.run()