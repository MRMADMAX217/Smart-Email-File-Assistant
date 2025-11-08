# utils/logger.py
import datetime
from colorama import Fore, Style, init

# Initialize colorama (for cross-platform colored output)
init(autoreset=True)

def log(message: str, icon: str = "🔹", color=Fore.WHITE):
    """Print a formatted log message with timestamp, emoji, and color."""
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.CYAN}[{time_str}]{Style.RESET_ALL} {color}{icon} {message}{Style.RESET_ALL}")

def info(msg): log(msg, "ℹ️", Fore.BLUE)
def success(msg): log(msg, "✅", Fore.GREEN)
def warn(msg): log(msg, "⚠️", Fore.YELLOW)
def error(msg): log(msg, "❌", Fore.RED)
def inbox(msg): log(msg, "📨", Fore.MAGENTA)
def mail(msg): log(msg, "📬", Fore.CYAN)
