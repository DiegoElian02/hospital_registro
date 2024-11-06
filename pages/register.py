# pages\register.py
import streamlit as st
import pandas as pd
import os
import datetime
from src.authentication import authenticate_user  # Asegúrate de tener esta función

def show_register_page(user_role):
    st.title("Registrar Paciente")

    # Crear columnas para posicionar el botón en la derecha
    header_cols = st.columns([8, 1])
    with header_cols[1]:
        if st.button("Cerrar Sesion"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.page = 'Registrar Paciente'
            st.rerun()

    # Botón para cambiar a la página de escaneo QR
    if st.button("Escanear QR"):
        st.session_state.page = 'Escanear QR'
        st.rerun()

    # Reorganizamos la interfaz: Datos de identificacion primero
    st.subheader("Datos de Identificacion Personal")
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input("Nombre(s)*", max_chars=50)
        primer_apellido = st.text_input("Primer Apellido*", max_chars=50)
        segundo_apellido = st.text_input("Segundo Apellido", max_chars=50)  # Opcional
        curp = st.text_input("CURP*", max_chars=18)
        if len(curp) != 18:
            st.error("CURP debe tener 18 caracteres.")
        fecha_min = datetime.date(1900, 1, 1)
        fecha_max = datetime.date.today()
        fecha_nacimiento = st.date_input("Fecha de Nacimiento*", value=datetime.date(2000, 1, 1), min_value=fecha_min, max_value=fecha_max)
    
    with col2:
        sexo = st.selectbox("Sexo*", ["Masculino", "Femenino", "Otro"])
        entidad_federativa = st.text_input("Entidad Federativa*")  # Estado de residencia
        domicilio = st.text_input("Domicilio*", max_chars=100)
        telefono = st.text_input("Telefono (Opcional)", max_chars=15)
        religion = st.text_input("Religion")  # Nuevo campo de Religion

    # Validacion de campos obligatorios
    if not nombre or not primer_apellido or not curp or not entidad_federativa or not domicilio:
        st.error("Por favor, completa todos los campos obligatorios marcados con *.")

    st.subheader("Informacion Clinica")
    col3, col4 = st.columns(2)
    with col3:
        numero_expediente = st.text_input("Numero de Expediente")
        medico_solicitante = st.text_input("Medico Solicitante")
        episodio = st.text_input("Episodio")
        ubicacion = st.text_input("Ubicacion")
    
    with col4:
        fecha_hora = st.date_input("Fecha y Hora del Estudio")
        procedimiento = st.text_area("Procedimiento")
        motivo_estudio = st.text_area("Motivo del Estudio")
        comparacion = st.text_area("Comparacion")
        tecnica = st.text_area("Tecnica")

    st.subheader("Resultados del Estudio")
    col5, col6 = st.columns(2)
    with col5:
        efectuado = st.text_input("Efectuado")
        dictado = st.text_input("Dictado")
        num_acceso = st.text_input("Numero de Acceso")
    with col6:
        hallazgos = st.text_area("Hallazgos")
        impresion_diagnostica = st.text_area("Impresion Diagnostica")

    # Solo mostramos la barra de contraseña si es admin y se va a registrar el paciente
    if user_role == 'admin':
        st.subheader("Reautenticacion Administrador")
        password = st.text_input("Ingresa tu contraseña nuevamente", type="password")

    # Boton para registrar el paciente
    if st.button("Registrar"):
        # Validacion de campos obligatorios
        if not nombre or not primer_apellido or len(curp) != 18:
            st.error("Por favor, completa correctamente los campos obligatorios.")
        else:
            # Si es administrador, pedimos y verificamos la contraseña
            if user_role == 'admin':
                if not password:
                    st.error("Por favor, ingresa tu contraseña para continuar.")
                    return
                user = authenticate_user('admin', password)
                if not user:
                    st.error("Contraseña incorrecta")
                    return

            # Registro de paciente despues de validacion
            registrar_paciente(nombre, primer_apellido, segundo_apellido, curp, fecha_nacimiento, sexo,
                               entidad_federativa, domicilio, telefono, religion, numero_expediente, 
                               medico_solicitante, episodio, ubicacion, fecha_hora, procedimiento, 
                               motivo_estudio, comparacion, tecnica, efectuado, dictado, num_acceso, 
                               hallazgos, impresion_diagnostica)
            st.success("Paciente registrado exitosamente")

    if user_role == 'admin':
        if st.button("Ver Tabla de Pacientes"):
            st.session_state.page = 'Ver Tabla'
            st.rerun()

def registrar_paciente(nombre, primer_apellido, segundo_apellido, curp, fecha_nacimiento, sexo,
                       entidad_federativa, domicilio, telefono, religion, numero_expediente, 
                       medico_solicitante, episodio, ubicacion, fecha_hora, procedimiento, 
                       motivo_estudio, comparacion, tecnica, efectuado, dictado, num_acceso, 
                       hallazgos, impresion_diagnostica):
    
    new_patient = {
        'Nombre': nombre,
        'Primer Apellido': primer_apellido,
        'Segundo Apellido': segundo_apellido,
        'CURP': curp,
        'Fecha de Nacimiento': fecha_nacimiento,
        'Sexo': sexo,
        'Entidad Federativa': entidad_federativa,
        'Domicilio': domicilio,
        'Telefono': telefono,
        'Religion': religion,  # Campo de Religion agregado
        'Numero de Expediente': numero_expediente,
        'Medico Solicitante': medico_solicitante,
        'Episodio': episodio,
        'Ubicacion': ubicacion,
        'Fecha y Hora': fecha_hora,
        'Procedimiento': procedimiento,
        'Motivo del Estudio': motivo_estudio,
        'Comparacion': comparacion,
        'Tecnica': tecnica,
        'Efectuado': efectuado,
        'Dictado': dictado,
        'Numero de Acceso': num_acceso,
        'Hallazgos': hallazgos,
        'Impresion Diagnostica': impresion_diagnostica
    }
    save_patient(new_patient)

def save_patient(patient_data):
    file_path = "data/patients.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        # Definir las columnas si el archivo no existe
        df = pd.DataFrame(columns=[
            'Nombre',
            'Primer Apellido',
            'Segundo Apellido',
            'CURP',
            'Fecha de Nacimiento',
            'Sexo',
            'Entidad Federativa',
            'Domicilio',
            'Telefono',
            'Religion',  # Nueva columna de Religion
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
            'Impresion Diagnostica'
        ])

    # Crear un DataFrame a partir de los datos del paciente
    new_patient_df = pd.DataFrame([patient_data])

    # Agregar la nueva fila al DataFrame existente
    df = pd.concat([df, new_patient_df], ignore_index=True)

    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv(file_path, index=False) 
