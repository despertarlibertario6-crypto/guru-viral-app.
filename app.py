import streamlit as st
import google.generativeai as genai

st.title("🕵️‍♂️ DETECTIVE DE MODELOS")

# 1. Verificar Llave
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    st.success(f"✅ Llave detectada (Empieza por: {api_key[:4]}...)")
    
    # 2. Configurar
    genai.configure(api_key=api_key)
    
    st.write("⏳ Preguntando a Google qué modelos están habilitados para ti...")
    
    try:
        # 3. Listar Modelos
        modelos = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                modelos.append(m.name)
        
        if modelos:
            st.subheader("✅ MODELOS DISPONIBLES (Copia uno de estos):")
            for modelo in modelos:
                st.code(modelo) # Ej: models/gemini-1.5-flash
        else:
            st.warning("⚠️ No se encontraron modelos. Tu API Key podría tener restricciones de región.")
            
    except Exception as e:
        st.error(f"❌ Error crítico de conexión: {e}")
        st.info("Intenta crear una API Key nueva en Google AI Studio.")

else:
    st.error("⛔ No has puesto la API Key en los 'Secrets' de Streamlit.")
