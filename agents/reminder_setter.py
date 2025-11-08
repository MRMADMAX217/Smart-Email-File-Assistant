# agents/reminder_setter.py
from mcp_agent.core.fastagent import FastAgent
import requests, json, re, datetime
from dateparser import parse as parse_date
from agents import fast
from utils.logger import success, info, warn, error  # ✅ for consistent logs


@fast.agent(
    name="reminder_setter",
    instruction="Create a Calendar event via the Calendar MCP using extracted date/time."
)
async def reminder_setter(runtime, summary: str, datetime_info: str):
    """
    Parses extracted date/time info and creates a Calendar event via Gmail MCP server.
    """

    try:
        # =========================================================
        # 1️⃣ Clean the JSON text (LLM output often includes noise)
        # =========================================================
        cleaned = re.sub(r"```(?:json)?", "", datetime_info or "", flags=re.IGNORECASE).strip()
        cleaned = cleaned.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
        cleaned = cleaned.replace('"null"', "null").replace("'null'", "null")

        # =========================================================
        # 2️⃣ Parse JSON safely
        # =========================================================
        try:
            dt_data = json.loads(cleaned) if cleaned else {}
        except json.JSONDecodeError:
            warn(f"Invalid JSON received from LLM: {datetime_info}")
            return {"status": "error", "reason": "Invalid JSON from LLM"}

        # =========================================================
        # 3️⃣ Normalize or recover date using natural-language parsing
        # =========================================================
        if dt_data.get("date"):
            parsed_date = parse_date(dt_data["date"], settings={"DATE_ORDER": "DMY"})
            if parsed_date:
                dt_data["date"] = parsed_date.strftime("%Y-%m-%d")
        else:
            parsed_date = parse_date(summary, settings={"DATE_ORDER": "DMY"})
            if parsed_date:
                dt_data["date"] = parsed_date.strftime("%Y-%m-%d")

        if not dt_data.get("date"):
            warn("No valid date found — skipping event creation.")
            return {"status": "skipped", "reason": "No valid date found", "raw": cleaned}

        start_time = dt_data.get("start_time")
        end_time = dt_data.get("end_time")

        # =========================================================
        # 4️⃣ Compute duration (default 60 minutes)
        # =========================================================
        duration = 60
        if start_time and end_time:
            try:
                t1 = datetime.datetime.strptime(start_time, "%H:%M")
                t2 = datetime.datetime.strptime(end_time, "%H:%M")
                duration = int((t2 - t1).seconds / 60)
            except Exception:
                pass

        # =========================================================
        # 5️⃣ Build accurate ISO start time
        # =========================================================
        try:
            time_for_start = start_time or "09:00"
            iso_base = f"{dt_data['date']} {time_for_start}"
            start_dt = parse_date(iso_base)
            if not start_dt:
                raise ValueError(f"Could not parse datetime: {iso_base}")
            start_dt = start_dt.astimezone(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
            start_iso = start_dt.isoformat()
        except Exception as err:
            error(f"Failed to parse ISO datetime: {err}")
            return {"status": "error", "reason": f"Date parsing failed: {err}"}

        # =========================================================
        # 6️⃣ Prepare payload for MCP
        # =========================================================
        payload = {
            "summary": "Meeting / Call (Auto-detected)",
            "description": summary.strip(),
            "start_iso": start_iso,
            "duration_minutes": duration,
        }

        # =========================================================
        # 7️⃣ Send POST request to Calendar MCP
        # =========================================================
        try:
            info(f"📤 Sending event to MCP: {payload}")
            r = requests.post("http://127.0.0.1:8080/create_event", json=payload, timeout=15)
            info(f"📥 MCP Response Status: {r.status_code}")
            info(f"📥 MCP Response Body: {r.text}")
        except Exception as conn_err:
            error(f"Failed to connect to MCP: {conn_err}")
            return {"status": "error", "reason": str(conn_err), "payload": payload}

        # =========================================================
        # 8️⃣ Handle MCP response
        # =========================================================
        try:
            response_data = r.json()
        except Exception:
            response_data = {"raw_response": r.text, "status_code": r.status_code}

        if r.status_code != 200:
            error(f"Calendar MCP returned {r.status_code}: {response_data}")
            return {
                "status": "failed",
                "reason": f"MCP returned {r.status_code}",
                "response": response_data,
            }

        success("✅ Calendar event successfully created via MCP.")
        return {
            "status": "created",
            "details": {
                "event_id": response_data.get("event_id"),
                "start": response_data.get("start", {}),
                "duration": duration,
                "summary": payload["summary"],
            },
        }

    except Exception as e:
        error(f"Unexpected error in reminder_setter: {e}")
        return {"status": "error", "reason": str(e)}
