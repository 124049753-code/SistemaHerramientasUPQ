import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Herramientas UPQ",
    page_icon="🔧",
    layout="wide"
)

# Título
st.title("🔧 Sistema de Gestión de Herramientas")
st.subheader("Universidad Politécnica de Querétaro")

st.markdown("---")

# Cargar inventario
try:
    inventario = pd.read_excel("excel/inventario.xlsx")

    total_herramientas = len(inventario)

    if "CANTIDAD" in inventario.columns:
        disponibles = inventario["CANTIDAD"].sum()
    else:
        disponibles = 0

except Exception as e:
    st.error(f"Error al cargar el inventario: {e}")
    inventario = pd.DataFrame()
    total_herramientas = 0
    disponibles = 0

# Dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Herramientas registradas", total_herramientas)

with col2:
    st.metric("Piezas disponibles", disponibles)

with col3:
    st.metric("Préstamos activos", 0)

with col4:
    st.metric("Herramientas dañadas", 0)

st.markdown("---")

# Mostrar inventario
st.header("📦 Inventario")

if not inventario.empty:
    st.dataframe(inventario, use_container_width=True)
else:
    st.warning("No se encontró información del inventario.")