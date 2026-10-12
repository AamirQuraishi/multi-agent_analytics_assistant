import json
from function_tools.supervisor_tools import classify_user_request
from function_tools.analyst_tools import validate_sql_safety, suggest_kpi_metrics
from function_tools.scientist_tools import recommend_ml_problem_type
from mcp_server.server import mcp_validate_sql

def test_classify_user_request():
    result = json.loads(classify_user_request("I need a dashboard for my sales data."))
    assert result["intent"] == "analytics"
    assert result["recommended_agent"] == "Data Analyst Agent"

def test_validate_sql_safety():
    # Should block dangerous commands
    result = json.loads(validate_sql_safety("DROP TABLE users;"))
    assert result["safe"] is False

def test_suggest_kpi_metrics():
    result = json.loads(suggest_kpi_metrics("ecommerce"))
    assert "Total revenue" in result["recommended_kpis"]

def test_recommend_ml_problem_type():
    result = json.loads(recommend_ml_problem_type("predict if a user will churn"))
    assert result["problem_type"] == "classification"

def test_mcp_validate_sql():
    # Should warn about SELECT *
    result = json.loads(mcp_validate_sql("SELECT * FROM data LIMIT 10"))
    assert result["status"] == "warning"