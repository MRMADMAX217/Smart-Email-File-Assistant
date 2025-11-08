# agents/email_receiver.py
import requests
from mcp_agent.core.fastagent import FastAgent

from agents import fast

@fast.agent(
    name="email_receiver",
    instruction="Fetch recent unread Gmail messages using Gmail MCP and return them as text.",
)
async def email_receiver(runtime):
    try:
        res = requests.get("http://localhost:8080/emails", timeout=10)
        res.raise_for_status()
        emails = res.json()
        print(f"✅ Received {len(emails)} email(s) from Gmail MCP.")
        return emails
    except Exception as e:
        print(f"❌ Error fetching emails from Gmail MCP: {e}")
        return [f"Error fetching emails from Gmail MCP: {e}"]
