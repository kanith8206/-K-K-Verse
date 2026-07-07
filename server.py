import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from nicegui import ui

from src.services.ai import fetch_insights_logic, fetch_copilot_logic
from src.App import AppState

load_dotenv()

app = FastAPI()

# Enable CORS for convenience
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PORT = int(os.getenv("PORT", 3000))

# Rest API endpoints preserved for backward compatibility
class InsightsRequest(BaseModel):
    kpis: Dict[str, Any]
    customerSummary: Dict[str, int]
    productSummary: Dict[str, Any]

@app.post("/api/gemini/insights")
async def get_insights(data: InsightsRequest):
    return await fetch_insights_logic(
        kpis=data.kpis,
        customer_summary=data.customerSummary,
        product_summary=data.productSummary
    )

class CopilotMessage(BaseModel):
    role: str
    content: str

class CopilotRequest(BaseModel):
    message: str
    history: Optional[List[CopilotMessage]] = None
    contextData: Dict[str, Any]

@app.post("/api/gemini/copilot")
async def get_copilot(data: CopilotRequest):
    return await fetch_copilot_logic(
        message=data.message,
        history_list=data.history or [],
        context_data=data.contextData
    )

# NiceGUI UI entry page
@ui.page('/')
def index():
    # Load and inject custom CSS stylesheet
    try:
        with open('src/index.css', 'r', encoding='utf-8') as f:
            ui.add_head_html(f'<style>{f.read()}</style>')
    except Exception as e:
        print(f"Error loading index.css: {e}")
    # Instantiates the React-like App entry logic, isolated per user browser tab
    app_state = AppState()
    app_state.render()

# Mount NiceGUI on top of the FastAPI instance
ui.run_with(app, title='KKVerse AI Platform')

if __name__ == "__main__":
    import uvicorn
    # Default port to 3000 if not overridden by env
    is_prod = os.getenv("NODE_ENV") == "production" or os.path.exists("dist")
    default_port = 3000
    port = int(os.getenv("PORT", default_port))
    # We must start uvicorn programmatically, NiceGUI will hook itself onto it
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=not is_prod)
