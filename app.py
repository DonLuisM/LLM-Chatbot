import streamlit as st
import time
from langchain_ollama import ChatOllama
import ollama

# Funciones 
def stream_text(text, delay=0.0002):
    '''
    Función para hacer lograr el correcto funcionamiento del st.write_stream 
    '''
    for word in text.split():
        yield word + " "
        time.sleep(delay)
        
def list_models():
    models_running = ollama.list()['models']
    available_models = [model["model"] for model in models_running]
    return available_models

lista = list_models()

def clc_chat_history():
    st.session_state.message = [{
        "role": "assistant",
        "content": "Hey jefé, En qué puedo ayudarte hoy?"
    }]
    st.session_state.historial = []
            
# -------------------------------------------------------- 
 
st.set_page_config(page_title="Chatbot Conversacional", page_icon="🧠")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hey jefé, En qué puedo ayudarte hoy?"}]

if "historial" not in st.session_state:
    st.session_state.historial = []
        
for message in st.session_state.message:
    role = message.get("role", "")
    content = message.get("content", "")
    
    if role == "user":
        with st.chat_message("user", avatar=":material/sprint:"):
            st.write(content)
    elif role == "assistant":
        with st.chat_message("assistant", avatar=":material/network_intelligence:"):
            st.write(content)

# Configuración barra lateral (Configuración parámetros)
with st.sidebar:
    st.title('🤖 Configuración IA')
    
    left, right = st.columns(2)
    if left.button('Nuevo chat', icon="🗒️", use_container_width=True, on_click=clc_chat_history):
        st.toast("✅ Nuevo chat iniciado.")

    st.session_state.model = st.selectbox('Elije el modelo', lista)
    
    with right.popover("Config.", icon="⚙️"):
        st.session_state.temperature = st.slider(
            'Temperatura',
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.1
        )
        st.session_state.top_p = st.slider(
            'Top P',
            min_value=0.0,
            max_value=1.0,
            value=0.9,
            step=0.1
        )
        st.session_state.top_k = st.slider(
            'Top K',
            min_value=0,
            max_value=100,
            value=50,
            step=1
        )
        st.session_state.max_tokens = st.slider(
            'Max Tokens',
            min_value=1,
            max_value=4096,
            value=256,
            step=1
        )
            
# Configuración userInput
modeloLLM = st.session_state.model

user_input = st.chat_input(
    'Escribe o pega el texto aquí', 
    accept_file=False,
    file_type=["jpg", "jpeg", "png", "pdf", "txt"])
    
if user_input:
    # Mostrar pregunta en un contenedor principal
    with st.container():
        with st.chat_message("user", avatar=":material/sprint:"):
            st.write(user_input)
            
        st.session_state.message.append({"role": "user", "content": user_input})
        
        llm = ChatOllama(
            model = modeloLLM,
            temperature = st.session_state.temperature,
            top_p = st.session_state.top_p,
            top_k = st.session_state.top_k,
            num_predict = st.session_state.max_tokens
        )
    
        # /nothink
        prompt = "You are a bilingual assistant"
        messages = [
            ("system", prompt),
            ("human", user_input)
        ]
  
        # Generar y mostrar respuesta
        with st.status(f"*Modelo pensando...*", expanded=True) as status:
            response = llm.invoke(messages)
            st.write("*🗒️ Procesando información...*")
            time.sleep(1)
            st.write("*🔧 Puliendo detalles...*")
            time.sleep(1)
            st.write("*♟️ Jugando ajedrez...*")
            time.sleep(1)
            st.write("*🧠 Generando respuesta...*")
            time.sleep(1)
            status.update(label = "🤖 Respuesta generada", state="complete", expanded=False)

        if response:
            with st.chat_message("assistant", avatar=":material/network_intelligence:"):
                st.write_stream(stream_text(response.content))
                # Metadata de la respuesta
                st.caption(f"""
                **Detalles Técnicos:**
                - Modelo preciso: {response.response_metadata['model']}
                - Tokens usados: {response.response_metadata['eval_count']}
                - Tiempo respuesta: {response.response_metadata['total_duration'] / 1e9:.2f}s
                """)
    
                # Guardar en historial
                st.session_state.message.append({
                    "role": "assistant", 
                    "content": response.content
                })
                
                st.session_state.historial.append({
                    "modelo": modeloLLM,
                    "pregunta": user_input,
                    "respuesta": response.content,
                    "metadata": response.response_metadata
                })