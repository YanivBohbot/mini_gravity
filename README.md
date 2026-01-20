# 🪐 Mini-Gravity: Autonomous AI Agent with MCP

**Mini-Gravity** is an advanced autonomous agentic system built with **Python**, **LangGraph**, and the **Model Context Protocol (MCP)**. It bridges the gap between Large Language Models (LLMs) and local infrastructure, allowing the AI to execute real-world tasks securely.

[Image of LangChain agent architecture with tools]

## 🚀 Key Features

* **🧠 Cognitive Architecture:** Uses **LangGraph** to manage state, memory, and reasoning loops (Plan → Act → Observe).
* **🔌 Model Context Protocol (MCP):** Implements the official MCP standard to connect the agent to external systems without custom API wrapping.
* **🐘 Database Integration:** Full **PostgreSQL** support via `mcp-server-postgres`, allowing the agent to perform Create, Read, Update, and Delete (CRUD) operations autonomously.
* **🛠️ Tool Ecosystem:** Equipped with capability to manipulate the local filesystem, run terminal commands, and perform web searches.
* **🛡️ Reliability:** Includes recursion limits and error handling to prevent hallucination loops.

[Image of Model Context Protocol architecture]

## 🛠️ Tech Stack

* **Core:** Python 3.11, LangChain, LangGraph
* **Protocol:** Model Context Protocol (MCP) by Anthropic
* **Database:** PostgreSQL (via `uv` managed server)
* **LLM:** ChatGoogleGenerativeAI (Gemini) / OpenAI
* **CI/CD:** GitHub Actions for automated linting and testing

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/mini-gravity.git](https://github.com/your-username/mini-gravity.git)
    cd mini-gravity
    ```

2.  **Set up the environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements

3.  **Install MCP dependencies:**
    ```bash
    pip install mcp langchain-mcp-adapters uv nest_asyncio
    ```

4.  **Configuration:**
    Create a `.env` file and add your API keys:
    ```env
    GOOGLE_API_KEY=your_key_here
    TAVILY_API_KEY=your_key_here
    ```

## 🏃‍♂️ Usage

Ensure your local PostgreSQL server is running, then start the agent:

```bash
python main.py




    
