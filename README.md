# HR-ASSIST Agentic AI System

**HR-ASSIST** is an agentic AI system designed to help HR teams automate routine workflows. This example demonstrates automation of the employee onboarding process, streamlining tasks that typically require manual intervention.

In terms of technical architecture: for the MCP client we use **Claude Desktop**, and the code base here represents the MCP server with the necessary tools that will be used by the MCP client.

## 🚀 Technical Architecture  
_(Brief overview of how things fit together)_

- The MCP server hosts the orchestration logic, automation tools, and endpoints used by the client.  
- The MCP client (via Claude Desktop) communicates with the server, triggers workflows (e.g., new-employee onboarding), and handles human-agent interactions.  
- The system uses agentic AI principles—automating not just responses, but **actions** (planning, executing tasks) in an HR context.

## 🛠️ Setup Instructions

To set up and run HR-ASSIST, follow these steps:

1. Create/modify `claude_desktop_config.json` in your client environment.  
   Add the following configuration:

   ```json
   {
     "mcpServers": {
       "hr-assist": {
         "command": "...\\.local\\bin\\uv",
         "args": [
           "--directory",
           "C::\\code\\..-hr-assist",
           "run",
           "server.py"
         ],
         "env": {
           "CB_EMAIL": "YOUR_EMAIL",
           "CB_EMAIL_PWD": "YOUR_APP_PASSWORD"
         }
       }
     }
   }
  
2.Run the following commands:
```
 uv init
 uv add mcp[cli]
```

## 📋 Usage

In your Claude Desktop client, click on the “+” icon and select the “Add from hr-assist” option, then send the request.

Fill out the form with details for the new employee, such as name, role, start date, department, etc.

HR-ASSIST will trigger workflows (e.g., IT equipment request, access provisioning, onboarding checklist) automatically.

## 📁 Project Structure (server side)
```
hr-assist/
├── server.py               ← Entry-point for the MCP server  
├── tools/                  ← Automation tools & helper modules  
├── workflows/              ← Definitions for onboarding, tasks, triggers  
├── config/                 ← Configuration files (paths, credentials, etc.)  
└── README.md               ← Project overview (this file)
```
## 🔐 Security & Credentials

Do not commit any credentials, API keys or passwords into the public repository. Use environment variables or secure vaults.

The CB_EMAIL and CB_EMAIL_PWD shown above must be stored securely and never checked into version control.

Agentic AI systems act autonomously—so governance, audit logging and human-in-the-loop oversight are critical.

## 🧩 Why Agentic AI for HR?

Agentic AI is defined as AI systems that not only generate or predict, but act on their own—with contextual planning and execution in a multi‐step workflow.
In an HR context, this means automating end-to-end processes such as onboarding, access provisioning, equipment setup, scheduling training, etc., reducing manual administrative load and improving the employee experience.

## ✅ Future Improvements

Add more onboarding workflows: benefits setup, orientation scheduling, training assignment.

Integrate with HRIS, identity/access management (IAM) systems for seamless automation.

Include audit trail dashboards and checklists for compliance oversight.

Expand the client interface (Claude Desktop) to mobile or chat-based channels (Slack, Teams).

Monitor and improve human-agent interaction feedback loops (e.g., how often human intervention was needed).


