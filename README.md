# Structure Flow

A split-screen web application that generates diagrams from natural language prompts via a chat interface.

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + TypeScript + Vite |
| Diagramming | Mermaid.js |
| Backend | FastAPI (Python) |
| Package management | uv |

## Getting started

### Prerequisites

- Python ≥ 3.11
- Node.js ≥ 18
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Configure environment

```bash
cp backend/.env.example backend/.env
```

The default config (`MODEL_PROVIDER=stub_openai`) uses stub responses — no API keys required.
