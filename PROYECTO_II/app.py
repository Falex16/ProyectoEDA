from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from libreria_clases_proyecto2 import DataAnalyzer


def validar_dataset_cargado():
    if st.session_state.df_telco is None:
        st.title(menu)
        st.warning("Debes cargar el dataset en el modulo 'Carga de datos' antes de continuar.")
        st.stop()


def crear_analyzer():
    validar_dataset_cargado()
    return DataAnalyzer(st.session_state.df_telco)


def mostrar_grafico_barras(dataframe, x, y=None, hue=None, titulo=None, rotacion=30):
    fig, ax = plt.subplots(figsize=(9, 4))
    sns.barplot(data=dataframe, x=x, y=y, hue=hue, ax=ax)
    ax.set_title(titulo or "")
    ax.tick_params(axis="x", rotation=rotacion)
    st.pyplot(fig)


def mostrar_histograma(dataframe, columna, bins):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(data=dataframe, x=columna, bins=bins, kde=True, ax=ax)
    ax.set_title(f"Distribucion de {columna}")
    ax.set_xlabel(columna)
    ax.set_ylabel("Frecuencia")
    st.pyplot(fig)


st.set_page_config(
    page_title="Telco Customer Churn - EDA",
    layout="wide"
)

sns.set_theme(style="whitegrid")

if "df_telco" not in st.session_state:
    st.session_state.df_telco = None


