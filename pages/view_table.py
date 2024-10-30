import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import os

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
            st.error("¿Estas seguro de que deseas eliminar el registro seleccionado?")
            confirm_delete_cols = st.columns([1, 1])
            with confirm_delete_cols[0]:
                if st.button("Si, eliminar"):
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
            st.error("¿Estas seguro de que deseas eliminar todos los registros? Esta accion no se puede deshacer.")
            confirm_reset_cols = st.columns([1, 1])
            with confirm_reset_cols[0]:
                if st.button("Si, resetear"):
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
        st.warning("La base de datos esta vacia. Registra nuevos pacientes.")
        return

    if df.empty:
        st.warning("La base de datos esta vacia. Registra nuevos pacientes.")
        return

    # Concatenar Nombre y Apellidos en el campo "Paciente"
    df['Paciente'] = df['Nombre'] + " " + df['Primer Apellido'] + " " + df['Segundo Apellido']

    # Filtros
    nombre_filter = st.text_input("Filtrar por Nombre")
    sexo_filter = st.multiselect("Filtrar por Sexo", options=df['Sexo'].unique())

    if nombre_filter:
        df = df[df['Paciente'].str.contains(nombre_filter, case=False, na=False)]

    if sexo_filter:
        df = df[df['Sexo'].isin(sexo_filter)]

    # DataFrame basico para mostrar en la tabla
    df_basic = df[['Paciente', 'Fecha de Nacimiento', 'Numero de Expediente', 'Sexo', 'Impresion Diagnostica']]

    # Dividir la pagina en dos columnas
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
            # Obtener el identificador unico del paciente seleccionado
            paciente_id = selected_rows.iloc[0]['Numero de Expediente']

            # Buscar el registro completo del paciente en el DataFrame original
            selected_patient_full = df[df['Numero de Expediente'] == paciente_id].iloc[0]

            # Guardar en session_state para usar en la eliminacion
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
                st.write(f"**{campo}:** {selected_patient_full[campo]}")
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
    # Eliminar el archivo CSV y crear uno nuevo vacio con las columnas necesarias
    file_path = "data/patients.csv"
    if os.path.exists(file_path):
        os.remove(file_path)

    # Crear un nuevo DataFrame vacio con las columnas definidas
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
