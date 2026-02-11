import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Auditor de Chats AI", page_icon="🛡️")

st.title("🛡️ Centro de Control: Auditoría de Chats")
st.markdown("Analiza riesgos de multas y comportamiento de operadores/clientes.")

# Configurar API Key (La ponemos en un espacio seguro)
API_KEY = "AIzaSyCPBRlnta-FQgO4ovpIjX-uzWcKLhCc_mU"
genai.configure(api_key=API_KEY)

# Sidebar para reglas
with st.sidebar:
    st.header("Reglas de Monitoreo")
    st.info("Buscando: Pedido de regalos, invitaciones externas y frases de riesgo.")

# Área de entrada de datos
chat_input = st.text_area("Pega el historial del chat aquí:", height=300)

if st.button("Analizar Turno"):
    if chat_input:
        with st.spinner('La IA está auditando la conversación...'):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                prompt = f"""
                Analiza este chat de AmoLatina/FunChat.
                Reglas: No pedir regalos, no dar datos personales, no incitar a salir de la web.
                
                Entrega el resultado con este formato:
                1. NIVEL DE RIESGO: (Escribe solo: VERDE, AMARILLO o ROJO)
                2. RESUMEN: Un párrafo corto.
                3. ALERTAS OPERADOR: Lista de fallas detectadas (ej: pidió regalos).
                4. ALERTAS CLIENTE: Lista de peligros del cliente.
                
                Chat: {chat_input}
                """
                response = model.generate_content(prompt)
                res_text = response.text

                # Mostrar Resultados
                st.divider()
                st.subheader("📋 Reporte de Auditoría")
                
                # Pintar el semáforo
                if "ROJO" in res_text:
                    st.error("🚨 ALERTA ROJA: Riesgo Crítico detectado")
                elif "AMARILLO" in res_text:
                    st.warning("⚠️ RIESGO MEDIO: Revisar comportamiento")
                else:
                    st.success("✅ SEGURO: Sin infracciones detectadas")
                
                st.write(res_text)
                
            except Exception as e:
                st.error(f"Hubo un error: {e}")
    else:
        st.warning("Bro, pega un chat primero para poder trabajar.")
