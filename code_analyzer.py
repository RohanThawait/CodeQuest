import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

# Load environment variables
load_dotenv()

# Ensure the Google API key is set
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

def create_code_analyzer_chain():
    """Creates a LangChain chain to analyze and explain code snippets."""
    
    # Initialize the Gemini LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

    # Define the detailed prompt template
    prompt_template = """
    You are CodeQuest, an expert AI software architect. Your task is to analyze and explain the following code snippet.
    Provide a clear, structured explanation that would be helpful for a new engineer.

    Format your response as follows:
    **1. Purpose:** Briefly describe the overall goal of this code.
    **2. Language:** Identify the programming language.
    **3. Breakdown:** Provide a step-by-step explanation of what the code is doing. Explain complex lines or logic in detail.
    **4. Architectural Context & Best Practices:** Suggest how this code might fit into a larger application. Mention any potential improvements, best practices, or design patterns (e.g., error handling, modularity, performance).

    Here is the code snippet:
    ---
    {code_snippet}
    ---
    """
    
    prompt = PromptTemplate.from_template(prompt_template)
    
    # Create the analysis chain
    # The chain pipes the user input to the prompt, then to the LLM, and finally parses the output
    chain = prompt | llm | StrOutputParser()
    
    return chain

def format_code_for_terminal(code, language):
    """Uses Pygments to add syntax highlighting to the code for terminal output."""
    try:
        lexer = get_lexer_by_name(language, stripall=True)
        return highlight(code, lexer, TerminalFormatter())
    except:
        # Fallback if the language is not found or pygments fails
        return code

if __name__ == '__main__':
    # Create the analyzer chain
    #analyzer_chain = create_code_analyzer_chain()
    
    # Example Python code snippet for analysis
    #sample_code = """
#def factorial(n):
    #if n < 0:
    #    return "Factorial does not exist for negative numbers"
    #elif n == 0:
    #    return 1
    #else:
    #    return n * factorial(n-1)
#"""
    
    #print("--- Code Analyzer Ready ---")
    #print("Analyzing the following code snippet:")
    
    # Print the code with syntax highlighting
    #print(format_code_for_terminal(sample_code, 'python'))
    
    # Invoke the chain with the code
    #explanation = analyzer_chain.invoke({"code_snippet": sample_code})
    
    # Print the explanation
    #print("\n--- Explanation ---")
    #print(explanation)
    pass