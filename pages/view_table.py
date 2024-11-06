# pages/view_table.py
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import os
import datetime

def show_table_page():
    st.title("Tabla de Pacientes")

    # Botón para cargar CSV
    uploaded_file = st.file_uploader("Cargar archivo CSV de pacientes", type=["csv"])
    if uploaded_file is not None:
        # Pasar directamente el archivo a append_to_database
        append_to_database(uploaded_file)

    # Inicializar variables de estado para confirmaciones
    if 'confirm_delete' not in st.session_state:
        st.session_state.confirm_delete = False

    if 'confirm_reset' not in st.session_state:
        st.session_state.confirm_reset = False

    # Botones para acciones
    action_cols = st.columns([1, 1, 2])
    with action_cols[0]:
        if st.button("Registrar Paciente"):
            st.session_state.page = 'Registrar Paciente'
            st.rerun()

    with action_cols[1]:
        if st.session_state.confirm_delete:
            st.error("¿Estás seguro de que deseas eliminar el registro seleccionado?")
            confirm_delete_cols = st.columns([1, 1])
            with confirm_delete_cols[0]:
                if st.button("Sí, eliminar"):
                    delete_selected_record(st.session_state.selected_patient_full)
                    st.success("Registro eliminado exitosamente.")
                    st.session_state.confirm_delete = False
                    st.rerun()
            with confirm_delete_cols[1]:
                if st.button("Cancelar"):
                    st.session_state.confirm_delete = False
        else:
            if st.button("Eliminar Registro Seleccionado"):
                if 'selected_patient_full' in st.session_state:
                    st.session_state.confirm_delete = True
                else:
                    st.warning("Por favor, selecciona un paciente para eliminar.")

    with action_cols[2]:
        if st.session_state.confirm_reset:
            st.error("¿Estás seguro de que deseas eliminar todos los registros? Esta acción no se puede deshacer.")
            confirm_reset_cols = st.columns([1, 1])
            with confirm_reset_cols[0]:
                if st.button("Sí, resetear"):
                    reset_database()
                    st.success("Base de datos reseteada exitosamente.")
                    st.session_state.confirm_reset = False
                    st.rerun()
            with confirm_reset_cols[1]:
                if st.button("Cancelar"):
                    st.session_state.confirm_reset = False
        else:
            if st.button("Resetear Base de Datos"):
                st.session_state.confirm_reset = True

    # Leer el DataFrame
    if os.path.exists("data/patients.csv"):
        df = pd.read_csv("data/patients.csv")
    else:
        st.warning("La base de datos está vacía. Registra nuevos pacientes.")
        return

    if df.empty:
        st.warning("La base de datos está vacía. Registra nuevos pacientes.")
        return

    # Concatenar Nombre y Apellidos en el campo "Paciente"
    df['Paciente'] = df['Nombre'] + " " + df['Primer Apellido'] + " " + df['Segundo Apellido']

    # Convertir columnas de fecha a datetime
    df['Fecha de Nacimiento'] = pd.to_datetime(df['Fecha de Nacimiento'], errors='coerce')
    df['Fecha y Hora'] = pd.to_datetime(df['Fecha y Hora'], errors='coerce')

    # Manejar valores nulos en fechas
    fecha_nacimiento_min_value = df['Fecha de Nacimiento'].min()
    fecha_nacimiento_max_value = df['Fecha de Nacimiento'].max()
    fecha_estudio_min_value = df['Fecha y Hora'].min()
    fecha_estudio_max_value = df['Fecha y Hora'].max()

    if pd.isnull(fecha_nacimiento_min_value):
        fecha_nacimiento_min_value = datetime.date(1900, 1, 1)
    else:
        fecha_nacimiento_min_value = fecha_nacimiento_min_value.date()

    if pd.isnull(fecha_nacimiento_max_value):
        fecha_nacimiento_max_value = datetime.date.today()
    else:
        fecha_nacimiento_max_value = fecha_nacimiento_max_value.date()

    if pd.isnull(fecha_estudio_min_value):
        fecha_estudio_min_value = datetime.date(1900, 1, 1)
    else:
        fecha_estudio_min_value = fecha_estudio_min_value.date()

    if pd.isnull(fecha_estudio_max_value):
        fecha_estudio_max_value = datetime.date.today()
    else:
        fecha_estudio_max_value = fecha_estudio_max_value.date()

    # Filtros
    with st.expander("Filtros de Búsqueda"):
        nombre_filter = st.text_input("Filtrar por Nombre")
        sexo_filter = st.multiselect("Filtrar por Sexo", options=df['Sexo'].dropna().unique())
        expediente_filter = st.text_input("Filtrar por Número de Expediente")
        curp_filter = st.text_input("Filtrar por CURP")
        medico_filter = st.multiselect("Filtrar por Médico Solicitante", options=df['Medico Solicitante'].dropna().unique())
        procedimiento_filter = st.multiselect("Filtrar por Procedimiento", options=df['Procedimiento'].dropna().unique())
        impresion_filter = st.multiselect("Filtrar por Impresión Diagnóstica", options=df['Impresion Diagnostica'].dropna().unique())
        # Rango de fechas de nacimiento
        fecha_nacimiento_min = st.date_input("Fecha de Nacimiento - Desde", value=fecha_nacimiento_min_value)
        fecha_nacimiento_max = st.date_input("Fecha de Nacimiento - Hasta", value=fecha_nacimiento_max_value)
        # Rango de fechas de estudios
        fecha_estudio_min = st.date_input("Fecha del Estudio - Desde", value=fecha_estudio_min_value)
        fecha_estudio_max = st.date_input("Fecha del Estudio - Hasta", value=fecha_estudio_max_value)

    # Aplicar los filtros
    if nombre_filter:
        df = df[df['Paciente'].str.contains(nombre_filter, case=False, na=False)]

    if sexo_filter:
        df = df[df['Sexo'].isin(sexo_filter)]

    if expediente_filter:
        df = df[df['Numero de Expediente'].astype(str).str.contains(expediente_filter, case=False, na=False)]

    if curp_filter:
        df = df[df['CURP'].str.contains(curp_filter, case=False, na=False)]

    if medico_filter:
        df = df[df['Medico Solicitante'].isin(medico_filter)]

    if procedimiento_filter:
        df = df[df['Procedimiento'].isin(procedimiento_filter)]

    if impresion_filter:
        df = df[df['Impresion Diagnostica'].isin(impresion_filter)]

    if fecha_nacimiento_min and fecha_nacimiento_max:
        df = df[(df['Fecha de Nacimiento'] >= pd.to_datetime(fecha_nacimiento_min)) & (df['Fecha de Nacimiento'] <= pd.to_datetime(fecha_nacimiento_max))]

    if fecha_estudio_min and fecha_estudio_max:
        df = df[(df['Fecha y Hora'] >= pd.to_datetime(fecha_estudio_min)) & (df['Fecha y Hora'] <= pd.to_datetime(fecha_estudio_max))]

    # DataFrame básico para mostrar en la tabla
    df_basic = df[['Paciente', 'Fecha de Nacimiento', 'Numero de Expediente', 'Sexo', 'Impresion Diagnostica']]

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
            # Obtener el identificador único del paciente seleccionado
            paciente_id = selected_rows.iloc[0]['Numero de Expediente']

            # Buscar el registro completo del paciente en el DataFrame original
            selected_patient_full = df[df['Numero de Expediente'] == paciente_id].iloc[0]

            # Guardar en session_state para usar en la eliminación
            st.session_state.selected_patient_full = selected_patient_full

            st.subheader(f"Detalles de {selected_patient_full['Paciente']}")

            # Mostrar los detalles del paciente, incluyendo los campos faltantes
            campos = [
                'Nombre', 'Primer Apellido', 'Segundo Apellido', 'CURP', 'Fecha de Nacimiento', 'Sexo',
                'Entidad Federativa', 'Domicilio', 'Telefono', 'Numero de Expediente', 'Medico Solicitante',
                'Episodio', 'Ubicacion', 'Fecha y Hora', 'Procedimiento', 'Motivo del Estudio', 'Comparacion',
                'Tecnica', 'Efectuado', 'Dictado', 'Numero de Acceso', 'Hallazgos', 'Impresion Diagnostica', 'Religion'
            ]
            for campo in campos:
                st.write(f"**{campo}:** {selected_patient_full.get(campo, '')}")
        else:   
            st.subheader("Seleccione un paciente para ver los detalles")
            if 'selected_patient_full' in st.session_state:
                del st.session_state.selected_patient_full

