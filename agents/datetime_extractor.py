# agents/datetime_extractor.py
from mcp_agent.core.fastagent import FastAgent
from utils.helpers import call_with_instruction

from agents import fast

@fast.agent(
    name="datetime_extractor",
    instruction="Extract date, start and end times from summarized text and return JSON."
)
async def datetime_extractor(runtime, text: str):
    instruction = (
        "From the text, extract scheduling details as pure JSON (no markdown or extra text):\n"
        "{\n"
        '  "date": "YYYY-MM-DD",\n'
        '  "start_time": "HH:MM",\n'
        '  "end_time": "HH:MM"\n'
        "}\n\n"
        "- Convert natural-language dates like 'November 15th' or 'next Monday' to valid ISO format.\n"
        "- Convert '4 p.m. to 8 p.m.' or '11:00am–12:30pm' into start_time and end_time in 24-hour format.\n"
        "- Use 2025 as the default year.\n"
        "- If one of the times is missing, set it to null.\n"
        "- Return only valid JSON (no backticks or explanations)."
    )
    return await call_with_instruction(runtime, instruction, text)
