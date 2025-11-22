import streamlit as st
import google.generativeai as genai
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="BLUEPRINT ENGINE", page_icon="🧬", layout="wide")

# --- ⚠️ TU LLAVE ---
API_KEY_FIJA = "AIzaSyA3xMsuxhrVNVMKrWV60bXHcwQdH_mk5y0"

# --- DATOS DEL DOCUMENTO (Base de Conocimiento) ---
NICHOS = {
    "💀 Terror / Horror": [
        "Analog Horror (VHS)", "Backrooms / Liminal", "True Crime Sobrenatural", 
        "SCP / Creepypastas", "Terror en el Mar", "Historias de la Deep Web"
    ],
    "📜 Historia": [
        "Batallas Olvidadas", "Inventos Mortales", "Biografías Oscuras", 
        "Mitología Nórdica/Griega", "Secretos del Vaticano", "Imperios Perdidos"
    ],
    "🤖 Tecnología": [
        "Futurismo / Cyberpunk", "IA fuera de control", "Gadgets Retro", 
        "Hacks de Ingeniería", "Armas del Futuro", "Realidad Simulada"
    ],
    "🧠 Psicología": [
        "Psicología Oscura", "Lenguaje Corporal", "Efecto Mandéla", 
        "Manipulación Mental", "Datos Curiosos del Cerebro"
    ],
    "😂 Humor / Viral": [
        "Brainrot Abstracto", "POV Situaciones", "Datos Falsos Divertidos", 
        "Comida Extrema", "Animales con Microfonos"
    ]
}

ESTILOS_VISUALES = [
    "Cine Noir Moderno (Alto Contraste)", "Glitch Digital & Datamoshing", 
    "Realismo Cinematográfico 8K (Sora)", "Stop-Motion de Arcilla (Inquietante)",
    "Estilo VHS Found Footage 90s", "Cyberpunk Neón", "Anime Studio Ghibli",
    "3D Render Abstracto (Satisfying)", "Ilustración Cómic Vintage"
]

TIEMPOS = {
    "Micro-Short (15s)": "1 Escena Larga (Sora) + 1 Clip Rápido (Grok)",
    "Standard Viral (60s)": "3 Escenas Largas (Sora) + 6 Clips Rápidos (Grok)",
    "Mini-Doc (3 min)": "Estructura Documental por Bloques"
}

