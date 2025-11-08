# # mcp_server/routes/email_routes.py
# from flask import Blueprint, jsonify
# from mcp_server.utils.auth_loader import load_credentials
# from mcp_server.services.gmail_service import get_unread_emails

# email_bp = Blueprint('email_bp', __name__)

# @email_bp.route('/emails', methods=['GET'])
# def fetch_emails():
#     try:
#         creds = load_credentials()
#         emails = get_unread_emails(creds)
#         return jsonify(emails)
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return jsonify({"error": str(e)}), 500


# mcp_server/routes/email_routes.py
from fastapi import APIRouter
from mcp_server.utils.auth_loader import load_credentials
from mcp_server.services.gmail_service import fetch_emails
from utils.logger import inbox, success, error

router = APIRouter()

@router.get("/emails")
async def get_emails():
    """Fetch unread Gmail emails via MCP."""
    try:
        inbox("/emails endpoint called")
        creds = load_credentials()
        emails = fetch_emails(creds)
        success(f"✅ Returning {len(emails)} email(s)")
        return emails
    except Exception as e:
        error(f"❌ Error fetching emails: {e}")
        return {"error": str(e)}
