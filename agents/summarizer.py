# agents/summarizer.py
from mcp_agent.core.fastagent import FastAgent
from utils.helpers import call_with_instruction
from agents import fast

@fast.agent(
    name="summarizer",
    instruction="Summarize the given text clearly, avoiding hallucination.",
)
async def summarizer(runtime, text: str, max_length: int = 80):
    instruction = (
        f"Write a concise summary in about {max_length} words. "
        "Focus only on the information present in the input."
    )
    return await call_with_instruction(runtime, instruction, text)
