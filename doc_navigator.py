import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables from .env file
load_dotenv()

# Ensure the Google API key is set
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

def create_vector_store():
    """
    Loads documents, splits them, creates embeddings, and stores them in a FAISS vector store.
    This function should be run once to set up the knowledge base.
    """
    print("Loading documents...")
    # Load markdown documents from the 'docs' directory
    loader = DirectoryLoader('docs/', glob="**/*.md")
    documents = loader.load()

    print("Splitting documents into chunks...")
    # Split documents into smaller chunks for better processing
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    print("Creating embeddings and FAISS vector store...")
    # Create embeddings using Google's model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Create the FAISS vector store from the document chunks and embeddings
    # This will be saved locally in a folder named 'faiss_index'
    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local("faiss_index")
    print("Vector store created and saved locally at 'faiss_index'.")
    return vector_store

def create_rag_chain():
    """
    Creates the complete RAG chain for answering questions.
    """
    # Initialize the Gemini LLM
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

    # Load the locally saved FAISS vector store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    
    # Create a retriever from the vector store
    retriever = vector_store.as_retriever()

    # Define the prompt template
    # This guides the LLM on how to use the context to answer the question
    prompt_template = """
    You are CodeQuest, an expert AI assistant for onboarding software engineers.
    Your goal is to answer questions accurately based on the provided documentation context.
    Provide a clear and concise answer. If the context doesn't contain the answer,
    state that you couldn't find the information in the available documents.

    Context:
    {context}

    Question:
    {input}

    Answer:
    """
    prompt = PromptTemplate.from_template(prompt_template)
    
    # Create the main RAG chain
    rag_chain = (
        create_stuff_documents_chain(llm, prompt)
    )

    # Wrap it in a retrieval chain
    retrieval_chain = create_retrieval_chain(retriever, rag_chain)

    return retrieval_chain

if __name__ == '__main__':
    # First, create and save the vector store
    #create_vector_store()

    # Next, create the RAG chain
    #qa_chain = create_rag_chain()
    
    #print("\n--- RAG Chain Ready. Ask a question! ---")
    
    # Example question
    #question = "How are user passwords stored?"
    
    # Invoke the chain with the question
    #response = qa_chain.invoke({"input": question})
    
    # Print the answer
    #print(f"Question: {question}")
    #print(f"Answer: {response['answer']}")
    pass