def delete_selected_record(selected_patient):
    # Leer el DataFrame original
    df = pd.read_csv("data/patients.csv")

    # Eliminar el registro del paciente seleccionado
    df = df[df['Numero de Expediente'] != selected_patient['Numero de Expediente']]

    # Guardar el DataFrame actualizado
    df.to_csv("data/patients.csv", index=False)

def reset_database():
    # Eliminar el archivo CSV y crear uno nuevo vacío con las columnas necesarias
    file_path = "data/patients.csv"
    if os.path.exists(file_path):
        os.remove(file_path)

    # Crear un nuevo DataFrame vacío con las columnas definidas
    columns = [
        'Nombre',
        'Primer Apellido',
        'Segundo Apellido',
        'CURP',
        'Fecha de Nacimiento',
        'Sexo',
        'Entidad Federativa',
        'Domicilio',
        'Telefono',
        'Numero de Expediente',
        'Medico Solicitante',
        'Episodio',
        'Ubicacion',
        'Fecha y Hora',
        'Procedimiento',
        'Motivo del Estudio',
        'Comparacion',
        'Tecnica',
        'Efectuado',
        'Dictado',
        'Numero de Acceso',
        'Hallazgos',
        'Impresion Diagnostica',
        'Religion'
    ]
    df_empty = pd.DataFrame(columns=columns)
    df_empty.to_csv(file_path, index=False)

def append_to_database(new_data_file):
    file_path = "data/patients.csv"

    # Verificar que se cargó un archivo válido
    if new_data_file is not None:
        try:
            # Leer el archivo cargado
            new_data = pd.read_csv(new_data_file)
        except UnicodeDecodeError:
            st.error("Error de codificación en el archivo cargado. Asegúrate de que esté en formato ISO-8859-1 o sin caracteres especiales.")

        # Combinar con la base de datos existente o crear uno nuevo si no existe
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = pd.concat([df, new_data], ignore_index=True)
        else:
            df = new_data

        # Guardar el DataFrame en el archivo CSV
        df.to_csv(file_path, index=False)
    else:
        st.warning("Por favor, carga un archivo para proceder.")
