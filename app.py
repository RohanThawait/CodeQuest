# app.py

import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Import our custom modules
from doc_navigator import create_rag_chain
from code_analyzer import create_code_analyzer_chain

# --- Initialization ---
# Load environment variables from .env
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the Slack App with your bot token and socket mode handler
app = App(token=os.environ["SLACK_BOT_TOKEN"])

# --- Pre-load AI Chains ---
# For efficiency, we create the chains once when the app starts
logging.info("Initializing AI chains... This might take a moment.")
try:
    doc_qa_chain = create_rag_chain()
    code_analyzer_chain = create_code_analyzer_chain()
    logging.info("AI chains initialized successfully.")
except Exception as e:
    logging.error(f"Error initializing AI chains: {e}")
    # Exit if chains fail to load, as the bot is non-functional
    exit()

# --- Slack Event Handlers ---
@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    """
    This function is triggered when the bot is @mentioned in a channel.
    """
    event = body["event"]
    message_text = event["text"]
    channel_id = event["channel"]
    thread_ts = event.get("thread_ts", event["ts"]) # Reply in a thread

    # Extract the user's actual query by removing the bot mention
    # This is a simple way; a more robust solution might use regex
    user_query = message_text.split(">", 1)[-1].strip()

    # Routing logic: check for a code block
    if "```" in user_query:
        # This is a code analysis request
        logger.info("Received a code analysis request.")
        say(text="Analyzing the code snippet... 🧠", thread_ts=thread_ts)
        
        try:
            # The user query itself is the code snippet here
            response = code_analyzer_chain.invoke({"code_snippet": user_query})
            say(text=f"Here's the analysis:\n\n{response}", thread_ts=thread_ts)
        except Exception as e:
            logger.error(f"Error during code analysis: {e}")
            say(text="Sorry, I encountered an error while analyzing the code.", thread_ts=thread_ts)

    else:
        # This is a documentation question
        logger.info("Received a documentation question.")
        say(text="Searching the documentation... 📚", thread_ts=thread_ts)
        
        try:
            response = doc_qa_chain.invoke({"input": user_query})
            say(text=response["answer"], thread_ts=thread_ts)
        except Exception as e:
            logger.error(f"Error during documentation lookup: {e}")
            say(text="Sorry, I encountered an error while searching the docs.", thread_ts=thread_ts)

# --- Start the App ---
if __name__ == "__main__":
    logging.info("Starting CodeQuest bot...")
    # SocketModeHandler is used for a secure connection without exposing a public URL
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()