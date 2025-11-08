# # mcp_server/app.py
# from flask import Flask
# from mcp_server.routes.email_routes import email_bp
# from mcp_server.routes.calendar_routes import calendar_bp


# app = Flask(__name__)

# # Register routes
# app.register_blueprint(email_bp)
# app.register_blueprint(calendar_bp)

# @app.route('/')
# def index():
#     return {"message": "✅ Gmail MCP running", "routes": ["/emails", "/create_event"]}

# if __name__ == "__main__":
#     print("🚀 Gmail MCP Server running at http://localhost:8080")
#      # 🔍 List all routes before running
#     print("\n📜 Registered routes:")
#     for rule in app.url_map.iter_rules():
#         print(f"➡️  {rule}")
#     app.run(host="127.0.0.1", port=8080)



# mcp_server/main.py
from fastapi import FastAPI
from mcp_server.routes.email_routes import router as email_router
from mcp_server.routes.calendar_routes import router as calendar_router
from utils.logger import success

app = FastAPI(title="📬 Gmail MCP Server")

# Include routers
app.include_router(email_router)
app.include_router(calendar_router)

@app.get("/")
async def root():
    return {"message": "✅ Gmail MCP running", "routes": ["/emails", "/create_event"]}

if __name__ == "__main__":
    success("🚀 Starting Gmail MCP FastAPI server at http://127.0.0.1:8080")
    import uvicorn
    uvicorn.run("mcp_server.main:app", host="127.0.0.1", port=8080, reload=True)
