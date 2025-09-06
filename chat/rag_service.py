import os
import faiss
import numpy as np
import ollama
from sentence_transformers import SentenceTransformer

client = ollama.Client(host='http://localhost:11434')

class RAGService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base_path = 'knowledge_base'
        self.documents = []
        self.document_embeddings = None
        self.index = None
        self._load_and_index_documents()

    def _load_and_index_documents(self):
        for filename in os.listdir(self.knowledge_base_path):
            if filename.endswith(".txt"):
                with open(os.path.join(self.knowledge_base_path, filename), 'r') as f:
                    self.documents.append(f.read())

        if not self.documents:
            print("Warning: No documents found in knowledge base.")
            return

        self.document_embeddings = self.model.encode(self.documents, convert_to_tensor=False)
        dimension = self.document_embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(self.document_embeddings, dtype=np.float32))

    def retrieve_documents(self, query, k=2):
        if self.index is None:
            return []
        
        query_embedding = self.model.encode([query])
        query_embedding_np = np.array(query_embedding, dtype=np.float32)
        
        distances, indices = self.index.search(query_embedding_np, k)
        
        return [self.documents[i] for i in indices[0]]

    def generate_response(self, query, retrieved_docs):
        """
        Generates a response using a local Ollama model.
        """
        if not retrieved_docs:
            prompt = f"Answer the following question: {query}"
        else:
            context = "\n\n".join(retrieved_docs)
            prompt = f"Based on the following context, answer the user's question.\n\nContext:\n{context}\n\nQuestion: {query}"
        
        try:
            response = client.chat(
                model='phi3:mini',
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return "Sorry, I'm having trouble connecting to the local AI service. Is Ollama running?"

rag_service_instance = RAGService()