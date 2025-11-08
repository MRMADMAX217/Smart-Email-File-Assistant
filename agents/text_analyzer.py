# agents/text_analyzer.py
from mcp_agent.core.fastagent import FastAgent
from utils.helpers import call_with_instruction

from agents import fast

@fast.agent(
    name="text_analyzer",
    instruction="Analyze text for topics, sentiment, and key sentences.",
)
async def text_analyzer(runtime, text: str):
    instruction = (
        "Analyze the text and return a JSON with:\n"
        "topics: list of 3–6 keywords,\n"
        "sentiment: one-word label (positive/neutral/negative),\n"
        "key_sentences: up to 3 short sentences summarizing main points."
    )
    return await call_with_instruction(runtime, instruction, text)
