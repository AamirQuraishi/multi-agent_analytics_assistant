# Multi-Agent Analytics Assistant Architecture

```mermaid
graph TD
    User([User]) -->|Inputs Prompt| UI[Streamlit UI]
    UI -->|Sends History & Prompt| Supervisor[Supervisor Agent]
    
    Supervisor -->|Delegates Analytics Tasks| Analyst[Data Analyst Agent]
    Supervisor -->|Delegates ML Tasks| Scientist[Data Scientist Agent]
    
    Supervisor -.->|Local Tools| STools[Classify Intent, Work Plan, Validate]
    Analyst -.->|Local Tools| ATools[Profile DF, KPIs, SQL Safety]
    Scientist -.->|Local Tools| SCTools[ML Problem Type, Feature Eng, Risk Detect]
    
    Analyst ==>|JSON RPC| MCP[Local MCP Server]
    Scientist ==>|JSON RPC| MCP
    
    MCP -->|Tools| MTools[DuckDB Query, CSV Profile, Detect Issues]
    MTools --> Data[(Sample Datasets)]
    
    Analyst -->|Returns Findings| Supervisor
    Scientist -->|Returns Findings| Supervisor
    Supervisor -->|Combined Final Answer| UI