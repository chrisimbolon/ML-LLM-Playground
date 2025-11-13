"""
CortexOS - RAG Prototype 🤘
A minimal but functional AI document chat system
Built with LangChain, OpenAI, and ChromaDB

Requirements:
pip install langchain langchain-openai langchain-community chromadb pypdf python-dotenv

Setup:
1. Create a .env file with: OPENAI_API_KEY=your_key_here
2. Place a PDF in the same directory
3. Run this script and ask questions!
"""

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()

class CortexRAG:
    """The brain of your AI companion - RAG pipeline"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",  # Cheaper and faster for testing
            temperature=0.7
        )
        self.vectorstore = None
        self.qa_chain = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
    def ingest_document(self):
        """Load, chunk, and embed the document 📄➡️🧠"""
        print(f"🔥 Loading document: {self.pdf_path}")
        
        # Load PDF
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        
        print(f"✅ Loaded {len(documents)} pages")
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Adjust based on your needs
            chunk_overlap=200,  # Overlap to maintain context
            length_function=len
        )
        chunks = text_splitter.split_documents(documents)
        
        print(f"✂️  Split into {len(chunks)} chunks")
        
        # Create vector store
        print("🚀 Creating embeddings... (this might take a moment)")
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory="./chroma_db"  # Saves to disk
        )
        
        print("💾 Vector store created and persisted!")
        
    def setup_qa_chain(self):
        """Set up the conversational retrieval chain 🔗"""
        if not self.vectorstore:
            raise ValueError("Must ingest document first!")
        
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 4}  # Retrieve top 4 relevant chunks
            ),
            memory=self.memory,
            return_source_documents=True,
            verbose=True  # See what's happening under the hood
        )
        
        print("🎸 QA Chain is ready to rock!")
        
    def chat(self, question: str):
        """Ask a question and get an answer 💬"""
        if not self.qa_chain:
            raise ValueError("Must setup QA chain first!")
        
        print(f"\n🎤 You: {question}")
        print("🤔 Thinking...")
        
        response = self.qa_chain.invoke({"question": question})
        
        answer = response["answer"]
        sources = response["source_documents"]
        
        print(f"\n🤖 Cortex: {answer}")
        print(f"\n📚 Sources: Found {len(sources)} relevant chunks")
        
        # Show source snippets
        for i, doc in enumerate(sources[:2], 1):  # Show first 2 sources
            print(f"\n   Source {i} (Page {doc.metadata.get('page', 'N/A')}):")
            print(f"   {doc.page_content[:150]}...")
        
        return answer


def main():
    """Rock and roll! 🎸"""
    print("="*60)
    print("🧠 CORTEXOS - RAG PROTOTYPE")
    print("="*60)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment!")
        print("Create a .env file with: OPENAI_API_KEY=your_key_here")
        return
    
    # Get PDF path
    pdf_path = input("\n📄 Enter path to your PDF (or press Enter for 'document.pdf'): ").strip()
    if not pdf_path:
        pdf_path = "document.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: {pdf_path} not found!")
        return
    
    # Initialize Cortex
    cortex = CortexRAG(pdf_path)
    
    # Ingest document
    cortex.ingest_document()
    
    # Setup QA chain
    cortex.setup_qa_chain()
    
    # Chat loop
    print("\n" + "="*60)
    print("💬 CHAT MODE - Ask me anything about your document!")
    print("Type 'quit' or 'exit' to stop")
    print("="*60 + "\n")
    
    while True:
        question = input("\n🎤 You: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n🤘 Rock on! Exiting...")
            break
        
        if not question:
            continue
        
        try:
            cortex.chat(question)
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()