# mcp_server/utils/auth_loader.py
import os
from google.oauth2.credentials import Credentials

CREDENTIALS_PATH = os.path.expanduser("~/.gmail-mcp/gcp-oauth.keys.json")
TOKEN_PATH = os.path.expanduser("~/.gmail-mcp/token.json")

def load_credentials():
    """Load authorized credentials from user's token file."""
    if not os.path.exists(TOKEN_PATH):
        raise FileNotFoundError(f"Token file not found at {TOKEN_PATH}")
    return Credentials.from_authorized_user_file(TOKEN_PATH)
