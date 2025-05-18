import os
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")

def rag_function(filepath):
    
    loader = PyPDFLoader(filepath)
    docs = loader.load()
    
    n = 1000
    
    print("- La cantidad de páginas del documento es: ", len(docs))
    print(f"- El primer fragmento en el documento es (sus primeros {n}):")
    print(f"{docs[0].page_content[:n]}\n")
    print("- Metadata del primer documento:")
    print(docs[0].metadata)
    
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200, 
    add_start_index=True
    )

    all_splits = text_splitter.split_documents(docs)

    print(f"- Tamaño del documento despues de splitter: {len(all_splits)}")

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # vector_1 = embeddings.embed_query(all_splits[0].page_content)
    # vector_2 = embeddings.embed_query(all_splits[1].page_content)

    # assert len(vector_1) == len(vector_2)
    # print(f"Vectores de longitud generados {len(vector_1)}\n")
    # print(vector_1[:10])

    vector_store = Chroma(
        collection_name="example_collection",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
    )
    
    ids = vector_store.add_documents(documents=all_splits)
    return vector_store

def rag_user_input(vector_store, user_input):
    if user_input:
        results = vector_store.similarity_search_with_score(user_input)
        doc, score = results[0]
        return doc, score
    return None, None

    # st.caption("2st Question: What was Nike's revenue in 2023?")
    # input_question2 = st.text_input("Enter your question here:")
    # if input_question2:
    #     st.write(f"Question: {input_question2}")
    #     results = vector_store.similarity_search_with_score(input_question2)

    #     doc, score = results[0]
    #     st.write(f"Score: {score}")
    #     st.write(doc)