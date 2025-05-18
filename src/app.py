"""
Desarrollo parte Interfaz con Streamlit, solicitud de función RAG. 
Modelo de Chatbot Intermedio con RAG
"""
import time
import os
import ollama
import streamlit as st
from langchain_ollama import ChatOllama
from rag import rag_function, rag_user_input

if not os.path.exists("data"):
    os.mkdir("data")

# * ------------ Funciones -----------
def stream_text(text):
    '''
    Función para hacer lograr el correcto funcionamiento del st.write_stream 
    '''
    for word in text:
        yield word
        time.sleep(0.022)

def list_models():
    '''
    Función para enlistar los modelos de ollama locales
    '''
    models_running = ollama.list()['models']
    available_models = [model["model"] for model in models_running]
    return available_models

lista = list_models()

def clc_chat_history():
    '''
    Función para limpiar el historial a partir del botón
    '''
    st.session_state.message = [{
        "role": "assistant",
        "content": "Hey jefé, soy tu asistente CORTEXiRAG. En qué puedo ayudarte hoy?"
    }]
    st.session_state.historial = []
    st.session_state.pdf_loaded = False
    st.session_state.pdf_vector = None

# * --------------------------------------------------------
st.set_page_config(page_title="CORTEXiRAG BOT", page_icon="🧠")

if "message" not in st.session_state:
    st.session_state.message = [{
        "role": "assistant", 
        "content": "Hey jefé, En qué puedo ayudarte hoy?"
    }]

if "historial" not in st.session_state:
    st.session_state.historial = []

if "pdf_vector" not in st.session_state:
    st.session_state.pdf_vector = None

if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

for message in st.session_state.message:
    role = message.get("role", "")
    content = message.get("content", "")

    if role == "user":
        with st.chat_message("user", avatar=":material/sprint:"):
            st.write(content)
    elif role == "assistant":
        with st.chat_message("assistant", avatar=":material/network_intelligence:"):
            st.write(content)

# * Configuración barra lateral (Configuración parámetros)
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

    st.divider()

    with st.form("Sube tu archivo", clear_on_submit=True):
        upload_file = st.file_uploader(
            "Sube tu archivo PDF",
            accept_multiple_files=False,
            type = ['pdf'],
        )

        submitted_file = st.form_submit_button("Subir archivo")

        if submitted_file and upload_file is not None:
            st.write(f"Archivo subido: *{upload_file.name}*")

            filepath = os.path.join("data/", upload_file.name)
            with open(filepath, "wb") as f:
                f.write(upload_file.getbuffer())

            with st.spinner("*Leyendo documento...*"):
                vector = rag_function(filepath)
                st.session_state.pdf_vector = vector
                st.session_state.pdf_loaded = True
                st.success("Cargado con éxito")
    
    st.info("""Para usar mis herramientas de RAG, primero sube el archivo y después me preguntas. 
            \n
            \nTambién puedes preguntarme cualquier cosa sin necesidad de archivo. ƪ(˘⌣˘)ʃ""", icon=':material/info:')

# * Configuración userInput
modeloLLM = st.session_state.model

user_input = st.chat_input(
'Escribe que deseas saber del documento', 
accept_file=True,
file_type=["jpg", "jpeg", "png"],)

if user_input is None:
    st.caption("""1st Q: Cómo debería limpiar el módulo base del equipo? 
               \n\n 2nd Q: Que es el modo cortical? 
               \n\n 3rd Q: Quien pertenecía al Reform-Club?
               \n\n 4th Q: Quien es el autor del libro?""")

