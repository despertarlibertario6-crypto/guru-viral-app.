import streamlit as st
import google.generativeai as genai
from gradio_client import Client
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="GURÚ 2.5 BLUEPRINT", page_icon="🧬", layout="wide")

# --- TU LLAVE MAESTRA ---
API_KEY_FIJA = "AIzaSyA3xMsuxhrVNVMKrWV60bXHcwQdH_mk5y0"

# --- FUNCIÓN DE VIDEO ---
def generar_video_gratis(prompt):
    try:
        client = Client("ByteDance/AnimateDiff-Lightning")
        result = client.predict(
            prompt, 
            "bad quality, low resolution, static, ugly, text, watermark", 
            "Film", 
            "1-AnimateDiff-Lightning-4step.ckpt", 
            api_name="/generate_image"
        )
        return result
    except:
        return None

# --- DATOS ---
NICHOS = {
    "💀 Terror": ["Analog Horror", "Backrooms", "True Crime", "SCP", "Leyendas"],
    "📜 Historia": ["Batallas", "Inventos", "Biografías", "Mitología", "Secretos"],
    "🤖 Tecnología": ["Futurismo", "IA", "Retro-Tech", "Hacks", "Ciberseguridad"],
    "🧠 Psicología": ["Psicología Oscura", "Lenguaje Corporal", "Manipulación", "Datos"],
    "😂 Humor": ["Brainrot", "POV", "Datos Falsos", "Comida", "Fails"]
}

ESTILOS = [
    "Cinematic Realistic 8K", "Cyberpunk Neon", "Terror VHS 90s", 
    "Glitch Digital", "Anime Studio Ghibli", "Stop-Motion Arcilla"
]

TIEMPOS = {
    "Micro-Short (15s)": "Rápido",
    "Viral (60s)": "Narrativa HERC",
    "Mini-Doc (3 min)": "Profundo"
}

# --- INTERFAZ ---
st.markdown("""<style>.stButton>button { background: linear-gradient(90deg, #FF8C00, #FFD700); color: black; font-weight: bold; }</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🧬 GURÚ 2.5")
    st.success("✅ Sistema Listo")
    
    # SELECTOR DE MODELO
    modelo = st.selectbox("Modelo:", [
        "models/gemini-2.5-flash", 
        "models/gemini-2.0-flash-exp",
        "models/nano-banana-pro-preview"
    ])
    
    st.markdown("---")
    activar_video = st.checkbox("🎥 Generar VIDEO (Lento)", value=False)

# --- MAIN ---
st.title("🏭 FÁBRICA 2.5")

c1, c2, c3 = st.columns(3)
with c1: nicho = st.selectbox("1. Nicho", list(NICHOS.keys()))
with c2: subnicho = st.selectbox("2. Subnicho", NICHOS[nicho])
with c3: duracion = st.selectbox("3. Duración", list(TIEMPOS.keys()))

estilo = st.selectbox("4. Estilo Visual", ESTILOS)
boton = st.button("🚀 GENERAR PROYECTO")

# --- LÓGICA ---
if boton:
    try:
        genai.configure(api_key=API_KEY_FIJA)
        model = genai.GenerativeModel(modelo)
        
        with st.spinner(f"🧠 {modelo} pensando..."):
            
            # HE ARREGLADO EL PROMPT AQUÍ PARA QUE NO DE ERROR DE SINTAXIS
            prompt = f"""Eres el Arquitecto Viral.
            Nicho: {nicho} ({subnicho}). Estilo: {estilo}. Duración: {duracion}.
            
            Genera estructura completa:
            [CANAL_NOMBRE]: (Nombre corto)
            [CANAL_BIO]: (Bio impacto)
            [LOGO_PROMPT]: (Logo visual simple)
            
            [TITULO_VIDEO]: (Clickbait)
            
            [ESCENA_1_GUION]: (Inicio)
            [ESCENA_1_PROMPT]: (Prompt visual en INGLES estilo {estilo})
            
            [ESCENA_2_GUION]: (Nudo)
            [ESCENA_2_PROMPT]: (Prompt visual en INGLES)
            
            [ESCENA_3_GUION]: (Final)
            [ESCENA_3_PROMPT]: (Prompt visual en INGLES)
            """
            
            respuesta = model.generate_content(prompt).text
            
            # --- PARSEO ---
            def get_val(txt, tag):
                start = txt.find(tag)
                if start == -1: return ""
                start += len(tag)
                end = txt.find("[", start)
                if end == -1: end = len(txt)
                return txt[start:end].strip().replace(":", "").strip()

            # 1. BRANDING
            st.divider()
            col_b1, col_b2 = st.columns([1, 3])
            logo_p = get_val(respuesta, "[LOGO_PROMPT]")
            
            with col_b1:
                if logo_p:
                    st.image(f"https://pollinations.ai/p/{logo_p.replace(' ', '%20')}?width=500&height=500&model=flux", caption="Logo")
            with col_b2:
                st.header(get_val(respuesta, "[CANAL_NOMBRE]"))
                st.info(get_val(respuesta, "[CANAL_BIO]"))

            # 2. VIDEO
            st.divider()
            st.subheader(f"🎬 {get_val(respuesta, '[TITULO_VIDEO]')}")
            
            c1, c2, c3 = st.columns(3)
            
            def pintar(col, num):
                guion = get_val(respuesta, f"[ESCENA_{num}_GUION]")
                prompt_vis = get_val(respuesta, f"[ESCENA_{num}_PROMPT]")
                
                if guion:
                    with col:
                        st.markdown(f"### Escena {num}")
                        st.warning(guion)
                        if prompt_vis:
                            if activar_video:
                                with st.spinner(f"🎥 Video {num}..."):
                                    vid = generar_video_gratis(prompt_vis)
                                    if vid: st.video(vid)
                                    else: st.image(f"https://pollinations.ai/p/{prompt_vis.replace(' ', '%20')}?model=flux")
                            else:
                                st.image(f"https://pollinations.ai/p/{prompt_vis.replace(' ', '%20')}?width=720&height=1280&model=flux&seed={num}")
                            
                            with st.expander("Prompt"): st.code(prompt_vis)

            pintar(c1, 1)
            pintar(c2, 2)
            pintar(c3, 3)
            
    except Exception as e:
        st.error(f"Error: {e}")
