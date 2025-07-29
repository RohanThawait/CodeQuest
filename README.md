# 🤖 CodeQuest: Your AI Onboarding Companion

CodeQuest is an AI-powered agent designed to streamline the onboarding process for software engineers. It integrates directly into Slack, answering questions about documentation and explaining complex code snippets to help new hires get up to speed faster.

*(**Action Item:** Replace the placeholder above with a screen recording or GIF of you interacting with the bot in Slack\!)*

-----

## 🎯 The Problem

Software engineer onboarding is often a slow and expensive process. New engineers face scattered documentation, complex codebases, and limited access to senior engineers' time. This leads to lost productivity and frustration. CodeQuest tackles this by providing an instant, context-aware knowledge source.

-----

## ✨ Key Features

  * **Documentation Navigator:** Ask questions in natural language and get answers sourced directly from your project's documentation. The system uses a Retrieval-Augmented Generation (RAG) pipeline to provide accurate, context-aware responses.
  * **Code Understanding:** Paste a snippet of code and ask CodeQuest to explain it. The bot provides a breakdown of the code's purpose, language, and logic, along with architectural context and best practices.
  * **Seamless Slack Integration:** Interact with CodeQuest directly within your team's workspace, ensuring a smooth and natural workflow.

-----

## 🛠️ Tech Stack & Architecture

This project was built using a modern, modular architecture, leveraging powerful AI tools.

  * **AI & Machine Learning:**
      * **Language Model:** Google Gemini Pro
      * **Framework:** LangChain
      * **Embeddings:** Google's `embedding-001` Model
      * **Vector Store:** FAISS (Facebook AI Similarity Search)
  * **Backend & Integration:**
      * **Language:** Python
      * **Slack Integration:** `slack-bolt`
      * **Environment Management:** `python-dotenv`

### Architecture Overview

CodeQuest uses a router-based approach within the Slack bot.

1.  **Slack Listener:** The bot listens for `@mentions` in Slack channels.
2.  **Request Router:** When mentioned, it analyzes the message.
      * If the message contains a code block (`...`), it's routed to the **Code Analyzer**.
      * Otherwise, it's treated as a documentation question and routed to the **Documentation Navigator**.
3.  **RAG Pipeline (Documentation):** The question is used to retrieve relevant text chunks from the FAISS vector store, which are then passed to the Gemini model along with the original question to generate an answer.
4.  **LLM Chain (Code Analysis):** The code snippet is inserted into a specialized prompt and sent directly to the Gemini model for a detailed explanation.

-----

## 🚀 Getting Started

Follow these steps to set up and run CodeQuest locally.

### Prerequisites

  * Python 3.8+
  * A Slack workspace where you can install apps.
  * API keys for Google AI and Slack.

### 1\. Clone the Repository

```bash
git clone https://github.com/your-username/codequest.git
cd codequest
```

### 2\. Set Up Environment

Create and activate a virtual environment.

```bash
# Create the virtual environment
python -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate
# Or (Windows)
# venv\Scripts\activate
```

Install the required dependencies.

```bash
pip install -r requirements.txt
```

### 3\. Configure API Keys

Create a `.env` file in the root directory and add your API keys.

```
# .env file
GOOGLE_API_KEY="YOUR_GOOGLE_AI_API_KEY"
SLACK_BOT_TOKEN="YOUR_xoxb-SLACK_BOT_TOKEN"
SLACK_APP_TOKEN="YOUR_xapp-SLACK_APP_TOKEN"
```

### 4\. Populate the Knowledge Base

1.  Add your project's Markdown documentation files to the `/docs` directory.
2.  Run the `doc_navigator.py` script once to create the local vector store.

<!-- end list -->

```bash
python doc_navigator.py
```

This will create a `faiss_index` folder containing the knowledge base.

### 5\. Run the Bot

Start the Slack bot.

```bash
python app.py
```

Invite the bot to a channel in your Slack workspace and start asking it questions\!

-----

## 💬 Usage Examples

**1. Ask a question about the documentation:**

`@CodeQuest-Bot what is the database technology used?`

**2. Ask for a code explanation:**

`@CodeQuest-Bot please explain this code snippet:`</br>
`  ```python `</br>
`def __init__(self, key):`</br>
`     self.key = key `</br>
` ``` `
