import streamlit as st
import google.generativeai as genai
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BLUEPRINT ENGINE", page_icon="🧬", layout="wide")

# --- TU LLAVE (Ya integrada) ---
API_KEY_FIJA = "AIzaSyA3xMsuxhrVNVMKrWV60bXHcwQdH_mk5y0"

# --- BASE DE DATOS DEL DOCUMENTO ---
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

# --- INTERFAZ ---
st.markdown("""<style>.stButton>button { background: #7B2CBF; color: white; width: 100%; font-weight: bold; }</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🧬 BLUEPRINT ENGINE")
    st.success("✅ Sistema Estable Cargado")
    
    st.subheader("🧠 Motor IA")
    # HE CAMBIADO ESTO: Solo dejamos el modelo que funciona GRATIS SIEMPRE
    modelo = st.selectbox("Modelo:", ["models/gemini-1.5-flash", "models/gemini-1.5-pro"])
    st.info("Usando motor estable (Sin límites 429).")

st.title("🏭 FÁBRICA DE CANALES VIRALES")

c1, c2, c3 = st.columns(3)
with c1: nicho_sel = st.selectbox("1. Nicho", list(NICHOS.keys()))
with c2: subnicho_sel = st.selectbox("2. Subnicho", NICHOS[nicho_sel])
with c3: duracion_sel = st.selectbox("3. Duración", list(TIEMPOS.keys()))

estilo_sel = st.selectbox("4. Estilo Visual", ESTILOS)
boton = st.button("🚀 GENERAR ESTRATEGIA AHORA")

# --- LÓGICA ---
if boton:
    try:
        genai.configure(api_key=API_KEY_FIJA)
        model = genai.GenerativeModel(modelo) # Usamos el modelo seleccionado
        
        with st.spinner("🧠 Consultando al Blueprint Maestro..."):
            
            prompt = f"""
            Eres el Arquitecto Viral (Basado en el documento PDF).
            Nicho: {nicho_sel} ({subnicho_sel}). Estilo: {estilo_sel}. Duración: {duracion_sel}.
            
            Genera la estructura completa:
            
            [CANAL_NOMBRE]: (Nombre corto y pegadizo)
            [CANAL_BIO]: (Frase de alto impacto)
            [LOGO_PROMPT]: (Descripción visual para el logo)
            
            [TITULO_VIDEO]: (Clickbait ético)
            
            [ESCENA_1_GUION]: (Inicio impactante)
            [ESCENA_1_PROMPT]: (Descripción visual detallada en Inglés, estilo {estilo_sel})
            
            [ESCENA_2_GUION]: (Desarrollo/Conflicto)
            [ESCENA_2_PROMPT]: (Descripción visual detallada en Inglés)
            
            [ESCENA_3_GUION]: (Cierre/Call to Action)
            [ESCENA_3_PROMPT]: (Descripción visual detallada en Inglés)
            """
            
            respuesta = model.generate_content(prompt).text
            
            # --- VISUALIZADOR ---
            def get_val(text, tag):
                start = text.find(tag)
                if start == -1: return ""
                start += len(tag)
                end = text.find("[", start)
                if end == -1: end = len(text)
                return text[start:end].strip().replace(":", "").strip()

            # BRANDING
            st.divider()
            col_b1, col_b2 = st.columns([1, 3])
            logo_p = get_val(respuesta, "[LOGO_PROMPT]")
            
            with col_b1:
                if logo_p:
                    # Logo cuadrado
                    st.image(f"https://pollinations.ai/p/{logo_p.replace(' ', '%20')}?width=500&height=500&model=flux", caption="Logo Generado")
            with col_b2:
                st.header(get_val(respuesta, "[CANAL_NOMBRE]"))
                st.info(get_val(respuesta, "[CANAL_BIO]"))

            # VIDEO
            st.divider()
            st.subheader(f"🎬 {get_val(respuesta, '[TITULO_VIDEO]')}")
            
            c1, c2, c3 = st.columns(3)
            
            def pintar(col, num):
                guion = get_val(respuesta, f"[ESCENA_{num}_GUION]")
                prompt = get_val(respuesta, f"[ESCENA_{num}_PROMPT]")
                if guion:
                    with col:
                        st.markdown(f"### Escena {num}")
                        st.warning(guion)
                        if prompt:
                            # Imagen vertical
                            url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=720&height=1280&model=flux&seed={num}"
                            st.image(url, use_column_width=True)
                            with st.expander("Ver Prompt"): st.code(prompt)

            pintar(c1, 1)
            pintar(c2, 2)
            pintar(c3, 3)
            
    except Exception as e:
        st.error(f"Error: {e}")
        st.write("Si ves error 429, espera 1 minuto y vuelve a probar.")
