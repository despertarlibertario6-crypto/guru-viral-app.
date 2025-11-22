import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="GURÚ 2.5 (FUTURO)", page_icon="🍌", layout="wide")

# --- ESTILO ---
st.markdown("""
<style>
    .stButton>button { background: linear-gradient(45deg, #FFD700, #FF8C00); color: black; font-weight: bold; border: none; }
    h1 { color: #FF8C00; }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("⚙️ CONFIGURACIÓN")
    
    # 1. API KEY
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ Llave Maestra (Secrets)")
    else:
        api_key = st.text_input("🔑 Pega tu API Key:", type="password")

    st.markdown("---")
    
    # 2. SELECTOR DE MODELO (Basado en tu lista)
    st.subheader("🧠 Elige el Cerebro")
    modelo_elegido = st.selectbox(
        "Modelo:", 
        [
            "models/gemini-2.5-flash", 
            "models/nano-banana-pro-preview", 
            "models/gemini-2.5-pro",
            "models/gemini-3-pro-preview"
        ]
    )
    st.info(f"Usando motor: {modelo_elegido}")

# --- INTERFAZ PRINCIPAL ---
st.title("🍌 GURÚ VIRAL: NEXT GEN")
st.markdown(f"Generador impulsado por **{modelo_elegido.replace('models/', '').upper()}**.")

col1, col2 = st.columns([3, 1])
with col1:
    tema = st.text_input("¿De qué trata el video?", placeholder="Ej: La paradoja del viaje en el tiempo")
with col2:
    st.write("")
    st.write("")
    boton = st.button("🚀 GENERAR PACK 2.5")

# --- LÓGICA ---
if boton:
    if not api_key or not tema:
        st.error("⚠️ Falta la API Key o el Tema.")
    else:
        try:
            genai.configure(api_key=api_key)
            # Aquí usamos el modelo exacto de tu lista
            model = genai.GenerativeModel(modelo_elegido)
            
            with st.spinner(f"🧠 {modelo_elegido} está pensando estrategias virales..."):
                
                # PROMPT MAESTRO
                prompt = f"""
                Eres el CEREBRO DE VIRALIDAD (Versión 2.5). Tema: "{tema}".
                
                Genera 3 ESCENAS CLAVE para un Short Viral.
                Formato estricto:
                
                ESCENA_1_GUION: [Texto narrador impactante]
                ESCENA_1_PROMPT: [Prompt visual detallado en inglés, estilo cinematográfico 8k]
                
                ESCENA_2_GUION: [Texto narrador desarrollo]
                ESCENA_2_PROMPT: [Prompt visual detallado en inglés]
                
                ESCENA_3_GUION: [Texto narrador cierre/hook]
                ESCENA_3_PROMPT: [Prompt visual detallado en inglés]
                """
                
                respuesta = model.generate_content(prompt).text

            # --- RENDERIZADO DE RESULTADOS ---
            st.divider()
            
            # Función para pintar
            def pintar(col, num, texto_raw):
                with col:
                    try:
                        # Buscar textos
                        k_guion = f"ESCENA_{num}_GUION:"
                        k_prompt = f"ESCENA_{num}_PROMPT:"
                        
                        start_g = texto_raw.find(k_guion) + len(k_guion)
                        end_g = texto_raw.find(k_prompt)
                        
                        # Truco para encontrar el final del prompt
                        next_k = f"ESCENA_{num+1}_GUION:"
                        start_p = texto_raw.find(k_prompt) + len(k_prompt)
                        end_p = texto_raw.find(next_k) if num < 3 else len(texto_raw)
                        
                        guion = texto_raw[start_g:end_g].strip()
                        prompt = texto_raw[start_p:end_p].strip()
                        
                        # Mostrar
                        st.markdown(f"### 🎬 Escena {num}")
                        st.info(guion)
                        
                        # Generar Imagen (Flux)
                        # Usamos el prompt generado por el modelo 2.5 para pintar en Flux
                        url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=720&height=1280&model=flux&seed={num}"
                        st.image(url, use_column_width=True)
                        
                    except:
                        st.warning(f"Procesando escena {num}...")

            c1, c2, c3 = st.columns(3)
            pintar(c1, 1, respuesta)
            pintar(c2, 2, respuesta)
            pintar(c3, 3, respuesta)
            
            st.success("✅ ¡Generación Exitosa con el Nuevo Motor!")

        except Exception as e:
            st.error(f"❌ Error con el modelo {modelo_elegido}: {e}")
            st.write("Prueba seleccionando otro modelo en la barra lateral (ej: gemini-2.5-flash).")
