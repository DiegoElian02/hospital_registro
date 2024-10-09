# pages\view_table.py
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode

def show_table_page():
    st.title("Tabla de Pacientes")

    # Botón para volver a la página de registro
    if st.button("Registrar Paciente"):
        st.session_state.page = 'Registrar Paciente'
        st.rerun()

    # Leer el DataFrame
    df = pd.read_csv("data/patients.csv")

    # Filtros
    nombre_filter = st.text_input("Filtrar por Nombre")
    sexo_filter = st.multiselect("Filtrar por Sexo", options=df['Sexo'].unique())

    if nombre_filter:
        df = df[df['Paciente'].str.contains(nombre_filter, case=False, na=False)]

    if sexo_filter:
        df = df[df['Sexo'].isin(sexo_filter)]

    # DataFrame básico para mostrar en la tabla
    df_basic = df[['Paciente', 'Fecha de Nacimiento', 'Número de Expediente', 'Sexo', 'Impresión Diagnóstica']]

    # Dividir la página en dos columnas
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Lista de Pacientes")

        # Configurar AgGrid
        gb = GridOptionsBuilder.from_dataframe(df_basic)
        gb.configure_selection(selection_mode='single', use_checkbox=False)
        grid_options = gb.build()

        # Mostrar AgGrid
        grid_response = AgGrid(
            df_basic,
            gridOptions=grid_options,
            height=400,
            width='100%',
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            enable_enterprise_modules=False,
            theme='streamlit'
        )

        # Obtener las filas seleccionadas
        selected_rows = grid_response['selected_rows']

        # Convertir selected_rows a DataFrame
        selected_rows = pd.DataFrame(selected_rows)

    with col2:
        # Verificar si hay filas seleccionadas
        if not selected_rows.empty:
            # Obtener el identificador único del paciente seleccionado (por ejemplo, 'Número de Expediente')
            paciente_id = selected_rows.iloc[0]['Número de Expediente']

            # Buscar el registro completo del paciente en el DataFrame original
            selected_patient_full = df[df['Número de Expediente'] == paciente_id].iloc[0]

            st.subheader(f"Detalles de {selected_patient_full['Paciente']}")

            # Mostrar los detalles del paciente
            for key, value in selected_patient_full.items():
                st.write(f"**{key}:** {value}")
        else:
            st.subheader("Seleccione un paciente para ver los detalles")