st.sidebar.title("Telco Customer Churn")
menu = st.sidebar.selectbox(
    "Selecciona un modulo",
    [
        "🏠 Home",
        "📂 Carga de datos",
        "🧹 Limpieza y transformacion",
        "📊 Analisis exploratorio",
        "📈 Visualizaciones",
        "✅ Conclusiones"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Proyecto Python for Analytics")

if st.session_state.df_telco is not None:
    st.sidebar.success("Dataset cargado")
else:
    st.sidebar.warning("Dataset pendiente")


if menu == "🏠 Home":
    logo_path = Path("imagenes/logo.png")

    if logo_path.exists():
        col_logo, col_titulo = st.columns([1, 12])

        with col_logo:
            st.image(str(logo_path), width=80)

        with col_titulo:
            st.title("Analisis Exploratorio de Datos - Telco Customer Churn")
    else:
        st.title("Analisis Exploratorio de Datos - Telco Customer Churn")

    st.markdown("""
    Esta aplicacion interactiva realiza un **Analisis Exploratorio de Datos (EDA)**
    sobre el dataset **Telco Customer Churn**, con el objetivo de identificar
    patrones asociados a la fuga de clientes en una empresa de telecomunicaciones.

    El proyecto no construye modelos predictivos. Su enfoque es limpiar, transformar,
    analizar y visualizar los datos para apoyar la toma de decisiones de retencion.
    """)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👨‍💻 Datos del autor")
        st.write("**Nombre completo:** Fabrizio Pena Panduro")
        st.write("**Curso / Especializacion:** Python for Analytics")
        st.write("**Anio:** 2026")

    with col2:
        st.subheader("📌 Dataset utilizado")
        st.write("""
        El dataset contiene informacion de clientes, servicios contratados,
        facturacion mensual, cargos totales, tiempo de permanencia y estado de
        abandono del cliente.
        """)

    st.divider()
    st.subheader("🎯 Objetivo del analisis")
    st.write("""
    Comprender los factores asociados a la fuga de clientes mediante limpieza,
    transformacion, estadistica descriptiva y visualizaciones interactivas.
    """)

    st.divider()
    st.subheader("🛠️ Tecnologias utilizadas")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🐍 Lenguaje", "Python")
    col2.metric("📋 Datos", "Pandas")
    col3.metric("🔢 Numerico", "NumPy")
    col4.metric("🌐 App", "Streamlit")
    st.write("Tambien se utilizan Matplotlib y Seaborn para la visualizacion.")


elif menu == "📂 Carga de datos":
    st.title("Carga del dataset")
    st.markdown("""
    Antes de ejecutar cualquier analisis, la aplicacion necesita cargar el archivo
    de datos mediante `st.file_uploader()`. Se aceptan archivos CSV y Excel.
    """)

    archivo_datos = st.file_uploader(
        "Carga el archivo de datos",
        type=["csv", "xlsx", "xls"]
    )

    if archivo_datos is not None:
        try:
            nombre_archivo = archivo_datos.name.lower()

            if nombre_archivo.endswith(".csv"):
                df = pd.read_csv(archivo_datos)
            elif nombre_archivo.endswith((".xlsx", ".xls")):
                df = pd.read_excel(archivo_datos)
            else:
                st.session_state.df_telco = None
                st.error("Formato no permitido. Carga un archivo CSV o Excel.")
                st.stop()

            st.session_state.df_telco = df
            st.success("Archivo cargado correctamente.")

            filas_preview = st.slider("Numero de filas para vista previa", 5, 30, 5)
            st.subheader("Vista previa del dataset")
            st.dataframe(df.head(filas_preview), use_container_width=True)

            st.subheader("Dimensiones del dataset")
            filas, columnas = df.shape
            col1, col2 = st.columns(2)
            col1.metric("Filas", filas)
            col2.metric("Columnas", columnas)

            if st.checkbox("Mostrar nombres de columnas"):
                st.write(df.columns.tolist())

        except Exception as error:
            st.session_state.df_telco = None
            st.error(f"No se pudo cargar el archivo. Detalle del error: {error}")
    else:
        st.session_state.df_telco = None
        st.warning("Primero debes cargar un archivo CSV o Excel para continuar.")


elif menu == "🧹 Limpieza y transformacion":
    analyzer = crear_analyzer()
    df = analyzer.df

    st.title("Limpieza y transformacion")
    st.markdown("""
    En este modulo se revisan transformaciones necesarias para que el analisis sea
    consistente. La transformacion principal es convertir `TotalCharges` a valor
    numerico, porque originalmente llega como texto.
    """)

    col1, col2, col3 = st.columns(3)
    col1.metric("Filas", df.shape[0])
    col2.metric("Columnas", df.shape[1])
    col3.metric("Duplicados", int(df.duplicated().sum()))

    tab1, tab2, tab3 = st.tabs(["Tipos de datos", "Valores nulos", "Vista limpia"])

    with tab1:
        tipos = pd.DataFrame({
            "Variable": df.columns,
            "Tipo de dato": df.dtypes.astype(str).values
        })
        st.dataframe(tipos, use_container_width=True)
        st.info("`TotalCharges` fue convertido a numerico y `SeniorCitizen` fue etiquetado como Yes/No.")

    with tab2:
        nulos = analyzer.valores_nulos()
        st.dataframe(nulos, use_container_width=True)
        nulos_filtrados = nulos[nulos["Valores nulos"] > 0]
        if not nulos_filtrados.empty:
            mostrar_grafico_barras(
                nulos_filtrados,
                x="Variable",
                y="Valores nulos",
                titulo="Variables con valores nulos"
            )
        else:
            st.success("No se encontraron valores nulos despues de la transformacion.")

    with tab3:
        st.dataframe(df.head(10), use_container_width=True)


elif menu == "📊 Analisis exploratorio":
    analyzer = crear_analyzer()
    df = analyzer.df
    numericas, categoricas = analyzer.clasificar_variables()

    st.title("Analisis Exploratorio de Datos (EDA)")
    st.markdown("""
    Este modulo presenta 10 items de analisis para comprender la estructura del
    dataset y los patrones asociados al abandono de clientes.
    """)

    tabs = st.tabs([
        "1. Info general",
        "2. Variables",
        "3. Estadisticas",
        "4. Faltantes",
        "5. Numericas",
        "6. Categoricas",
        "7. Num vs Churn",
        "8. Cat vs Churn",
        "9. Analisis dinamico",
        "10. Hallazgos"
    ])

    with tabs[0]:
        st.subheader("Item 1: Informacion general del dataset")
        st.write("Se revisa la estructura general del dataset, los tipos de datos y los valores nulos.")
        col1, col2, col3 = st.columns(3)
        col1.metric("Filas", df.shape[0])
        col2.metric("Columnas", df.shape[1])
        col3.metric("Valores nulos", int(df.isnull().sum().sum()))

        st.text(analyzer.informacion_general())
        tipos = pd.DataFrame({"Variable": df.columns, "Tipo": df.dtypes.astype(str).values})
        st.dataframe(tipos, use_container_width=True)
        st.dataframe(analyzer.valores_nulos(), use_container_width=True)

    with tabs[1]:
        st.subheader("Item 2: Clasificacion de variables")
        st.write("Se utiliza una funcion personalizada dentro de la clase `DataAnalyzer` para separar variables numericas y categoricas.")
        col1, col2 = st.columns(2)
        col1.metric("Variables numericas", len(numericas))
        col2.metric("Variables categoricas", len(categoricas))
        col1.write(numericas)
        col2.write(categoricas)

    with tabs[2]:
        st.subheader("Item 3: Estadisticas descriptivas")
        st.write("Se aplican medidas como media, mediana, moda y dispersion para resumir el comportamiento de los datos.")
        st.dataframe(analyzer.estadisticas_descriptivas(), use_container_width=True)

        variable_num = st.selectbox("Selecciona una variable numerica", numericas)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Media", round(df[variable_num].mean(), 2))
        col2.metric("Mediana", round(df[variable_num].median(), 2))
        col3.metric("Desviacion", round(df[variable_num].std(), 2))
        col4.metric("Moda", analyzer.moda_variable(variable_num))
        st.info("La media resume el promedio, la mediana indica el centro de la distribucion y la desviacion muestra dispersion.")

    with tabs[3]:
        st.subheader("Item 4: Analisis de valores faltantes")
        st.write("Se identifican variables con datos faltantes y se visualiza su magnitud.")
        nulos = analyzer.valores_nulos()
        st.dataframe(nulos, use_container_width=True)
        nulos_filtrados = nulos[nulos["Valores nulos"] > 0]
        if not nulos_filtrados.empty:
            mostrar_grafico_barras(nulos_filtrados, "Variable", "Valores nulos", titulo="Conteo de valores faltantes")
            st.warning("Los valores faltantes deben revisarse antes de interpretar resultados finales.")
        else:
            st.success("No hay valores faltantes detectados.")

    with tabs[4]:
        st.subheader("Item 5: Distribucion de variables numericas")
        st.write("Los histogramas permiten observar concentracion, asimetria y dispersion de variables numericas.")
        variable_hist = st.selectbox("Variable numerica para histograma", numericas, key="hist_num")
        bins = st.slider("Cantidad de intervalos del histograma", 5, 60, 25)
        mostrar_histograma(df, variable_hist, bins)
        st.info("Una distribucion concentrada en valores bajos o altos puede revelar perfiles de clientes especificos.")

    with tabs[5]:
        st.subheader("Item 6: Analisis de variables categoricas")
        st.write("Se analizan conteos y proporciones de variables categoricas.")
        variable_cat = st.selectbox("Variable categorica", categoricas, key="cat_count")
        conteo = df[variable_cat].value_counts().reset_index()
        conteo.columns = [variable_cat, "Conteo"]
        conteo["Proporcion (%)"] = (conteo["Conteo"] / len(df) * 100).round(2)
        st.dataframe(conteo, use_container_width=True)
        mostrar_grafico_barras(conteo, variable_cat, "Conteo", titulo=f"Conteo de {variable_cat}")

    with tabs[6]:
        st.subheader("Item 7: Analisis bivariado numerico vs categorico")
        st.write("Se comparan variables numericas frente a `Churn` para observar diferencias entre clientes que abandonan y los que permanecen.")
        variable_biv_num = st.selectbox("Variable numerica", numericas, key="biv_num")
        st.dataframe(analyzer.resumen_por_churn(variable_biv_num), use_container_width=True)

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=df, x="Churn", y=variable_biv_num, ax=ax)
        ax.set_title(f"{variable_biv_num} vs Churn")
        st.pyplot(fig)
        st.info("La comparacion de grupos ayuda a detectar diferencias en permanencia, cargos mensuales o cargos totales.")

    with tabs[7]:
        st.subheader("Item 8: Analisis bivariado categorico vs categorico")
        st.write("Se evalua la relacion entre variables categoricas y el abandono de clientes.")
        opciones_cat = [col for col in categoricas if col not in ["customerID", "Churn"]]
        variable_biv_cat = st.selectbox("Variable categorica", opciones_cat, key="biv_cat")
        tabla = pd.crosstab(df[variable_biv_cat], df["Churn"])
        proporciones = pd.crosstab(df[variable_biv_cat], df["Churn"], normalize="index") * 100
        st.write("Conteo")
        st.dataframe(tabla, use_container_width=True)
        st.write("Proporcion por categoria (%)")
        st.dataframe(proporciones.round(2), use_container_width=True)

        plot_data = proporciones.reset_index().melt(id_vars=variable_biv_cat, var_name="Churn", value_name="Porcentaje")
        mostrar_grafico_barras(plot_data, variable_biv_cat, "Porcentaje", hue="Churn", titulo=f"{variable_biv_cat} vs Churn")

    with tabs[8]:
        st.subheader("Item 9: Analisis basado en parametros seleccionados")
        st.write("El usuario puede elegir columnas y filtros para construir un analisis dinamico.")
        columnas_elegidas = st.multiselect(
            "Selecciona columnas para visualizar",
            df.columns.tolist(),
            default=["Contract", "InternetService", "MonthlyCharges", "tenure", "Churn"]
        )
        churn_filtro = st.selectbox("Filtrar por Churn", ["Todos", "Yes", "No"])

        df_filtrado = df.copy()
        if churn_filtro != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Churn"] == churn_filtro]

        if columnas_elegidas:
            st.dataframe(df_filtrado[columnas_elegidas].head(50), use_container_width=True)
            st.metric("Registros filtrados", len(df_filtrado))
        else:
            st.warning("Selecciona al menos una columna.")

    with tabs[9]:
        st.subheader("Item 10: Hallazgos clave")
        st.write("Resumen visual de los principales patrones observados en el EDA.")

        churn_rate = analyzer.tasa_churn()
        if churn_rate is not None:
            col1, col2 = st.columns(2)
            col1.metric("Clientes que abandonan (%)", churn_rate.get("Yes", 0))
            col2.metric("Clientes que permanecen (%)", churn_rate.get("No", 0))

        resumen_contrato = pd.crosstab(df["Contract"], df["Churn"], normalize="index") * 100
        resumen_contrato = resumen_contrato.reset_index()
        if "Yes" in resumen_contrato.columns:
            resumen_contrato = resumen_contrato[["Contract", "Yes"]].rename(columns={"Yes": "Churn (%)"})
            mostrar_grafico_barras(resumen_contrato, "Contract", "Churn (%)", titulo="Tasa de churn por tipo de contrato")

        st.markdown("""
        **Insights principales:**
        - La permanencia (`tenure`) es una variable clave para entender la fuga.
        - Los contratos mensuales suelen concentrar una mayor proporcion de churn.
        - Los cargos mensuales permiten comparar diferencias entre clientes que abandonan y permanecen.
        - El metodo de pago y el servicio de internet ayudan a perfilar grupos de mayor riesgo.
        """)


elif menu == "📈 Visualizaciones":
    analyzer = crear_analyzer()
    df = analyzer.df
    numericas, categoricas = analyzer.clasificar_variables()

    st.title("Visualizaciones")
    st.markdown("Espacio para explorar graficos adicionales de forma interactiva.")

    tipo_grafico = st.selectbox(
        "Selecciona tipo de grafico",
        ["Histograma", "Boxplot por Churn", "Barras categoricas", "Heatmap de correlacion"]
    )

    if tipo_grafico == "Histograma":
        variable = st.selectbox("Variable numerica", numericas)
        bins = st.slider("Bins", 5, 60, 25, key="viz_bins")
        mostrar_histograma(df, variable, bins)

    elif tipo_grafico == "Boxplot por Churn":
        variable = st.selectbox("Variable numerica", numericas, key="viz_box")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=df, x="Churn", y=variable, ax=ax)
        ax.set_title(f"{variable} por Churn")
        st.pyplot(fig)

    elif tipo_grafico == "Barras categoricas":
        variable = st.selectbox("Variable categorica", [c for c in categoricas if c != "customerID"])
        conteo = df[variable].value_counts().reset_index()
        conteo.columns = [variable, "Conteo"]
        mostrar_grafico_barras(conteo, variable, "Conteo", titulo=f"Conteo de {variable}")

    else:
        corr = df[numericas].corr()
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.heatmap(corr, annot=True, cmap="Blues", ax=ax)
        ax.set_title("Correlacion entre variables numericas")
        st.pyplot(fig)


