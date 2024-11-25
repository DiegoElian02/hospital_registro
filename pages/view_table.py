# pages/view_table.py
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import os
import datetime
import unicodedata

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
    file_path = "data/patients.csv"
    if os.path.exists(file_path):
        try:
            # Leer el CSV sin parsear las fechas
            df = pd.read_csv(file_path, encoding='utf-8')

            # Eliminar la columna "Fecha y Hora" si existe
            if 'Fecha y Hora' in df.columns:
                df.drop(columns=['Fecha y Hora'], inplace=True)

            # Parsear solo la fecha de nacimiento para visualización
            df['Fecha de Nacimiento'] = pd.to_datetime(df['Fecha de Nacimiento'], dayfirst=True, errors='coerce')
        except Exception as e:
            st.error("Error al leer la base de datos.")
            st.error(str(e))
            return
    else:
        st.warning("La base de datos está vacía. Registra nuevos pacientes.")
        return

    if df.empty:
        st.warning("La base de datos está vacía. Registra nuevos pacientes.")
        return

    # Concatenar Nombre y Apellidos en el campo "Paciente"
    df['Paciente'] = df['Nombre'] + " " + df['Primer Apellido'] + " " + df['Segundo Apellido']

    # Agregar número de fila al DataFrame
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'N°'}, inplace=True)
    df['N°'] += 1  # Para iniciar el conteo desde 1 en lugar de 0

    # Verificar el número de registros
    st.write(f"Número de registros en la base de datos: {len(df)}")

    # Manejar valores nulos en fechas
    fecha_nacimiento_min_value = df['Fecha de Nacimiento'].min()
    fecha_nacimiento_max_value = df['Fecha de Nacimiento'].max()

    if pd.isnull(fecha_nacimiento_min_value):
        fecha_nacimiento_min_value = datetime.date(1900, 1, 1)
    else:
        fecha_nacimiento_min_value = fecha_nacimiento_min_value.date()

    if pd.isnull(fecha_nacimiento_max_value):
        fecha_nacimiento_max_value = datetime.date.today()
    else:
        fecha_nacimiento_max_value = fecha_nacimiento_max_value.date()

    # Filtros
    with st.expander("Filtros de Búsqueda"):
        nombre_filter = st.text_input("Filtrar por Nombre")
        sexo_filter = st.multiselect("Filtrar por Sexo", options=df['Sexo'].dropna().unique())
        expediente_filter = st.text_input("Filtrar por Número de Expediente")
        curp_filter = st.text_input("Filtrar por CURP")
        tipo_sangre_filter = st.multiselect("Filtrar por Tipo de Sangre", options=df['Tipo de Sangre'].dropna().unique())
        alergias_filter = st.text_input("Filtrar por Alergias")
        medico_filter = st.multiselect("Filtrar por Médico Solicitante", options=df['Medico Solicitante'].dropna().unique())
        procedimiento_filter = st.multiselect("Filtrar por Procedimiento", options=df['Procedimiento'].dropna().unique())
        impresion_filter = st.multiselect("Filtrar por Impresión Diagnóstica", options=df['Impresion diagnostica'].dropna().unique())
        # Rango de fechas de nacimiento
        fecha_nacimiento_min = st.date_input("Fecha de Nacimiento - Desde", value=fecha_nacimiento_min_value)
        fecha_nacimiento_max = st.date_input("Fecha de Nacimiento - Hasta", value=fecha_nacimiento_max_value)

    # Aplicar los filtros
    if nombre_filter:
        df = df[df['Paciente'].str.contains(nombre_filter, case=False, na=False)]

    if sexo_filter:
        df = df[df['Sexo'].isin(sexo_filter)]

    if expediente_filter:
        df = df[df['Numero de Expediente'].astype(str).str.contains(expediente_filter, case=False, na=False)]

    if curp_filter:
        df = df[df['CURP'].str.contains(curp_filter, case=False, na=False)]

    if tipo_sangre_filter:
        df = df[df['Tipo de Sangre'].isin(tipo_sangre_filter)]

    if alergias_filter:
        df = df[df['Alergias'].str.contains(alergias_filter, case=False, na=False)]

    if medico_filter:
        df = df[df['Medico Solicitante'].isin(medico_filter)]

    if procedimiento_filter:
        df = df[df['Procedimiento'].isin(procedimiento_filter)]

    if impresion_filter:
        df = df[df['Impresion diagnostica'].isin(impresion_filter)]

    if fecha_nacimiento_min and fecha_nacimiento_max:
        df = df[(df['Fecha de Nacimiento'] >= pd.to_datetime(fecha_nacimiento_min)) & (df['Fecha de Nacimiento'] <= pd.to_datetime(fecha_nacimiento_max))]

    # DataFrame básico para mostrar en la tabla
    df_basic = df[['N°', 'Paciente', 'Fecha de Nacimiento', 'Numero de Expediente', 'Sexo', 'Tipo de Sangre', 'Impresion diagnostica']]

    # Mostrar el número de registros en la tabla después de aplicar los filtros
    st.write(f"Número de registros en la tabla: {len(df_basic)}")

    # Dividir la página en dos columnas
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Lista de Pacientes")

        # Configurar AgGrid
        gb = GridOptionsBuilder.from_dataframe(df_basic)
        gb.configure_selection(selection_mode='single', use_checkbox=False)
        # Configurar formato de fecha solo para 'Fecha de Nacimiento'
        gb.configure_column('Fecha de Nacimiento', type=['dateColumnFilter', 'customDateTimeFormat'], custom_format_string='dd/MM/yyyy', pivot=True)
        gb.configure_column('N°', pinned='left', width=70)

        # Mostrar el número de fila
        gb.configure_grid_options(rowSelection='single', suppressRowClickSelection=False, enableRowGroup=True, rowDragManaged=True)
        grid_options = gb.build()

        # Mostrar AgGrid
        grid_response = AgGrid(
            df_basic,
            gridOptions=grid_options,
            height=500,  # Puedes ajustar la altura o establecerla en None
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
            paciente_id = selected_rows.iloc[0]['N°'] - 1  # Restar 1 porque el índice original empieza en 0

            # Buscar el registro completo del paciente en el DataFrame original
            selected_patient_full = df[df['N°'] == selected_rows.iloc[0]['N°']].iloc[0]

            # Guardar en session_state para usar en la eliminación
            st.session_state.selected_patient_full = selected_patient_full

            st.subheader(f"Detalles de {selected_patient_full['Paciente']}")

            # Mostrar los detalles del paciente, excluyendo "Fecha y Hora"
            campos = [
                'Nombre', 'Primer Apellido', 'Segundo Apellido', 'CURP', 'Fecha de Nacimiento', 'Sexo',
                'Entidad Federativa', 'Domicilio', 'Telefono', 'Tipo de Sangre', 'Alergias', 'Religion',
                'Numero de Expediente', 'Medico Solicitante', 'Episodio', 'Ubicacion',
                'Procedimiento', 'Motivo del Estudio', 'Comparacion', 'Tecnica', 'Efectuado', 'Dictado',
                'Numero de Acceso', 'Hallazgos', 'Impresion diagnostica'
            ]
            for campo in campos:
                valor = selected_patient_full.get(campo, '')
                if campo == 'Fecha de Nacimiento':
                    if pd.notnull(valor):
                        valor = pd.to_datetime(valor, dayfirst=True, errors='coerce')
                        if pd.notnull(valor):
                            valor = valor.strftime('%d/%m/%Y')
                        else:
                            valor = selected_patient_full.get(campo, '')
                    else:
                        valor = ''
                st.write(f"**{campo}:** {valor}")
        else:
            st.subheader("Seleccione un paciente para ver los detalles")
            if 'selected_patient_full' in st.session_state:
                del st.session_state.selected_patient_full

    # Mostrar los doctores asociados debajo de la tabla en la columna 1
    with col1:
        st.subheader("Doctores Asociados")

        if not selected_rows.empty:
            # Obtener la impresión diagnóstica del paciente seleccionado
            impresion_diagnostica_paciente = selected_patient_full['Impresion diagnostica']

            if pd.notnull(impresion_diagnostica_paciente):
                # Leer el archivo de doctores (ahora JSON)
                doctores_path = "data/doctores.json"
                if os.path.exists(doctores_path):
                    try:
                        # Leer el archivo JSON y convertirlo en un DataFrame
                        doctores_df = pd.read_json(doctores_path, encoding='utf-8')

                        # Función para normalizar texto (quitar acentos y pasar a minúsculas)
                        def normalizar(texto):
                            texto = str(texto).lower()
                            texto = ''.join(
                                c for c in unicodedata.normalize('NFD', texto)
                                if unicodedata.category(c) != 'Mn'
                            )
                            return texto

                        # Normalizar la impresión diagnóstica del paciente
                        impresion_paciente_normalizada = normalizar(impresion_diagnostica_paciente)

                        # Normalizar la impresión diagnóstica de los doctores
                        doctores_df['Impresion diagnostica normalizada'] = doctores_df['Impresion diagnostica'].apply(normalizar)

                        # Filtrar los doctores que coinciden con la impresión diagnóstica del paciente
                        doctores_filtrados = doctores_df[doctores_df['Impresion diagnostica normalizada'] == impresion_paciente_normalizada]

                        if not doctores_filtrados.empty:
                            # Mostrar la información de los doctores como tarjetas de presentación
                            for idx, doctor in doctores_filtrados.iterrows():
                                st.markdown("---")
                                st.markdown(f"**Nombre del Médico:** {doctor['Nombre del Médico']}")
                                st.markdown(f"**Especialidad:** {doctor['Especialidad']}")
                                st.markdown(f"**Teléfono:** {doctor['Teléfono']}")
                                st.markdown(f"**Contacto:** {doctor['Contacto']}")
                        else:
                            st.info("No se encontraron doctores asociados a esta impresión diagnóstica.")
                    except Exception as e:
                        st.error("Error al leer el archivo de doctores.")
                        st.error(str(e))
                else:
                    st.warning("El archivo de doctores no se encontró.")
            else:
                st.info("El paciente seleccionado no tiene una impresión diagnóstica.")
        else:
            st.info("Seleccione un paciente para ver los doctores asociados.")

def delete_selected_record(selected_patient):
    # Leer el DataFrame original sin parsear las fechas
    try:
        df = pd.read_csv("data/patients.csv", encoding='utf-8')

        # Eliminar la columna "Fecha y Hora" si existe
        if 'Fecha y Hora' in df.columns:
            df.drop(columns=['Fecha y Hora'], inplace=True)
    except Exception as e:
        st.error("Error al leer la base de datos.")
        st.error(str(e))
        return

    # Eliminar el registro del paciente seleccionado
    df = df[df['Numero de Expediente'] != selected_patient['Numero de Expediente']]

    # Guardar el DataFrame actualizado sin modificar las fechas
    try:
        df.to_csv("data/patients.csv", index=False, encoding='utf-8')
    except Exception as e:
        st.error("Error al guardar los cambios en la base de datos.")
        st.error(str(e))

def reset_database():
    # Eliminar el archivo CSV y crear uno nuevo vacío con las columnas necesarias, excluyendo 'Fecha y Hora'
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
        'Religion',
        'Tipo de Sangre',
        'Alergias',
        'Numero de Expediente',
        'Medico Solicitante',
        'Episodio',
        'Ubicacion',
        'Procedimiento',
        'Motivo del Estudio',
        'Comparacion',
        'Tecnica',
        'Efectuado',
        'Dictado',
        'Numero de Acceso',
        'Hallazgos',
        'Impresion diagnostica'
    ]
    df_empty = pd.DataFrame(columns=columns)
    try:
        df_empty.to_csv(file_path, index=False, encoding='utf-8')
    except Exception as e:
        st.error("Error al reiniciar la base de datos.")
        st.error(str(e))

