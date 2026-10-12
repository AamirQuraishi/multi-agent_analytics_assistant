import json
from crewai.tools import tool

@tool("Recommend ML Problem Type")
def recommend_ml_problem_type(description: str) -> str:
    """Classify the ML use case."""
    description = description.lower()
    if "churn" in description or "yes/no" in description or "fraud" in description:
        return json.dumps({"problem_type": "classification", "reason": "The goal is to predict a discrete categorical outcome."})
    elif "price" in description or "revenue" in description or "sales" in description:
        return json.dumps({"problem_type": "regression", "reason": "The goal is to predict a continuous numerical value."})
    return json.dumps({"problem_type": "clustering", "reason": "The goal is to find natural groupings in the data."})

@tool("Suggest Feature Engineering")
def suggest_feature_engineering(data_context: str) -> str:
    """Suggest features from raw event or transaction data."""
    return json.dumps({
        "features": [
            "User activity in last 1 hour",
            "Average transaction amount",
            "Days since last purchase",
            "Failed event ratio",
            "Session duration"
        ]
    })

@tool("Detect ML Data Risks")
def detect_ml_data_risks(dataset_description: str) -> str:
    """Identify risks before model training."""
    return json.dumps({
        "risks": [
            "Class imbalance in target variable",
            "Data leakage from future features",
            "High-cardinality categorical columns",
            "Outliers skewing numerical distributions"
        ]
    })

@tool("Recommend Evaluation Metrics")
def recommend_evaluation_metrics(problem_type: str) -> str:
    """Suggest evaluation metrics based on the ML problem type."""
    metrics = {
        "classification": ["Precision", "Recall", "F1-score", "ROC-AUC"],
        "regression": ["RMSE", "MAE", "R-Squared"]
    }
    return json.dumps({
        "problem_type": problem_type,
        "metrics": metrics.get(problem_type.lower(), ["Accuracy"]),
        "business_note": "Ensure metrics align with the business cost of false positives vs false negatives."
    })