# --- INTERFAZ ---
st.markdown("""<style>.stButton>button { background: #7B2CBF; color: white; width: 100%; font-size: 20px; }</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🧬 BLUEPRINT ENGINE")
    st.success("Sistema A.N.A.T.O.M.I.A. Cargado")
    
    st.subheader("🧠 Configuración del Motor")
    modelo = st.selectbox("Modelo IA:", ["models/nano-banana-pro-preview", "models/gemini-2.5-flash", "models/gemini-1.5-flash"])
    
    st.markdown("---")
    st.info("Este sistema usa la lógica modular del PDF: Sora (Base) + Grok (Detalle) + Meta (Estático).")

# --- PANEL DE CONTROL ---
st.title("🏭 FÁBRICA DE CANALES Y CONTENIDO")

c1, c2, c3 = st.columns(3)
with c1:
    nicho_sel = st.selectbox("1. Elige el Nicho", list(NICHOS.keys()))
with c2:
    subnicho_sel = st.selectbox("2. Elige el Subnicho", NICHOS[nicho_sel])
with c3:
    duracion_sel = st.selectbox("3. Duración del Video", list(TIEMPOS.keys()))

estilo_sel = st.selectbox("4. Estilo Visual (Atmósfera)", ESTILOS_VISUALES)

boton = st.button("🚀 GENERAR CANAL + VIDEO COMPLETO")

# --- LÓGICA MAESTRA ---
if boton:
    genai.configure(api_key=API_KEY_FIJA)
    try:
        model = genai.GenerativeModel(modelo)
        
        with st.spinner("🧠 Analizando nicho, creando branding y estructurando guion..."):
            
            # PROMPT MASIVO QUE INTEGRA TODO EL DOCUMENTO
            prompt = f"""
            Actúa como el Arquitecto de Contenido Viral (Modo Documento PDF).
            
            INPUTS:
            - Nicho: {nicho_sel} ({subnicho_sel})
            - Estilo: {estilo_sel}
            - Formato: {duracion_sel}
            
            TAREA 1: BRANDING DEL CANAL
            Genera un nombre viral, una bio corta y un prompt para el LOGO.
            
            TAREA 2: ESTRUCTURA DEL VIDEO (Modular)
            Usa la estructura: {TIEMPOS[duracion_sel]}.
            Aplica A.N.A.T.O.M.I.A (Gancho, Necesidad, Revelación).
            
            FORMATO DE SALIDA ESTRICTO (No cambies las etiquetas):
            
            [CANAL_NOMBRE]: ...
            [CANAL_BIO]: ...
            [LOGO_PROMPT]: ...
            
            [TITULO_VIDEO]: ...
            
            [ESCENA_1_TIPO]: (Ej: Sora 2 - 15s)
            [ESCENA_1_GUION]: ...
            [ESCENA_1_PROMPT]: ...
            
            [ESCENA_2_TIPO]: (Ej: Grok - 5s)
            [ESCENA_2_GUION]: ...
            [ESCENA_2_PROMPT]: ...
            
            [ESCENA_3_TIPO]: (Ej: Meta Estático - 5s)
            [ESCENA_3_GUION]: ...
            [ESCENA_3_PROMPT]: ...
            """
            
            respuesta = model.generate_content(prompt).text
            
        # --- PARSEO Y VISUALIZACIÓN ---
        
        # Función auxiliar para extraer texto
        def get_val(text, tag):
            start = text.find(tag)
            if start == -1: return ""
            start += len(tag)
            end = text.find("[", start)
            if end == -1: end = len(text)
            return text[start:end].strip().replace(":", "").strip()

        # 1. BRANDING DEL CANAL
        st.divider()
        st.subheader("📢 TU NUEVO CANAL")
        col_brand_1, col_brand_2 = st.columns([1, 3])
        
        nombre_canal = get_val(respuesta, "[CANAL_NOMBRE]")
        bio_canal = get_val(respuesta, "[CANAL_BIO]")
        logo_prompt = get_val(respuesta, "[LOGO_PROMPT]")
        
        with col_brand_1:
            # Generar Logo
            if logo_prompt:
                url_logo = f"https://pollinations.ai/p/{logo_prompt.replace(' ', '%20')}?width=500&height=500&model=flux"
                st.image(url_logo, caption="Logo Generado")
        
        with col_brand_2:
            st.markdown(f"## 📺 {nombre_canal}")
            st.info(f"📝 **Bio:** {bio_canal}")
            st.success(f"🎨 **Estilo Visual:** {estilo_sel}")

        # 2. EL VIDEO
        st.divider()
        st.subheader(f"🎬 GUION Y STORYBOARD: {get_val(respuesta, '[TITULO_VIDEO]')}")
        
        c1, c2, c3 = st.columns(3)
        
        # Función para pintar escena
        def pintar_escena(col, num):
            tipo = get_val(respuesta, f"[ESCENA_{num}_TIPO]")
            guion = get_val(respuesta, f"[ESCENA_{num}_GUION]")
            prompt = get_val(respuesta, f"[ESCENA_{num}_PROMPT]")
            
            if guion or prompt:
                with col:
                    st.markdown(f"### 🎞️ Escena {num}")
                    st.caption(f"🔧 Módulo: {tipo}")
                    st.warning(f"🗣️ {guion}")
                    
                    if prompt:
                        url_img = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=720&height=1280&model=flux&seed={num}"
                        st.image(url_img, use_column_width=True)
                        with st.expander("Ver Prompt Técnico"):
                            st.code(prompt)

        pintar_escena(c1, 1)
        pintar_escena(c2, 2)
        pintar_escena(c3, 3)
        
    except Exception as e:
        st.error(f"Error: {e}")
        st.write("Prueba cambiando el modelo en la barra lateral.")