def append_to_database(new_data_file):
    file_path = "data/patients.csv"

    # Verificar que se cargó un archivo válido
    if new_data_file is not None:
        try:
            # Leer el archivo cargado sin parsear las fechas
            new_data = pd.read_csv(new_data_file, encoding='utf-8')

            # Eliminar la columna "Fecha y Hora" si existe en los nuevos datos
            if 'Fecha y Hora' in new_data.columns:
                new_data.drop(columns=['Fecha y Hora'], inplace=True)

            # Combinar con la base de datos existente o crear uno nuevo si no existe
            if os.path.exists(file_path):
                df = pd.read_csv(file_path, encoding='utf-8')
                # Eliminar la columna "Fecha y Hora" si existe
                if 'Fecha y Hora' in df.columns:
                    df.drop(columns=['Fecha y Hora'], inplace=True)
                df = pd.concat([df, new_data], ignore_index=True)
            else:
                df = new_data

            # Guardar el DataFrame en el archivo CSV sin modificar las fechas
            df.to_csv(file_path, index=False, encoding='utf-8')
            st.success("Archivo CSV cargado y datos actualizados exitosamente.")
        except UnicodeDecodeError:
            st.error("Error de codificación en el archivo cargado. Asegúrate de que esté en formato UTF-8 o sin caracteres especiales.")
        except Exception as e:
            st.error("Ocurrió un error al procesar el archivo cargado.")
            st.error(str(e))
    else:
        st.warning("Por favor, carga un archivo para proceder.")
