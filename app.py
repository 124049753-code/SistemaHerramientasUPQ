import streamlit as st
import pandas as pd

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Sistema de Herramientas UPQ",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ENCABEZADO
# ==========================================

st.title("🔧 Sistema de Gestión de Herramientas")
st.subheader("Universidad Politécnica de Querétaro")

# RUTA CORREGIDA
ruta_excel = "excel/inventario.xlsx"

# ==========================================
# MENÚ LATERAL
# ==========================================

menu = st.sidebar.radio(
    "📋 Menú",
    [
        "📦 Inventario",
        "📝 Solicitar herramienta",
        "📋 Préstamos activos",
        "🔄 Devoluciones",
        "🛠 Herramientas dañadas",
        "📈 Reportes"
    ]
)

try:

    archivo = pd.ExcelFile(ruta_excel)

    almacen = st.sidebar.selectbox(
        "🏢 Seleccione un almacén",
        archivo.sheet_names
    )

    inventario = pd.read_excel(
        ruta_excel,
        sheet_name=almacen,
        header=None
    )

    # Limpieza del inventario
    inventario = inventario.replace("None", "")
    inventario = inventario.fillna("")
    inventario = inventario.dropna(axis=1, how="all")
    inventario = inventario.dropna(how="all")
    inventario = inventario.reset_index(drop=True)

    # Calcular piezas disponibles
    cantidad_total = 0

    for columna in inventario.columns:
        suma = pd.to_numeric(
            inventario[columna],
            errors="coerce"
        ).fillna(0).sum()

        if suma > cantidad_total:
            cantidad_total = suma

    total_herramientas = len(inventario)

    # Dashboard
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📦 Herramientas", total_herramientas)

    with col2:
        st.metric("🔢 Piezas disponibles", int(cantidad_total))

    with col3:
        st.metric("🏢 Almacén", almacen)

    with col4:
        st.metric("📑 Almacenes", len(archivo.sheet_names))

    st.divider()

    # ==========================================
    # INVENTARIO
    # ==========================================

    if menu == "📦 Inventario":

        st.header(f"📦 Inventario - {almacen}")

        busqueda = st.text_input(
            "🔍 Buscar herramienta"
        )

        inventario_filtrado = inventario

        if busqueda:
            inventario_filtrado = inventario[
                inventario.astype(str)
                .apply(
                    lambda fila:
                    fila.str.contains(
                        busqueda,
                        case=False
                    ).any(),
                    axis=1
                )
            ]

        st.dataframe(
            inventario_filtrado,
            use_container_width=True,
            hide_index=True
        )

except Exception as e:
    st.error(
        f"Error al cargar el archivo: {e}"
    )