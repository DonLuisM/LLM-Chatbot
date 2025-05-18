<!-- Organización del Repositorio GitHub: El repositorio debe ser público y contener:
El código fuente en una carpeta src, incluyendo la lógica del chatbot y del RAG.
Los PDFs utilizados en la carpeta data.
Un README.md detallado con:
Instrucciones claras para replicar el proyecto.
Ejemplos de consultas de prueba y las respuestas esperadas (p. ej., "¿Cuál es el tema principal del documento?" junto a una respuesta contextualizada).
.gitignore configurado correctamente. -->

# :brain: _CORTEXiRAG-BOT_
Este proyecto  consiste en un chatbot interactivo con interfaz en Streamlit capaz de interactuar con el usuario de manera casual o haciendo uso del beneficio de la técnica RAG para proporcionar respuestas informadas basadas en el contenido de archivos PDF cargados por el usuario. La funcionalidad del modelo se logra gracias a librerías como LangChain, LangSmith, PyPDFLoader, RecursiveCharacterTextSplitter y de embeddings.

### :dart: Características
- Consulta inteligente de PDFs.
- Respuestas contextualizadas con Langchain, Ollama y técnicas RAG.
- Procesamiento interno de PDFs y generación de embeddings.
- Monitoreo y Trazabilidad con LangSmith del chatbot.
- Interfaz de usuario intuitiva con Streamlit.
- Configuración de parámetros para el modelo (temperature, top_p, etc).
- Si cuentas con modelos en Ollama, los extrae y te permite elegir con un selectbox, el modelo que gustes.

### :rocket: Tecnologías usadas
- Python
- uv
- Ollama
- Streamlit
- LangChain

### :framed_picture: Visualización de la aplicación

| Vista Web | Vista Móvil |
|-----------|-------------|
| ![webapp](./data/) | ![mobile](./data/) |

| Vista Streamlit |
|------------------|
| ![st](./data/) |
 
---
## :hammer_and_wrench: Configuración

### 1. Descargar Ollama y uv
- Ollama - [Download](https://ollama.com/)
- uv - [Terminal](https://docs.astral.sh/uv/#__tabbed_1_1)
> [!IMPORTANT]
> Para correr satisfactoriamente la aplicación y configuración debes contar con UV Python y Ollama (LLMs Open Source).

### 2. Instalar modelos de Ollama:
```bash
# Validar modelos de Ollama descargados
ollama list

# Descargar modelos qwen3
ollama run qwen3:latest
```

### 3. Clona el repositorio e instalar dependencias
```bash
git clone https://github.com/DonLuisM/languagesTranslate_Ollama.git
cd languagesTranslate_Ollama

uv sync
```

### 4. Ejecutar el streamlit para comparar respuestas
```bash
uv run streamlit run .\streamlit\app_st_cont.py   
```
---

### :: Agradecimientos (Recursos de Apoyo)
Para lograr el debido desarrollo de la aplicación.

### :scroll: Licencia
Licencia MIT – consulta el archivo [LICENSE](./LICENSE) para más detalles.

### :handshake: Contribuciones
Si deseas contribuir a este proyecto, siéntete libre de hacer un fork del repositorio y enviar un pull request. ¡Todas las contribuciones son bienvenidas!

### :busts_in_silhouette: Autor:
- [@DonLuisM](https://github.com/DonLuisM)
