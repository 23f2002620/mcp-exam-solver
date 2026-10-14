# mcp-exam-solver

A Model Context Protocol (MCP) server implementation deployed over HTTPS, fully compliant with JSON-RPC 2.0. It exposes the `solve_challenge` tool and processes per-call exam challenges passed via HTTP headers.

**Live Endpoint:** `https://mcp-exam-solver.onrender.com/`
**M8ven Score:** [![M8ven Score](https://m8ven.ai/badge/mcp/23f2002620-mcp-exam-solver-vewrxx?v=1c8694a10d433f61ae24e1c6234e300d)](https://m8ven.ai/mcp/23f2002620-mcp-exam-solver-vewrxx?s=readme)
---

## Features

- **Protocol Compliance:** Handles `initialize`, `notifications/initialized`, `tools/list`, and `tools/call`.
- **Header Processing:** Dynamically reads challenge tokens from the `X-Exam-Challenge` HTTP header instead of request body parameters.
- **SHA-256 Digest Verification:** Returns the first 16 lowercase hex characters of `SHA-256("${challenge}:23f2002620@ds.study.iitm.ac.in")`.

---

## Specification Summary

| Property | Value |
| --- | --- |
| **Tool Name** | `solve_challenge` |
| **Input Schema** | `{ "type": "object", "properties": {} }` |
| **Header Dependency** | `X-Exam-Challenge` |
| **Registered Email** | `23f2002620@ds.study.iitm.ac.in` |

---

## Repository Structure

mcp-exam-solver/
├── main.py          # FastAPI application implementing MCP endpoint
├── requirements.txt # Python dependencies (fastapi, uvicorn)
├── Procfile         # Web service command for deployment
└── README.md        # Documentation

## Local Development
Clone the repository:

```Bash
git clone [https://github.com/YOUR_USERNAME/mcp-exam-solver.git](https://github.com/YOUR_USERNAME/mcp-exam-solver.git)
cd mcp-exam-solver
```

Install dependencies:

```Bash
pip install -r requirements.txt
```

Start the local server:

```Bash
python main.py
```

The local endpoint will run on http://localhost:8000.

## Testing the Live Deployment

1. Tool Discovery (tools/list)

```Bash
curl -X POST [https://mcp-exam-solver.onrender.com/](https://mcp-exam-solver.onrender.com/) \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list"
  }
```

2. Tool Execution (tools/call)

```Bash
curl -X POST [https://mcp-exam-solver.onrender.com/](https://mcp-exam-solver.onrender.com/) \
  -H "Content-Type: application/json" \
  -H "X-Exam-Challenge: 0123456789abcdef0123456789abcdef" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "solve_challenge",
      "arguments": {}
    }
  }`
```
