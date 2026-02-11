import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Auditoría Masiva AI", page_icon="🛡️", layout="wide")

# Configuración IA
API_KEY = "AIzaSyCPBRlnta-FQgO4ovpIjX-uzWcKLhCc_mU"
genai.configure(api_key=API_KEY)

st.title("🛡️ Auditoría Masiva de Chats")
st.markdown("Sube tu reporte de chats (Excel/CSV) y deja que la IA trabaje por ti.")

# --- SECCIÓN DE CARGA ---
st.subheader("1. Carga de Datos")
uploaded_file = st.file_uploader("Elige tu archivo de Excel o CSV", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Leer el archivo dependiendo del formato
    try:
        if uploaded_file.name.endswith('.csv'):
            df_input = pd.read_csv(uploaded_file)
        else:
            df_input = pd.read_excel(uploaded_file)
        
        st.write("Vista previa de los datos cargados:")
        st.dataframe(df_input.head(5))

        col_chat = st.selectbox("Selecciona la columna que tiene el CHAT:", df_input.columns)
        col_id = st.selectbox("Selecciona la columna del ID (opcional):", ["Ninguna"] + list(df_input.columns))

        if st.button("🚀 Iniciar Auditoría Masiva"):
            resultados = []
            progreso = st.progress(0)
            total = len(df_input)
            
            model = genai.GenerativeModel('gemini-1.5-flash-latest')

            # --- CORRECCIÓN AQUÍ: usamos enumerate para asegurar que 'i' sea un número entero ---
            for i, (index, row) in enumerate(df_input.iterrows()):
                chat_texto = str(row[col_chat])
                
                # Definición del ID (Línea 42 corregida)
                if col_id == "Ninguna":
                    id_val = f"Fila {i + 1}"
                else:
                    id_val = str(row[col_id])
                
                try:
                    prompt = f"Analiza este chat de AmoLatina/FunChat. Busca pedidos de regalos, invitaciones a salir o insultos. Responde: RIESGO (Verde/Amarillo/Rojo) y un breve PORQUÉ. Chat: {chat_texto}"
                    response = model.generate_content(prompt)
                    analisis = response.text
                    
                    riesgo = "VERDE"
                    if "ROJO" in analisis.upper(): riesgo = "ROJO"
                    elif "AMARILLO" in analisis.upper(): riesgo = "AMARILLO"

                    resultados.append({
                        "ID": id_val,
                        "Riesgo": riesgo,
                        "Análisis de la IA": analisis
                    })
                except Exception as e:
                    resultados.append({"ID": id_val, "Riesgo": "ERROR", "Análisis de la IA": f"Fallo: {str(e)}"})
                
                # --- CORRECCIÓN AQUÍ: usamos 'i' que siempre es un número para el progreso (Línea 61) ---
                progreso.progress((i + 1) / total)

            # Mostrar Resultados Finales
            df_final = pd.DataFrame(resultados)
            st.divider()
            st.subheader("📊 Resultados de la Auditoría")
            st.dataframe(df_final, use_container_width=True)

            # Botón de Descarga
            csv_result = df_final.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar Reporte Finalizado", csv_result, "auditoria_final.csv", "text/csv")
            
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
