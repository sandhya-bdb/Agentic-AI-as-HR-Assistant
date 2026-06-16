# 🤖 HR Assistant — Agentic AI for HR Automation

An intelligent, agentic AI system that automates routine HR workflows using **Claude Desktop** as the AI client and a custom **MCP (Model Context Protocol) server** as the backend. The assistant can manage employees, leaves, meetings, procurement tickets, send emails, and now — answer any HR policy question using **Docling-powered document intelligence**.

---

## ✨ What's New — Docling RAG Integration

The HR Assistant now includes a **knowledge base built from your HR Policy PDF** using [Docling](https://github.com/DS4SD/docling) — IBM's document AI library. This means Claude can answer policy questions like:

- *"How many casual leaves am I entitled to?"*
- *"What is the work-from-home policy?"*
- *"What happens during the probation period?"*

...with answers grounded in the **actual company document**, not guesswork.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Desktop (Client)                  │
│                  You chat / ask questions here               │
└───────────────────────────┬─────────────────────────────────┘
                            │  MCP Protocol (stdio / JSON)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     server.py  (MCP Server)                  │
│                                                              │
│  ┌─────────────────┐   ┌──────────────────────────────┐    │
│  │   HRMS Tools    │   │     HR Policy RAG Tool        │    │
│  │                 │   │                               │    │
│  │ • add_employee  │   │  answer_hr_policy_question()  │    │
│  │ • apply_leave   │   │         │                     │    │
│  │ • schedule_mtg  │   │         ▼                     │    │
│  │ • create_ticket │   │      rag.py                   │    │
│  │ • send_email    │   │         │                     │    │
│  └─────────────────┘   │  DocumentConverter            │    │
│                        │  ResultPostprocessor          │    │
│                        │  HierarchicalChunker          │    │
│                        │  SentenceTransformer          │    │
│                        │  Cosine Similarity Search     │    │
│                        └──────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### How MCP Works

**MCP (Model Context Protocol)** is Anthropic's open standard that lets Claude communicate with external tools running locally on your machine.

1. You ask Claude a question in Claude Desktop
2. Claude decides which tool to use (e.g., `answer_hr_policy_question`)
3. Claude sends a **JSON request** over `stdio` to `server.py`
4. `server.py` runs the tool logic and returns the result as JSON
5. Claude reads the result and responds in natural language

The MCP server is launched **automatically** by Claude Desktop using the path in `claude_desktop_config.json`. All processing happens **locally** — your data never leaves your machine.

### How Docling RAG Works

```
HR Policy PDF
      │
      ▼
DocumentConverter         ← Parses PDF layout, tables, headings
      │
      ▼
ResultPostprocessor       ← Fixes and resolves heading hierarchy
      │
      ▼
HierarchicalChunker       ← Splits into semantically meaningful chunks
      │                      Each chunk knows its full heading path:
      │                      ['HR Policies', 'Leave', 'Casual Leave']
      ▼
SentenceTransformer       ← Embeds each chunk into a vector
      │
      ▼
[At query time]
      │
      ▼
retrieve(query)           ← Cosine similarity search
      │
      ▼
Top-k chunks → Claude     ← Claude answers using this context
```

Unlike `RecursiveCharacterTextSplitter` or LangChain's `DoclingLoader`, this approach preserves the **full hierarchical heading path** on every chunk — so Claude always knows the section context of what it's reading.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| AI Client | Claude Desktop |
| Tool Protocol | MCP (Model Context Protocol) |
| MCP Framework | FastMCP |
| Document Parsing | Docling (`DocumentConverter`) |
| Heading Hierarchy | `docling-hierarchical-pdf` (`ResultPostprocessor`) |
| Chunking | `HierarchicalChunker` |
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| Vector Search | NumPy cosine similarity |
| HRMS Backend | Custom Python (in-memory) |
| Email | SMTP via Gmail |
| Package Manager | `uv` |

---

## 📁 Project Structure

```
hr-assist/
├── server.py               ← MCP server entry point — all tools defined here
├── rag.py                  ← Docling RAG pipeline (load, chunk, embed, retrieve)
├── utils.py                ← Seeds HRMS with dummy employee/leave/meeting data
├── emails.py               ← Email sending via SMTP
├── hrms/                   ← HRMS business logic
│   ├── __init__.py
│   ├── schemas.py          ← Pydantic models
│   ├── employee_manager.py
│   ├── leave_manager.py
│   ├── meeting_manager.py
│   └── ticket_manager.py
├── Resources/              ← Supporting assets
├── pyproject.toml          ← Dependencies
├── sample.env              ← Environment variable template
└── README.md
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- [Claude Desktop](https://claude.ai/download) installed

### 1. Clone the repo

```bash
git clone https://github.com/sandhya-bdb/HR_Assistant_using_AgenticAI.git
cd HR_Assistant_using_AgenticAI
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Set up environment variables

```bash
cp sample.env .env
```

Edit `.env` and fill in:
```
CB_EMAIL=your_gmail@gmail.com
CB_EMAIL_PWD=your_gmail_app_password
```

> For Gmail, generate an **App Password** at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

### 4. Configure Claude Desktop

Find your Claude Desktop config file:
- **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following (replace paths with your actual paths):

```json
{
  "mcpServers": {
    "hr-assist": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/path/to/HR_Assistant_using_AgenticAI",
        "run",
        "server.py"
      ],
      "env": {
        "CB_EMAIL": "your_gmail@gmail.com",
        "CB_EMAIL_PWD": "your_app_password"
      }
    }
  }
}
```

> Find your `uv` path by running `which uv` in Terminal.

### 5. Restart Claude Desktop

Quit Claude (`Cmd+Q`) and reopen it. You should see **hr-assist** appear under Connectors (`+` button in chat).

---

## 🧰 Available Tools

| Tool | Description |
|---|---|
| `answer_hr_policy_question` | Answers any question from the HR policy PDF using RAG |
| `add_employee` | Adds a new employee to the HRMS |
| `get_employee_details` | Looks up employee info by name |
| `apply_leave` | Applies leave for an employee |
| `get_employee_leave_balance` | Checks remaining leave balance |
| `get_leave_history` | Shows past leave records |
| `schedule_meeting` | Schedules a meeting |
| `get_meetings` | Lists meetings for an employee |
| `cancel_meeting` | Cancels a scheduled meeting |
| `create_ticket` | Raises a procurement ticket (laptop, ID card, etc.) |
| `update_ticket_status` | Updates ticket status |
| `list_tickets` | Lists tickets for an employee |
| `send_email` | Sends an email via Gmail SMTP |

### Prompt
| Prompt | Description |
|---|---|
| `onboard_new_employee` | End-to-end onboarding workflow (add employee → email → tickets → meeting) |

---

## 💬 Example Queries

```
"What is the casual leave policy at AtliqAI?"
"How many sick leaves can I take?"
"What is the probation period for new hires?"
"Onboard a new employee named Priya Sharma under manager David Wilson"
"What is Tony Sharma's leave balance?"
"Schedule a meeting for E003 tomorrow at 10 AM"
```

---

## 🔮 Future Improvements

- Integrate with a real HRIS (e.g., BambooHR, Darwinbox)
- Add Qdrant/ChromaDB for persistent vector storage
- Support multiple HR policy documents
- Add audit logging for all agent actions
- Expand to Slack/Teams as alternate MCP clients

---

## 📄 License

MIT License — feel free to use, modify, and distribute.
