# pages\register.py
import streamlit as st
import pandas as pd
import os

def show_register_page(user_role):
    st.title("Registrar Paciente")

    # Crear columnas para posicionar el botón en la derecha
    header_cols = st.columns([8, 1])
    with header_cols[1]:
        if st.button("Cerrar Sesión"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.page = 'Registrar Paciente'
            st.rerun()

    # Dividir la página en dos columnas para evitar que sea muy larga
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Información del Paciente")
        nombre = st.text_input("Paciente")
        fecha_nacimiento = st.date_input("Fecha de Nacimiento")
        numero_expediente = st.text_input("Número de Expediente")
        sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"])
        episodio = st.text_input("Episodio")
        ubicacion = st.text_input("Ubicación")

        st.subheader("Procedimiento")
        procedimiento = st.text_area("Procedimiento")
        motivo_estudio = st.text_area("Motivo del Estudio")
        comparacion = st.text_area("Comparación")
        tecnica = st.text_area("Técnica")

    with col2:
        st.subheader("Detalles Adicionales")
        efectuado = st.text_input("Efectuado")
        dictado = st.text_input("Dictado")
        num_acceso = st.text_input("Número de Acceso")
        medico_solicitante = st.text_input("Médico Solicitante")
        fecha_hora = st.date_input("Fecha y Hora")

        st.subheader("Resultados")
        hallazgos = st.text_area("Hallazgos")
        impresion_diagnostica = st.text_area("Impresión Diagnóstica")

        # Botón para registrar el paciente
        if st.button("Registrar"):
            new_patient = {
                'Paciente': nombre,
                'Fecha de Nacimiento': fecha_nacimiento,
                'Número de Expediente': numero_expediente,
                'Sexo': sexo,
                'Episodio': episodio,
                'Ubicación': ubicacion,
                'Efectuado': efectuado,
                'Dictado': dictado,
                'Número de Acceso': num_acceso,
                'Médico Solicitante': medico_solicitante,
                'Fecha y Hora': fecha_hora,
                'Procedimiento': procedimiento,
                'Motivo del Estudio': motivo_estudio,
                'Comparación': comparacion,
                'Técnica': tecnica,
                'Hallazgos': hallazgos,
                'Impresión Diagnóstica': impresion_diagnostica
            }
            save_patient(new_patient)
            st.success("Paciente registrado exitosamente")
            
        st.image("images/logo.png", use_column_width=True)

    if user_role == 'admin':
        if st.button("Ver Tabla de Pacientes"):
            st.session_state.page = 'Ver Tabla'
            st.rerun()

def save_patient(patient_data):
    file_path = "data/patients.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        # Definir las columnas si el archivo no existe
        df = pd.DataFrame(columns=[
            'Paciente',
            'Fecha de Nacimiento',
            'Número de Expediente',
            'Sexo',
            'Episodio',
            'Ubicación',
            'Efectuado',
            'Dictado',
            'Número de Acceso',
            'Médico Solicitante',
            'Fecha y Hora',
            'Procedimiento',
            'Motivo del Estudio',
            'Comparación',
            'Técnica',
            'Hallazgos',
            'Impresión Diagnóstica'
        ])

    # Crear un DataFrame a partir de los datos del paciente
    new_patient_df = pd.DataFrame([patient_data])

    # Agregar la nueva fila al DataFrame existente
    df = pd.concat([df, new_patient_df], ignore_index=True)

    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv(file_path, index=False)
