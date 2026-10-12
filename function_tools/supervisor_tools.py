import json
from crewai.tools import tool

@tool("Classify User Request")
def classify_user_request(request: str) -> str:
    """Classify the user request into analytical categories."""
    request_lower = request.lower()
    if any(kw in request_lower for kw in ["ml", "predict", "forecast", "model"]):
        return json.dumps({"intent": "data_science", "recommended_agent": "Data Scientist Agent", "reason": "Requires machine learning expertise."})
    elif any(kw in request_lower for kw in ["sql", "dashboard", "kpi"]):
        return json.dumps({"intent": "analytics", "recommended_agent": "Data Analyst Agent", "reason": "Requires reporting and data analysis."})
    return json.dumps({"intent": "mixed", "recommended_agent": "Both", "reason": "Request covers both analytics and ML."})

@tool("Create Agent Work Plan")
def create_agent_work_plan(request: str) -> str:
    """Generate a step-by-step work plan for the agents."""
    return json.dumps({
        "steps": [
            "Ask Data Analyst Agent to profile the dataset.",
            "Ask Data Analyst Agent to suggest dashboard KPIs.",
            "Ask Data Scientist Agent to identify ML use cases.",
            "Combine both outputs into a final answer."
        ]
    })

@tool("Validate Final Response Structure")
def validate_final_response_structure(response: str) -> str:
    """Check whether the final response contains required sections."""
    required_sections = ["Direct Answer", "Architecture", "Tools Used", "Step-by-Step Plan", "Risks", "Final Recommendation"]
    missing = [sec for sec in required_sections if sec.lower() not in response.lower()]
    if not missing:
        return json.dumps({"status": "Valid", "message": "All required sections are present."})
    return json.dumps({"status": "Invalid", "missing_sections": missing})

@tool("Estimate Context Usage")
def estimate_context_usage(estimated_input_tokens: int) -> str:
    """Estimate how much of the model context window is being used."""
    context_window = 8192
    usage_percent = round((estimated_input_tokens / context_window) * 100, 2)
    return json.dumps({
        "estimated_input_tokens": estimated_input_tokens,
        "context_window": context_window,
        "usage_percent": usage_percent
    })