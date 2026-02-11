import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Auditoría Pro - Chats", page_icon="🛡️", layout="wide")

# Estilo personalizado
st.markdown("## 🛡️ Centro de Control: Auditoría de Chats")

# --- CONFIGURACIÓN DE IA ---
API_KEY = "AIzaSyCPBRlnta-FQgO4ovpIjX-uzWcKLhCc_mU"
genai.configure(api_key=API_KEY)

# --- INICIALIZAR HISTORIAL ---
if 'historial_auditoria' not in st.session_state:
    st.session_state.historial_auditoria = []

# --- FORMULARIO DE ENTRADA ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        id_perfil = st.text_input("🆔 ID del Perfil (Operador)", placeholder="Ej: P-1025")
        nombre_perfil = st.text_input("👤 Nombre del Perfil", placeholder="Ej: Rebecca")
    with col2:
        id_cliente = st.text_input("🆔 ID del Cliente", placeholder="Ej: C-9988")
        nombre_cliente = st.text_input("👤 Nombre del Cliente", placeholder="Ej: John Doe")

    chat_input = st.text_area("💬 Historial del Chat:", height=250)

# --- LÓGICA DE ANÁLISIS ---
if st.button("🚀 Analizar y Guardar en Reporte"):
    if chat_input and id_perfil and id_cliente:
        with st.spinner('Analizando comportamiento y riesgos...'):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                prompt = f"""
                Analiza este chat de AmoLatina/FunChat.
                Reglas: No pedir regalos, no dar datos personales, no incitar a salir de la web.
                
                Chat: {chat_input}
                
                ENTREGA EL RESULTADO EXACTAMENTE ASÍ:
                RIESGO: [Escribe solo VERDE, AMARILLO o ROJO]
                RESUMEN: [Un párrafo corto del historial]
                HALLAZGOS: [Lista de fallas o alertas]
                """
                
                response = model.generate_content(prompt)
                analisis = response.text
                
                # Extraer el nivel de riesgo para el color
                nivel_riesgo = "VERDE"
                if "ROJO" in analisis.upper(): nivel_riesgo = "ROJO"
                elif "AMARILLO" in analisis.upper(): nivel_riesgo = "AMARILLO"

                # Guardar en el historial del supervisor
                nuevo_registro = {
                    "Fecha/Hora": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "ID Perfil": id_perfil,
                    "Perfil": nombre_perfil,
                    "ID Cliente": id_cliente,
                    "Cliente": nombre_cliente,
                    "Riesgo": nivel_riesgo,
                    "Análisis Completo": analisis
                }
                st.session_state.historial_auditoria.insert(0, nuevo_registro)
                st.success("✅ Análisis completado y añadido al reporte.")
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Bro, rellena los IDs y el chat para poder auditar.")

# --- SECCIÓN DE REPORTES (PUNTO 1 Y 2) ---
st.divider()
st.subheader("📊 Reporte Consolidado (Historial del Turno)")

if st.session_state.historial_auditoria:
    df = pd.DataFrame(st.session_state.historial_auditoria)
    
    # Mostrar tabla resumen
    st.dataframe(df[["Fecha/Hora", "ID Perfil", "Perfil", "ID Cliente", "Cliente", "Riesgo"]], use_container_width=True)

    # Botón para descargar reporte (Punto 2)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte Completo (Excel/CSV)",
        data=csv,
        file_name=f"reporte_auditoria_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime='text/csv',
    )
    
    # Detalle expandible
    with st.expander("Ver detalle de análisis por cada caso"):
        for reg in st.session_state.historial_auditoria:
            st.write(f"**Caso: {reg['Perfil']} vs {reg['Cliente']}**")
            st.code(reg['Análisis Completo'])
            st.divider()
else:
    st.info("Aún no hay análisis en este turno.")
