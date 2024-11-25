# pages/register.py
import streamlit as st
import pandas as pd
import os
import datetime
from src.authentication import authenticate_user  # Asegúrate de tener esta función

def show_register_page(user_role):
    # Crear columnas para posicionar el logo y el título
    col1, col2 = st.columns([8, 1])

    with col1:
        st.title("Registrar Paciente")

    with col2:
        # Ruta a la imagen del logo
        logo_path = os.path.join('images', 'logo.jpg')
        # Mostrar la imagen del logo
        st.image(logo_path, width=220)

    # Colocar los botones en una fila
    button_cols = st.columns([1, 6, 1])

    with button_cols[0]:
        if st.button("Escanear QR"):
            st.session_state.page = 'Escanear QR'
            st.rerun()

    with button_cols[2]:
        if st.button("Cerrar Sesión"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.page = 'Registrar Paciente'
            st.rerun()

    st.subheader("Datos de Identificación Personal")
    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre(s)*", max_chars=50)
        primer_apellido = st.text_input("Primer Apellido*", max_chars=50)
        segundo_apellido = st.text_input("Segundo Apellido", max_chars=50)
        curp = st.text_input("CURP*", max_chars=18)
        if len(curp) != 18:
            st.error("CURP debe tener 18 caracteres.")
        fecha_min = datetime.date(1900, 1, 1)
        fecha_max = datetime.date.today()
        fecha_nacimiento = st.date_input("Fecha de Nacimiento*", value=datetime.date(2000, 1, 1), min_value=fecha_min, max_value=fecha_max)
        tipo_sangre = st.selectbox("Tipo de Sangre*", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

    with col2:
        sexo = st.selectbox("Sexo*", ["Masculino", "Femenino", "Otro"])
        entidad_federativa = st.text_input("Entidad Federativa*")
        domicilio = st.text_input("Domicilio*", max_chars=100)
        telefono = st.text_input("Teléfono (Opcional)", max_chars=15)
        religion = st.text_input("Religión")
        alergias = st.text_area("Alergias")

    if not nombre or not primer_apellido or not curp or not entidad_federativa or not domicilio or not tipo_sangre:
        st.error("Por favor, completa todos los campos obligatorios marcados con *.")

    st.subheader("Información Clínica")
    col3, col4 = st.columns(2)
    with col3:
        numero_expediente = st.text_input("Número de Expediente")
        medico_solicitante = st.text_input("Médico Solicitante")
        episodio = st.text_input("Episodio")
        ubicacion = st.text_input("Ubicación")

    with col4:
        fecha_hora = st.date_input("Fecha y Hora del Estudio")
        procedimiento = st.text_area("Procedimiento")
        motivo_estudio = st.text_area("Motivo del Estudio")
        comparacion = st.text_area("Comparación")
        tecnica = st.text_area("Técnica")

    st.subheader("Resultados del Estudio")
    col5, col6 = st.columns(2)
    with col5:
        efectuado = st.text_input("Efectuado")
        dictado = st.text_input("Dictado")
        num_acceso = st.text_input("Número de Acceso")
    with col6:
        hallazgos = st.text_area("Hallazgos")
        impresion_diagnostica = st.text_area("Impresión Diagnóstica")

    if user_role == 'admin':
        st.subheader("Reautenticación Administrador")
        password = st.text_input("Ingresa tu contraseña nuevamente", type="password")

    if st.button("Registrar"):
        if not nombre or not primer_apellido or len(curp) != 18 or not tipo_sangre:
            st.error("Por favor, completa correctamente los campos obligatorios.")
        else:
            if user_role == 'admin':
                if not password:
                    st.error("Por favor, ingresa tu contraseña para continuar.")
                    return
                user = authenticate_user('admin', password)
                if not user:
                    st.error("Contraseña incorrecta")
                    return

            try:
                registrar_paciente(nombre, primer_apellido, segundo_apellido, curp, fecha_nacimiento, sexo,
                                   entidad_federativa, domicilio, telefono, religion, tipo_sangre, alergias,
                                   numero_expediente, medico_solicitante, episodio, ubicacion, fecha_hora,
                                   procedimiento, motivo_estudio, comparacion, tecnica, efectuado, dictado,
                                   num_acceso, hallazgos, impresion_diagnostica)
                st.success("Paciente registrado exitosamente")
            except Exception as e:
                st.error("Ocurrió un error al registrar el paciente.")
                st.error(str(e))

    if user_role == 'admin':
        if st.button("Ver Tabla de Pacientes"):
            st.session_state.page = 'Ver Tabla'
            st.rerun()

def registrar_paciente(nombre, primer_apellido, segundo_apellido, curp, fecha_nacimiento, sexo,
                       entidad_federativa, domicilio, telefono, religion, tipo_sangre, alergias,
                       numero_expediente, medico_solicitante, episodio, ubicacion, fecha_hora,
                       procedimiento, motivo_estudio, comparacion, tecnica, efectuado, dictado,
                       num_acceso, hallazgos, impresion_diagnostica):

    # Formatear la fecha de nacimiento al formato deseado
    fecha_nacimiento_formateada = fecha_nacimiento.strftime('%d/%m/%Y %I:%M:%S %p')
    fecha_hora_formateada = fecha_hora.strftime('%d/%m/%Y %I:%M:%S %p')

    new_patient = {
        'Nombre': nombre,
        'Primer Apellido': primer_apellido,
        'Segundo Apellido': segundo_apellido,
        'CURP': curp,
        'Fecha de Nacimiento': fecha_nacimiento_formateada,
        'Sexo': sexo,
        'Entidad Federativa': entidad_federativa,
        'Domicilio': domicilio,
        'Telefono': telefono,
        'Religion': religion,
        'Tipo de Sangre': tipo_sangre,
        'Alergias': alergias,
        'Numero de Expediente': numero_expediente,
        'Medico Solicitante': medico_solicitante,
        'Episodio': episodio,
        'Ubicacion': ubicacion,
        'Fecha y Hora': fecha_hora_formateada,
        'Procedimiento': procedimiento,
        'Motivo del Estudio': motivo_estudio,
        'Comparacion': comparacion,
        'Tecnica': tecnica,
        'Efectuado': efectuado,
        'Dictado': dictado,
        'Numero de acceso': num_acceso,
        'Hallazgos': hallazgos,
        'Impresion diagnostica': impresion_diagnostica
    }
    save_patient(new_patient)

def save_patient(patient_data):
    file_path = "data/patients.csv"
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
        'Fecha y Hora',
        'Procedimiento',
        'Motivo del Estudio',
        'Comparacion',
        'Tecnica',
        'Efectuado',
        'Dictado',
        'Numero de acceso',
        'Hallazgos',
        'Impresion diagnostica'
    ]

    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except Exception as e:
            st.error("Error al leer la base de datos existente.")
            st.error(str(e))
            df = pd.DataFrame(columns=columns)
    else:
        df = pd.DataFrame(columns=columns)

    # Crear un DataFrame a partir de los datos del paciente
    new_patient_df = pd.DataFrame([patient_data])

    # Asegurar que las columnas estén en el orden correcto
    new_patient_df = new_patient_df[columns]

    # Agregar la nueva fila al DataFrame existente
    df = pd.concat([df, new_patient_df], ignore_index=True)

    try:
        # Guardar el DataFrame actualizado en el archivo CSV
        df.to_csv(file_path, index=False, encoding='utf-8')
    except Exception as e:
        st.error("Error al guardar los datos del paciente.")
        st.error(str(e))
