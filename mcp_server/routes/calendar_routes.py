# # mcp_server/routes/calendar_routes.py
# from flask import Blueprint, request, jsonify
# from mcp_server.utils.auth_loader import load_credentials
# from mcp_server.services.calendar_service import create_calendar_event

# calendar_bp = Blueprint('calendar_bp', __name__)

# @calendar_bp.route('/create_event', methods=['POST'])
# def create_event():
#     try:
#         creds = load_credentials()
#         data = request.get_json(force=True)
#         result = create_calendar_event(creds, data)
#         return jsonify(result), 200
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return jsonify({"error": str(e)}), 500



# mcp_server/routes/calendar_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from mcp_server.utils.auth_loader import load_credentials
from mcp_server.services.calendar_service import create_calendar_event
from utils.logger import info, success, error

router = APIRouter()

class EventRequest(BaseModel):
    summary: str
    description: str
    start_iso: str | None = None
    duration_minutes: int = 30

@router.post("/create_event")
async def create_event(req: EventRequest):
    """Create a calendar event via MCP."""
    try:
        info("📅 /create_event endpoint called")
        creds = load_credentials()
        result = create_calendar_event(creds, req.dict())
        success("✅ Calendar event created successfully")
        return result
    except Exception as e:
        error(f"❌ Exception in /create_event: {e}")
        return {"error": str(e)}
