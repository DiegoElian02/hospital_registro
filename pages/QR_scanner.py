# pages/QR_Scanner.py
import streamlit as st
import pandas as pd
import numpy as np
import os
import json
from PIL import Image
import cv2
import datetime
import unicodedata  # Para normalizar texto

def show_qr_scanner_page():
    st.title("Escanear QR del Paciente")

    # Botón para volver a la página de registro
    if st.button("Volver al Registro"):
        st.session_state.page = 'Registrar Paciente'
        st.rerun()

    st.write("Por favor, escanea el código QR del paciente o sube una imagen del mismo.")

    # Opciones para escanear el QR: cámara o subir imagen
    option = st.radio("Selecciona una opción para ingresar el código QR:", ('Usar Cámara', 'Subir Imagen'))

    if option == 'Usar Cámara':
        # Capturar imagen desde la cámara
        img_file_buffer = st.camera_input("Escanear Código QR")
    else:
        # Subir imagen desde el equipo
        img_file_buffer = st.file_uploader("Sube una imagen con el código QR", type=["png", "jpg", "jpeg"])

    if img_file_buffer is not None:
        # Leer la imagen
        image = Image.open(img_file_buffer)
        image_np = np.array(image.convert('RGB'))

        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

        # Inicializar el detector de códigos QR
        detector = cv2.QRCodeDetector()

        # Detectar y decodificar el código QR
        data, vertices_array, _ = detector.detectAndDecode(gray)

        if vertices_array is not None:
            if data:
                # Ahora el QR contiene el CURP cifrado
                try:
                    # Desencriptar el CURP usando el cifrado César
                    encrypted_curp = data
                    patient_curp = decrypt_curp(encrypted_curp)

                    st.success("Código QR escaneado y CURP descifrado exitosamente.")

                    # Leer el archivo patients.csv y buscar el paciente por CURP
                    file_path = "data/patients.csv"
                    if os.path.exists(file_path):
                        df_patients = pd.read_csv(file_path, encoding='utf-8')
                    else:
                        st.error("La base de datos de pacientes no existe.")
                        return

                    # Buscar el paciente en la base de datos
                    patient_records = df_patients[df_patients['CURP'] == patient_curp]

                    if patient_records.empty:
                        st.warning("Paciente no encontrado en la base de datos. Puedes registrar una nueva consulta.")
                        return

                    # Obtener los datos del paciente
                    patient_data = patient_records.iloc[-1].to_dict()

                    # Crear dos columnas
                    col1, col2 = st.columns([1, 1])

                    # Inicializar registro_completo
                    registro_completo = None

                    # Mostrar el formulario para registrar una nueva consulta en la columna izquierda
                    with col1:
                        st.subheader("Información del Paciente")

                        # Mostrar los detalles del paciente obtenido de la base de datos
                        campos_paciente = [
                            'Nombre', 'Primer Apellido', 'Segundo Apellido', 'CURP', 'Fecha de Nacimiento', 'Sexo',
                            'Entidad Federativa', 'Domicilio', 'Telefono', 'Religion', 'Tipo de Sangre', 'Alergias'
                        ]
                        for campo in campos_paciente:
                            st.write(f"**{campo}:** {patient_data.get(campo, '')}")

                        st.subheader("Datos de la Consulta")

                        # Campos específicos de la consulta
                        with st.form("consulta_form"):
                            numero_expediente = st.text_input("Número de Expediente")
                            medico_solicitante = st.text_input("Médico Solicitante")
                            episodio = st.text_input("Episodio")
                            ubicacion = st.text_input("Ubicación")
                            fecha_hora = st.date_input("Fecha y Hora del Estudio", value=datetime.date.today())
                            procedimiento = st.text_area("Procedimiento")
                            motivo_estudio = st.text_area("Motivo del Estudio")
                            comparacion = st.text_area("Comparación")
                            tecnica = st.text_area("Técnica")
                            efectuado = st.text_input("Efectuado")
                            dictado = st.text_input("Dictado")
                            num_acceso = st.text_input("Número de Acceso")
                            hallazgos = st.text_area("Hallazgos")
                            impresion_diagnostica = st.text_area("Impresion diagnostica")

                            submit_button = st.form_submit_button(label='Registrar Consulta')

                        if submit_button:
                            # Combinar los datos del paciente y de la consulta
                            registro_completo = {**patient_data,
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
                                                 'Impresion diagnostica': impresion_diagnostica}

                            # Guardar el registro en el archivo CSV
                            save_consultation(registro_completo)
                            st.success("Consulta registrada exitosamente en la base de datos.")
                            st.experimental_rerun()

                    # Mostrar el historial y los doctores asociados en la columna derecha
                    with col2:
                        st.subheader("Historial del Paciente")

                        # Actualizar los registros del paciente después de guardar una nueva consulta
                        if registro_completo is not None:
                            # Volver a cargar df_patients y patient_records
                            df_patients = pd.read_csv(file_path, encoding='utf-8')
                            patient_records = df_patients[df_patients['CURP'] == patient_curp]

                        # Mostrar el historial de consultas del paciente
                        historial = patient_records.copy()

                        # Convertir fechas para visualización
                        for campo_fecha in ['Fecha de Nacimiento', 'Fecha y Hora']:
                            if campo_fecha in historial.columns:
                                historial[campo_fecha] = pd.to_datetime(historial[campo_fecha], dayfirst=True, errors='coerce')
                                historial[campo_fecha] = historial[campo_fecha].dt.strftime('%d/%m/%Y')

                        # Mostrar el historial en una tabla
                        st.dataframe(historial)

                        # Mostrar los doctores asociados
                        st.subheader("Doctores Asociados")

                        # Obtener la última impresión diagnóstica del historial
                        impresion_diagnostica_paciente = patient_records.iloc[-1].get('Impresion diagnostica', '')

                        if impresion_diagnostica_paciente:
                            # Leer el archivo de doctores
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
                            st.info("El paciente no tiene una impresión diagnóstica registrada.")
                except Exception as e:
                    st.error("Error al procesar el código QR.")
                    st.error(str(e))
            else:
                st.warning("No se pudo decodificar el código QR. Asegúrate de que contiene datos válidos.")
        else:
            st.warning("No se detectó ningún código QR en la imagen. Por favor, intenta nuevamente.")

