import asyncio
import os
from dotenv import load_dotenv
from agents import fast

# ======================================================
# === Logger Setup =====================================
# ======================================================
import datetime
from colorama import Fore, Style, init
init(autoreset=True)

def log(message: str, icon: str = "🔹", color=Fore.WHITE):
    """Pretty log messages with emoji and timestamp."""
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.CYAN}[{time_str}]{Style.RESET_ALL} {color}{icon} {message}{Style.RESET_ALL}")

def info(msg): log(msg, "ℹ️", Fore.BLUE)
def success(msg): log(msg, "✅", Fore.GREEN)
def warn(msg): log(msg, "⚠️", Fore.YELLOW)
def error(msg): log(msg, "❌", Fore.RED)
def inbox(msg): log(msg, "📨", Fore.MAGENTA)
def mail(msg): log(msg, "📬", Fore.CYAN)

# ======================================================
# === Environment Setup ================================
# ======================================================
load_dotenv()
success(f"ENV GOOGLE_API_KEY loaded: {bool(os.getenv('GOOGLE_API_KEY'))}")

# === Import all agents ===
from agents.email_receiver import email_receiver
from agents.text_analyzer import text_analyzer
from agents.summarizer import summarizer
from agents.datetime_extractor import datetime_extractor
from agents.reminder_setter import reminder_setter

# ======================================================
# === Chain Definition =================================
# ======================================================
@fast.chain(
    name="email_intelligence_chain",
    sequence=["email_receiver", "text_analyzer", "summarizer", "datetime_extractor", "reminder_setter"],
    instruction="Fetch unread emails, summarize them, extract date/time, and auto-schedule events.",
)
async def orchestrator(runtime):
    inbox("Starting Email Intelligence Chain...")

    emails = await email_receiver(runtime)
    success(f"Found {len(emails)} unread emails.")

    for idx, email in enumerate(emails, start=1):
        mail(f"Processing Email {idx}/{len(emails)}: {email.get('subject', 'No Subject')}")
        try:
            summary = await summarizer(runtime, str(email))
            info(f"Summary generated for Email {idx}")

            datetime_info = await datetime_extractor(runtime, summary)
            success(f"Extracted date/time info for Email {idx}")

            event_result = await reminder_setter(runtime, summary, datetime_info)
            success(f"Event created for Email {idx}")

            print(f"\n{'='*60}")
            print(f"📧 EMAIL {idx}")
            print(f"Subject: {email.get('subject', 'No Subject')}")
            print(f"📝 Summary: {summary.strip()}")
            print(f"📅 Event: {event_result}")
            print(f"{'='*60}")

        except Exception as e:
            error(f"Error processing Email {idx}: {e}")

    success("✅ Chain execution complete.\n")


# ======================================================
# === Entrypoint =======================================
# ======================================================
if __name__ == "__main__":
    async def main():
        success("🚀 Email Intelligence App starting up...")
        async with fast.run() as runtime:
            await orchestrator(runtime)
        success("🏁 Email Intelligence App finished.")

    asyncio.run(main())
