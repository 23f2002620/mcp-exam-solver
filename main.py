import hashlib
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MCP Exam Server")

# Enable CORS for MCP client connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NORMALIZED_EMAIL = "23f2002620@ds.study.iitm.ac.in".strip().lower()

@app.api_route("/", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/mcp", methods=["GET", "POST", "OPTIONS"])
async def mcp_endpoint(request: Request):
    if request.method == "OPTIONS":
        return Response(status_code=200)

    if request.method == "GET":
        return JSONResponse({
            "status": "ok",
            "server": "MCP Exam Server",
            "email": NORMALIZED_EMAIL,
            "tool": "solve_challenge"
        })

    try:
        body = await request.json()
    except Exception:
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32700, "message": "Parse error"}
        }, status_code=400)

    req_id = body.get("id")
    method = body.get("method")
    params = body.get("params", {})

    # Handshake 1: MCP initialize
    if method == "initialize":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "mcp-exam-server",
                    "version": "1.0.0"
                }
            }
        })

    # Handshake 2: Initialized notification
    elif method == "notifications/initialized":
        if req_id is not None:
            return JSONResponse({"jsonrpc": "2.0", "id": req_id, "result": {}})
        return Response(status_code=200)

    # Tool Discovery: list tools
    elif method == "tools/list":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "solve_challenge",
                        "description": "Solves the exam challenge using the X-Exam-Challenge header.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }
                ]
            }
        })

    # Execution: call tool
    elif method == "tools/call":
        tool_name = params.get("name")
        if tool_name == "solve_challenge":
            # Extract challenge from HTTP request header (case-insensitive)
            challenge = request.headers.get("x-exam-challenge", "").strip()

            # Hash calculation: SHA-256("${challenge}:${normalizedEmail}")
            to_hash = f"{challenge}:{NORMALIZED_EMAIL}"
            hash_hex = hashlib.sha256(to_hash.encode("utf-8")).hexdigest().lower()
            response_text = hash_hex[:16]

            return JSONResponse({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": response_text
                        }
                    ],
                    "isError": False
                }
            })
        else:
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Tool '{tool_name}' not found"
                }
            }, status_code=400)

    elif method == "ping":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {}
        })

    return JSONResponse({
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": -32601,
            "message": f"Method '{method}' not found"
        }
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)