import streamlit as st
import google.generativeai as genai
from gradio_client import Client
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="GURÚ 2.5 BLUEPRINT", page_icon="🧬", layout="wide")

# --- TU LLAVE MAESTRA ---
API_KEY_FIJA = "AIzaSyA3xMsuxhrVNVMKrWV60bXHcwQdH_mk5y0"

# --- FUNCIÓN DE VIDEO (ByteDance AnimateDiff) ---
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

# --- BASE DE DATOS (NICHOS PDF) ---
NICHOS = {
    "💀 Terror / Horror": ["Analog Horror", "Backrooms", "True Crime Sobrenatural", "SCP", "Leyendas Urbanas"],
    "📜 Historia": ["Batallas Olvidadas", "Inventos Mortales", "Biografías Oscuras", "Mitología", "Secretos Reales"],
    "🤖 Tecnología": ["Futurismo", "IA fuera de control", "Gadgets Retro", "Hacks", "Ciberseguridad"],
    "🧠 Psicología": ["Psicología Oscura", "Lenguaje Corporal", "Manipulación", "Datos Curiosos"],
    "😂 Humor": ["Brainrot", "POV", "Datos Falsos", "Comida Extrema", "Fails"]
}

ESTILOS = [
    "Cinematic Realistic 8K (Sora Style)", "Cyberpunk Neón", 
    "Terror Analogico VHS 90s", "Glitch Digital", "Anime Studio Ghibli",
    "Stop-Motion Arcilla", "Fotografía Macro Detallada"
]

TIEMPOS = {
    "Micro-Short (15s)": "Ritmo Rápido (Grok)",
    "Viral Standard (60s)": "Narrativa HERC (Sora + Grok)",
    "Mini-Doc (3 min)": "Storytelling Profundo"
}

# --- ESTILOS CSS ---
st.markdown("""<style>.stButton>button { background: linear-gradient(90deg, #FF8C00, #FFD700); color: black; width: 100%; font-weight: bold; font-size: 18px; }</style>""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("🧬 GURÚ 2.5")
    st.success("✅ Modelos Next-Gen Cargados")
    
    st.subheader("🧠 Motor IA")
    # AQUÍ ESTÁN TUS MODELOS QUE FUNCIONAN
    modelo = st.selectbox("Modelo:", [
        "models/gemini-2.5-flash", 
        "models/gemini-2.0-flash-exp",
        "models/nano-banana-pro-preview"
    ])
    st.info(f"Motor: {modelo}")
    
    st.markdown("---")
    st.subheader("🎥 Configuración Visual")
    # INTERRUPTOR DE VIDEO
    activar_video = st.checkbox("Generar VIDEO con movimiento", value=False, help="Actívalo para generar MP4 (Tarda +30s). Desactívalo para imágenes instantáneas.")
    if activar_video:
        st.warning("⚠️ Modo Video: Más lento pero con movimiento.")
    else:
        st.info("⚡ Modo Foto: Instantáneo.")

# --- INTERFAZ PRINCIPAL ---
st.title("🏭 FÁBRICA 2.5: ESTRATEGIA + VIDEO")

c1, c2, c3 = st.columns(3)
with c1: nicho_sel = st.selectbox("1. Nicho", list(NICHOS.keys()))
with c2: subnicho_sel = st.selectbox("2. Subnicho", NICHOS[nicho_sel])
with c3: duracion_sel = st.selectbox("3. Duración", list(TIEMPOS.keys()))

estilo_sel = st.selectbox("4. Estilo Visual", ESTILOS)
boton = st.button("🚀 GENERAR ESTRATEGIA COMPLETA")

# --- LÓGICA ---
if boton:
    try:
        genai.configure(api_key=API_KEY_FIJA)
        model = genai.GenerativeModel(modelo)
        
        with st.spinner(f"🧠 {modelo} consultando Blueprint Maestro..."):
            
            prompt = f"""
            Eres el Arquitecto Viral (Basado en el documento PDF).
            Nicho: {nicho_sel} ({subnicho_sel}). Estilo: {estilo_sel}. Duración: {duracion_sel}.
            
            Genera la estructura completa:
            
            [CANAL_NOMBRE]: (Nombre corto y pegadizo)
            [CANAL_BIO]: (Frase de alto impacto)
            [LOGO_PROMPT]: (Descripción visual para el logo, simple y vectorial)
            
            [TITULO_VIDEO]: (Clickbait ético)
            
            [ESCENA_1_GUION]: (Inicio impactante)
            [ESCENA_1_PROMPT]: (Descripción visual detallada en Inglés, corta y directa, estilo {estilo_sel})
            
            [ESCENA_2_GUION]: (Desarroll
