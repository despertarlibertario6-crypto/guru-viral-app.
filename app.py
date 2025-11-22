import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="GURÚ VIRAL ONLINE", page_icon="🚀", layout="wide")

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/11698/11698467.png", width=100)
    st.title("CONFIGURACIÓN")
    
    # TRUCO: Busca la llave en los "Secretos" de la nube, si no está, la pide.
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ Llave Maestra Detectada")
    else:
        api_key = st.text_input("🔑 Pega tu API Key:", type="password")

# --- INTERFAZ ---
st.title("🚀 GURÚ VIRAL: AUTOMATIZACIÓN TOTAL")
st.markdown("Generador de Guiones y Storyboards 4K (Motor Gemini + Flux).")

tema = st.text_input("¿De qué trata el video?", placeholder="Ej: Secretos de la Antártida")
estilo = st.selectbox("Estilo Visual:", ["Cinematic Realistic 8K", "Cyberpunk Neon", "Terror Analogico VHS", "Anime Studio Ghibli"])
boton = st.button("⚡ GENERAR PACK DE VIDEO")

# --- MOTOR LÓGICO ---
if boton:
    if not api_key or not tema:
        st.warning("⚠️ Necesito la API Key y un Tema.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash') # Usamos Flash porque es muy rápido
            
            with st.spinner("🧠 El Cerebro está diseñando la estrategia..."):
                # PROMPT MAESTRO
                prompt = f"""
                Eres el Productor Ejecutivo de un canal viral. Tema: "{tema}".
                Estilo Visual: {estilo}.
                
                Genera 3 ESCENAS CLAVE para un video corto.
                Para cada escena necesito:
                1. GUION (Lo que dice el narrador).
                2. PROMPT (Descripción visual en Inglés para generar la imagen).
                
                Formato de salida OBLIGATORIO:
                ESCENA_1_GUION: ...
                ESCENA_1_PROMPT: ...
                ESCENA_2_GUION: ...
                ESCENA_2_PROMPT: ...
                ESCENA_3_GUION: ...
                ESCENA_3_PROMPT: ...
                """
                respuesta = model.generate_content(prompt).text

            # --- VISUALIZADOR ---
            st.divider()
            col1, col2, col3 = st.columns(3)

            # Función para pintar
            def pintar_escena(columna, num_escena, respuesta_texto):
                with columna:
                    # Buscar texto en la respuesta de Gemini
                    key_g = f"ESCENA_{num_escena}_GUION:"
                    key_p = f"ESCENA_{num_escena}_PROMPT:"
                    
                    # Extracción simple de texto
                    try:
                        start_g = respuesta_texto.find(key_g) + len(key_g)
                        end_g = respuesta_texto.find(key_p)
                        guion_txt = respuesta_texto[start_g:end_g].strip()
                        
                        # El prompt va hasta la siguiente escena o el final
                        start_p = respuesta_texto.find(key_p) + len(key_p)
                        end_p = respuesta_texto.find(f"ESCENA_{num_escena+1}_GUION:")
                        if end_p == -1: end_p = len(respuesta_texto)
                        
                        prompt_txt = respuesta_texto[start_p:end_p].strip()
                        prompt_txt = prompt_txt.replace("\n", " ")
                        
                        # Mostrar Guion
                        st.markdown(f"### 🎬 Escena {num_escena}")
                        st.info(guion_txt)
                        
                        # Generar Imagen (Flux)
                        url_limpia = f"https://pollinations.ai/p/{prompt_txt.replace(' ', '%20')}?width=720&height=1280&model=flux&seed={num_escena}"
                        st.image(url_limpia, use_column_width=True)
                        
                    except:
                        st.error("Error leyendo la escena. Intenta de nuevo.")

            # Pintar las 3 columnas
            pintar_escena(col1, 1, respuesta)
            pintar_escena(col2, 2, respuesta)
            pintar_escena(col3, 3, respuesta)
            
            st.success("✅ ¡Pack Completo! Guarda las imágenes (Click derecho) y graba el audio.")

        except Exception as e:
            st.error(f"Error de conexión: {e}")