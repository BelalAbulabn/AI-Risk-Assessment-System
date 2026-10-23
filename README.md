# AI Risk Assessment System

Master's thesis project (University of Stuttgart, IAS, grade 1.3): automated risk management with LLM agents.

The system supports an FMEA-style risk analysis for industrial machines. A pipeline of LLM agents works step by step through failure modes, causes, effects, recommended actions and risk evaluation. Asset data is managed in an Asset Administration Shell (AAS) model.

## Structure

- `WebApp/` – Flask web app with the agent pipeline (`agents.py`, `llm.py`)
- `AssetAdministrationShellV2/` – AAS data model (Flask, SQLAlchemy)
- `FMEA Collection Data/` – reference FMEA tables used during development

## Run

```bash
cd WebApp
pip install flask flask-cors flask-caching openai python-dotenv
cp ../.env.example .env   # then add your own OPENAI_API_KEY
python app.py
```