elif menu == "✅ Conclusiones":
    analyzer = crear_analyzer()
    df = analyzer.df

    st.title("Conclusiones finales")
    st.markdown("""
    Las conclusiones se enfocan en la toma de decisiones para mejorar la retencion
    de clientes, no en la prediccion automatica de churn.
    """)

    churn_rate = analyzer.tasa_churn()
    if churn_rate is not None:
        col1, col2 = st.columns(2)
        col1.metric("Churn Yes (%)", churn_rate.get("Yes", 0))
        col2.metric("Churn No (%)", churn_rate.get("No", 0))

    st.subheader("5 conclusiones basadas en el EDA")
    st.markdown("""
    1. Los clientes con menor tiempo de permanencia deben ser monitoreados con mayor atencion, porque la variable `tenure` permite diferenciar grupos con comportamientos distintos frente al abandono.
    2. El tipo de contrato es un factor relevante para la retencion; los contratos mensuales muestran mayor exposicion a fuga que los contratos de uno o dos anios.
    3. Los cargos mensuales ayudan a identificar segmentos sensibles al precio, especialmente cuando se comparan clientes que abandonaron frente a clientes que permanecen.
    4. Los servicios contratados, como internet, soporte tecnico y seguridad en linea, permiten detectar combinaciones de productos asociadas a mayor o menor abandono.
    5. La empresa debe priorizar estrategias de retencion sobre adquisicion, ya que retener clientes existentes es mas eficiente que reemplazarlos por nuevos clientes.
    """)

    st.subheader("Recomendaciones de negocio")
    st.write("""
    Se recomienda disenar campanias de retencion para clientes con contrato mensual,
    baja permanencia y cargos mensuales altos. Tambien conviene evaluar paquetes de
    servicios que aumenten valor percibido y reduzcan la probabilidad de abandono.
    """)
