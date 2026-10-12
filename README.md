# Multi-Agent Analytics Assistant

A Streamlit app where a team of AI agents answers analytics questions. A **Supervisor** agent reads the request and delegates it to a **Data Analyst** (SQL, KPIs, dashboards, EDA) or a **Data Scientist** (ML strategy, modeling, experiments), then combines their answers. The language models run locally through [Ollama](https://ollama.com), so no data leaves the machine.

Built as a course project at E&ICT Academy, IIT Roorkee (Machine Learning & Agentic AI program), with AI coding assistance.

## How it works

- **Agents and tasks** are defined in YAML (`config/agents.yaml`, `config/tasks.yaml`): role, goal, backstory, delegation settings and iteration limits.
- **CrewAI** runs the team in hierarchical mode: the Supervisor is the manager agent and delegates to the specialists.
- **Ollama** serves the local model (default `llama3.2:3b`); the model can be chosen in the sidebar.
- **Streamlit** provides the chat interface and a timeline of agent events.

## Also in this repo

- `mcp_server/server.py`: a local [Model Context Protocol](https://modelcontextprotocol.io) server (FastMCP) with tools to profile a CSV, run read-only SQL on a CSV with DuckDB, validate SQL, and detect data-quality issues. It also contains two placeholder tools (KPI catalog, ML use cases) that return fixed example output.
- `function_tools/`: plain Python helper functions for each agent (classify a request, suggest KPIs, recommend an ML problem type, and so on).
- `tests/test_tools.py`: 5 unit tests for these tools.
- `docs/architecture.md`: the intended architecture diagram.

**Current status:** the MCP server and helper tools are standalone modules with tests. `app.py` does not call them yet, so the running app uses the agents and the local LLM only. Connecting the agents to the MCP tools is the next step.

## Project structure

```text
app.py                      Streamlit app and CrewAI crew
requirements.txt
config/
  agents.yaml               Agent definitions
  tasks.yaml                Task prompt for the Supervisor
function_tools/             Helper functions per agent
mcp_server/
  server.py                 FastMCP server
  sample_data/events_sample.csv
tests/test_tools.py
docs/architecture.md
```

## Run it

1. Install [Ollama](https://ollama.com), then pull a model and start the server:
   ```bash
   ollama pull llama3.2:3b
   ollama serve
   ```
2. Install Python dependencies (Python 3.10+ recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```
4. Run the tests:
   ```bash
   pip install pytest
   python -m pytest
   ```

If it is slow, lower `max_iter` in `config/agents.yaml` or use a smaller model.

## Known limitations

- Small local models (1B to 4B parameters) are slow and not always reliable at following delegation instructions.
- The SQL safety check is a keyword blocklist, which is not a complete defense, and file paths are inserted into the query string. Treat it as a demonstration, not production security.
- The KPI and ML use-case MCP tools are placeholders.

## Tech stack

Python, CrewAI, Ollama, Streamlit, FastMCP (MCP), DuckDB, Pandas, YAML.
