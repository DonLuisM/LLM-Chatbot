import streamlit as st
import time
from langchain_ollama import ChatOllama
import ollama


def stream_text(text):
    '''
    Función para hacer lograr el correcto funcionamiento del st.write_stream 
    '''
    for char in text:
        yield char
        time.sleep(0.02)
        
st.write("## Chat Conversacional")
st.write('### Bienvenido')

if 'message' not in st.session_state:
    st.session_state.message = []
    
for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.write(message["content"])
    
# Configuración barra lateral (Configuración parámetros)
with st.sidebar:
    st.write('## Configuración IA')
    
    left, right = st.columns(2)
    if left.button('Nuevo chat', icon="🗒️", use_container_width=True):
        st.session_state.message = []
        st.session_state.nuevo_chat = True
        
    if st.session_state.get("nuevo_chat"):
        st.toast("✅ Nuevo chat iniciado.")
        st.session_state.nuevo_chat = False
    

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
modeloLLM = 'qwen3'
user_input = st.chat_input(
    'Escribe o pega el texto aquí', 
    accept_file=False,
    file_type=["jpg", "jpeg", "png", "pdf", "txt"])

with st.chat_message("assistant", avatar=":material/network_intelligence:"):
    st.write("Hey boss, How can I help you today? \n\n What word or phrase do you want to translate?")
    
if user_input:
    # Mostrar pregunta en un contenedor principal
    with st.container():
        with st.chat_message("user", avatar=":material/sprint:"):
            st.write(user_input)
          
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
        st.write_stream(stream_text(response.content))
    
    # Metadata de la respuesta
    st.caption(f"""
    **Detalles Técnicos:**
    - Temperatura: {st.session_state.temperature}
    - Tokens usados: {response.response_metadata['eval_count']}
    - Tiempo respuesta: {response.response_metadata['total_duration'] / 1e9:.2f}s
    - Modelo preciso: {response.response_metadata['model']}
    - Tokens entrada: {response.usage_metadata['input_tokens']}
    """)
    
    # Guardar en historial
    st.session_state.message.append({
        "modelo": modeloLLM,
        "pregunta": user_input,
        "respuesta": response.content,
        "metadata": response.response_metadata
    })