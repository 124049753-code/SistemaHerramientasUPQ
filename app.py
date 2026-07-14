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

# Ruta correcta del inventario
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

    # ==========================================
    # LIMPIEZA DEL INVENTARIO
    # ==========================================

    inventario = inventario.replace(
        ["None", "nan", "NaN"],
        pd.NA
    )

    inventario = inventario.dropna(
        axis=1,
        how="all"
    )

    inventario = inventario.dropna(
        how="all"
    )

    inventario = inventario.fillna("")

    inventario = inventario.reset_index(
        drop=True
    )

    # ==========================================
    # MÉTRICAS
    # ==========================================

    cantidad_total = 0

    for columna in inventario.columns:

        suma = pd.to_numeric(
            inventario[columna],
            errors="coerce"
        ).fillna(0).sum()

        if suma > cantidad_total:
            cantidad_total = suma

    total_herramientas = len(inventario)

    # ==========================================
    # DASHBOARD
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📦 Herramientas",
            total_herramientas
        )

    with col2:
        st.metric(
            "🔢 Piezas disponibles",
            int(cantidad_total)
        )

    with col3:
        st.metric(
            "🏢 Almacén",
            almacen
        )

    with col4:
        st.metric(
            "📑 Almacenes",
            len(archivo.sheet_names)
        )

    st.divider()

    # ==========================================
    # INVENTARIO
    # ==========================================

    if menu == "📦 Inventario":

        st.header(
            f"📦 Inventario - {almacen}"
        )

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
                        case=False,
                        na=False
                    ).any(),
                    axis=1
                )
            ]

        st.dataframe(
            inventario_filtrado,
            use_container_width=True,
            hide_index=True
        )

    # ==========================================
    # SOLICITUD DE HERRAMIENTAS
    # ==========================================

    elif menu == "📝 Solicitar herramienta":

        st.header(
            "📝 Solicitud de préstamo"
        )

        col1, col2 = st.columns(2)

        with col1:
            matricula = st.text_input(
                "🎓 Matrícula"
            )

            nombre = st.text_input(
                "👤 Nombre completo"
            )

            carrera = st.text_input(
                "🏫 Carrera"
            )

        with col2:
            profesor = st.text_input(
                "👨‍🏫 Profesor responsable"
            )

            materia = st.text_input(
                "📚 Materia"
            )

            fecha_devolucion = st.date_input(
                "📅 Fecha de devolución"
            )

        herramienta = st.selectbox(
            "🔧 Herramienta solicitada",
            inventario.iloc[:, 0]
            .astype(str)
            .tolist()
        )

        cantidad = st.number_input(
            "🔢 Cantidad",
            min_value=1,
            value=1
        )

        observaciones = st.text_area(
            "📝 Observaciones"
        )

        if st.button(
            "📋 Enviar solicitud"
        ):
            st.success(
                "Solicitud enviada correctamente."
            )

    # ==========================================
    # PRÉSTAMOS ACTIVOS
    # ==========================================

    elif menu == "📋 Préstamos activos":

        st.header(
            "📋 Préstamos activos"
        )

        st.info(
            "Aquí aparecerán las herramientas actualmente prestadas."
        )

    # ==========================================
    # DEVOLUCIONES
    # ==========================================

    elif menu == "🔄 Devoluciones":

        st.header(
            "🔄 Registro de devoluciones"
        )

        st.info(
            "Aquí se registrarán las devoluciones."
        )

    # ==========================================
    # HERRAMIENTAS DAÑADAS
    # ==========================================

    elif menu == "🛠 Herramientas dañadas":

        st.header(
            "🛠 Herramientas dañadas"
        )

        st.info(
            "Aquí se registrarán los daños y mantenimientos."
        )

    # ==========================================
    # REPORTES
    # ==========================================

    elif menu == "📈 Reportes":

        st.header(
            "📈 Reportes y estadísticas"
        )

        st.metric(
            "Herramientas registradas",
            total_herramientas
        )

        st.metric(
            "Piezas disponibles",
            int(cantidad_total)
        )

except Exception as e:

    st.error(
        f"Error al cargar el archivo: {e}"
    )