if st.session_state.pdf_vector and st.session_state.pdf_loaded:
    if user_input and user_input.text:
        with st.container():
            with st.chat_message("user", avatar=":material/sprint:"):
                st.write(user_input.text)

            st.session_state.message.append({"role": "user", "content": user_input.text})

            llm = ChatOllama(
                model = modeloLLM,
                temperature = st.session_state.temperature,
                top_p = st.session_state.top_p,
                top_k = st.session_state.top_k,
                num_predict = st.session_state.max_tokens
            )

            with st.spinner("*Buscando respuestas...*"):
                doc, score = rag_user_input(st.session_state.pdf_vector, user_input.text)

            # /nothink
            prompt = f"Responde con base en el siguiente contexto:{doc}\nPregunta:{user_input}"
            messages = [
                ("system", "Eres un asistente que responde basandote en el contexto dado y brindas respuestas detalladas y concisas"),
                ("human", prompt)
            ]

            # * Generar y mostrar respuesta
            with st.status("*Modelo pensando...*", expanded=True) as status:
                response = llm.invoke(messages)
                st.write("*🗒️ Procesando información...*")
                time.sleep(1)
                st.write("*🔧 Puliendo detalles...*")
                time.sleep(1)
                st.write("*♟️ Jugando ajedrez...*")
                time.sleep(1)
                st.write("*🧠 Generando respuesta...*")
                time.sleep(1)
                status.update(label = "🤖 Respuesta generada", expanded=False)

            if response:
                with st.chat_message("assistant", avatar=":material/network_intelligence:"):
                    st.write_stream(stream_text(response.content))
                    with st.expander("Detalles del RAG"):
                        st.write((f"Score: {score}"))
                        st.write((doc))
                        
                    # * Metadata de la respuesta
                    st.caption(f"""
                    **Detalles Técnicos:**
                    - Modelo preciso: {response.response_metadata['model']}
                    - Tokens usados: {response.response_metadata['eval_count']}
                    - Tiempo respuesta: {response.response_metadata['total_duration'] / 1e9:.2f}s
                    """)

                    # * Guardar en historial
                    st.session_state.message.append({
                        "role": "assistant", 
                        "content": response.content
                    })

                    st.session_state.historial.append({
                        "modelo": modeloLLM,
                        "pregunta": user_input.text,
                        "respuesta": response.content,
                        "metadata": response.response_metadata
                    })

else:
    if user_input and user_input.text:
        with st.container():
            with st.chat_message("user", avatar=":material/sprint:"):
                st.write(user_input.text)

            st.session_state.message.append({"role": "user", "content": user_input.text})

            llm = ChatOllama(
                model = modeloLLM,
                temperature = st.session_state.temperature,
                top_p = st.session_state.top_p,
                top_k = st.session_state.top_k,
                num_predict = st.session_state.max_tokens
            )
            
            messages = [
                ("system", "Eres un chatbot asistente cuando el usuario lo requiera, brindando información sólida y detalles"),
                ("human", user_input.text)
            ]
            
            with st.status("*Modelo pensando...*", expanded=True) as status:
                response = llm.invoke(messages)
                st.write("*🗒️ Procesando información...*")
                time.sleep(1)
                st.write("*🔧 Puliendo detalles...*")
                time.sleep(1)
                st.write("*♟️ Jugando ajedrez...*")
                time.sleep(1)
                st.write("*🧠 Generando respuesta...*")
                time.sleep(1)
                status.update(label = "🤖 Respuesta generada", expanded=False)

            if response:
                with st.chat_message("assistant", avatar=":material/network_intelligence:"):
                    st.write_stream(stream_text(response.content))

                    # * Metadata de la respuesta
                    st.caption(f"""
                    **Detalles Técnicos:**
                    - Modelo preciso: {response.response_metadata['model']}
                    - Tokens usados: {response.response_metadata['eval_count']}
                    - Tiempo respuesta: {response.response_metadata['total_duration'] / 1e9:.2f}s
                    """)

                    # * Guardar en historial
                    st.session_state.message.append({
                        "role": "assistant", 
                        "content": response.content
                    })

                    st.session_state.historial.append({
                        "modelo": modeloLLM,
                        "pregunta": user_input.text,
                        "respuesta": response.content,
                        "metadata": response.response_metadata
                    })
    
    
if user_input and user_input["files"]:
    st.image(user_input["files"][0])
    st.write("Probando funciones de imágenes para futuro")