def save_consultation(consultation_data):
    file_path = "data/patients.csv"
    # Definir las columnas
    all_fields = [
        'Nombre', 'Primer Apellido', 'Segundo Apellido', 'CURP', 'Fecha de Nacimiento', 'Sexo',
        'Entidad Federativa', 'Domicilio', 'Telefono', 'Religion', 'Tipo de Sangre', 'Alergias',
        'Numero de Expediente', 'Medico Solicitante', 'Episodio', 'Ubicacion', 'Fecha y Hora',
        'Procedimiento', 'Motivo del Estudio', 'Comparacion', 'Tecnica', 'Efectuado', 'Dictado',
        'Numero de Acceso', 'Hallazgos', 'Impresion diagnostica'
    ]
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='utf-8')
    else:
        df = pd.DataFrame(columns=all_fields)

    # Crear un DataFrame a partir de los datos de la consulta
    new_consultation_df = pd.DataFrame([consultation_data])

    # Asegurar que las columnas estén en el orden correcto
    new_consultation_df = new_consultation_df[all_fields]

    # Agregar la nueva fila al DataFrame existente
    df = pd.concat([df, new_consultation_df], ignore_index=True)

    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv(file_path, index=False, encoding='utf-8')

def decrypt_curp(encrypted_curp, shift=3):
    decrypted = ''
    for char in encrypted_curp:
        if char.isupper():
            decrypted += chr((ord(char) - shift - 65) % 26 + 65)
        elif char.islower():
            decrypted += chr((ord(char) - shift - 97) % 26 + 97)
        elif char.isdigit():
            decrypted += chr((ord(char) - shift - 48) % 10 + 48)
        else:
            decrypted += char  # No modifica caracteres especiales
    return decrypted
