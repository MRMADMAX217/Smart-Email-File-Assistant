# utils/helpers.py
async def call_with_instruction(runtime, instruction: str, user_text: str):
    """
    Sends an instruction + user input in a unified format to the runtime.
    """
    prompt = f"INSTRUCTION:\n{instruction}\n\nINPUT:\n{user_text}\n\nRespond concisely."
    return await runtime(prompt)
