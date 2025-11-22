import streamlit as st
import google.generativeai as genai
from gradio_client import Client
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="GURÚ VIDEO MAKER", page_icon="🎥", layout="wide")
st.markdown("""<style>.stButton>button { background: #E50914; color: white; font-weight: bold; }</style>""", unsafe_allow_html=True)

# --- LLAVE MAESTRA INTEGRADA ---
API_KEY_FIJA = "AIzaSyA3xMsuxhrVNVMKrWV60bXHcwQdH_mk5y0"

# --- FUNCIÓN DE VIDEO (LA MAGIA) ---
def generar_video_gratis(prompt_video):
    """Conecta con AnimateDiff Lightning en HuggingFace (Gratis)"""
    try:
        # Usamos el cliente de Gradio para conectar con el Space gratuito
        client = Client("ByteDance/AnimateDiff-Lightning")
        
        # Parámetros mágicos para que funcione rápido
        result = client.predict(
            prompt_video, # Tu prompt
            "bad quality, low resolution, static, ugly", # Negative prompt
            "Film", # Estilo (Base)
            "1-AnimateDiff-Lightning-4step.ckpt", # Modelo rápido
            api_name="/generate_image"
        )
        return result # Devuelve la ruta del video MP4
    except Exception as e:
        return None

# --- INTERFAZ ---
with st.sidebar:
    st.title("🎥 VIDEO MAKER")
    st.success("✅ Motor Gemini: Activo")
    st.info("✅ Motor Video: AnimateDiff (Gratis)")
    st.warning("⚠️ Nota: El video tarda unos 20-30 segs por escena. Ten paciencia.")

st.title("🎥 GURÚ: TEXTO A VIDEO (GRATIS)")
st.markdown("Genera guiones virales y **VIDEOS CON MOVIMIENTO REAL** (2-4s) automáticamente.")

# --- ENTRADAS ---
c1, c2 = st.columns([3, 1])
with c1:
    tema = st.text_input("¿De qué trata el video?", placeholder="Ej: Un astronauta caminando en Marte")
with c2:
    st.write("")
    st.write("")
    boton = st.button("🚀 GENERAR VIDEO PACK")

# --- LÓGICA ---
if boton:
    if not tema:
        st.error("Escribe un tema.")
    else:
        try:
            # 1. CEREBRO (GEMINI)
            genai.configure(api_key=API_KEY_FIJA)
            # Usamos el modelo Flash porque es el más fiable ahora mismo
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("🧠 Escribiendo guion y diseñando prompts de video..."):
                prompt = f"""
                Eres un Director de Video AI. Tema: "{tema}".
                Genera 2 ESCENAS CLAVE.
                
                Importante: Los PROMPTS DE VIDEO deben ser en Inglés, cortos, directos y describir movimiento.
                Ejemplo: "A cybernetic cat running in neon rain, 4k, highly detailed".
                
                Formato de salida:
                ESCENA_1_GUION: ...
                ESCENA_1_PROMPT: ...
                ESCENA_2_GUION: ...
                ESCENA_2_PROMPT: ...
                """
                respuesta = model.generate_content(prompt).text

            # --- RENDERIZADO ---
            st.divider()
            
            # Función para procesar cada escena
            def procesar_escena(col, num):
                with col:
                    try:
                        # Extraer textos
                        k_g = f"ESCENA_{num}_GUION:"
                        k_p = f"ESCENA_{num}_PROMPT:"
                        next_k = f"ESCENA_{num+1}_GUION:"
                        
                        start_g = respuesta.find(k_g) + len(k_g)
                        end_g = respuesta.find(k_p)
                        guion = respuesta[start_g:end_g].strip()
                        
                        start_p = respuesta.find(k_p) + len(k_p)
                        end_p = respuesta.find(next_k) if num < 2 else len(respuesta)
                        prompt_video = respuesta[start_p:end_p].strip()
                        
                        # Mostrar Texto
                        st.markdown(f"### 🎬 Escena {num}")
                        st.info(f"🎙️ {guion}")
                        st.caption(f"Prompt: {prompt_video}")
                        
                        # GENERAR VIDEO
                        with st.spinner(f"🎥 Renderizando video {num} (Espera...)..."):
                            video_path = generar_video_gratis(prompt_video)
                            
                            if video_path:
                                st.video(video_path)
                                st.success("¡Movimiento generado!")
                            else:
                                st.error("El servidor de video está saturado. Prueba de nuevo.")
                                # Fallback a imagen si falla el video
                                url_img = f"https://pollinations.ai/p/{prompt_video.replace(' ', '%20')}?model=flux"
                                st.image(url_img, caption="Imagen estática (Fallback)")
                                
                    except Exception as e:
                        st.error(f"Error en escena {num}: {e}")

            col1, col2 = st.columns(2)
            
            # Lanzamos las 2 escenas
            procesar_escena(col1, 1)
            procesar_escena(col2, 2)
            
        except Exception as e:
            st.error(f"Error general: {e}")
