# pages/QR_Scanner.py
import streamlit as st
import pandas as pd
import numpy as np
import os
import json
from PIL import Image
import cv2
import datetime

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
                # Asumiendo que el código QR contiene la información del paciente en formato JSON
                try:
                    patient_data = json.loads(data)

                    st.success("Código QR escaneado exitosamente.")

                    # Mostrar los detalles del paciente
                    st.subheader("Información del Paciente")
                    campos_paciente = [
                        'Nombre', 'Primer Apellido', 'Segundo Apellido', 'CURP', 'Fecha de Nacimiento', 'Sexo',
                        'Entidad Federativa', 'Domicilio', 'Telefono', 'Religion'
                    ]
                    for campo in campos_paciente:
                        st.write(f"**{campo}:** {patient_data.get(campo, '')}")

                    st.subheader("Datos de la Consulta")

                    # Campos específicos de la consulta
                    with st.form("consulta_form"):
                        numero_expediente = st.text_input("Nmero de Expediente")
                        medico_solicitante = st.text_input("Medico Solicitante")
                        episodio = st.text_input("Episodio")
                        ubicacion = st.text_input("Ubicacion")
                        fecha_hora = st.date_input("Fecha y Hora del Estudio", value=datetime.date.today())
                        procedimiento = st.text_area("Procedimiento")
                        motivo_estudio = st.text_area("Motivo del Estudio")
                        comparacion = st.text_area("Comparacion")
                        tecnica = st.text_area("Tecnica")
                        efectuado = st.text_input("Efectuado")
                        dictado = st.text_input("Dictado")
                        num_acceso = st.text_input("Numero de Acceso")
                        hallazgos = st.text_area("Hallazgos")
                        impresion_diagnostica = st.text_area("Impresion Diagnostica")

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
                                             'Impresion Diagnostica': impresion_diagnostica}

                        # Guardar el registro en el archivo CSV
                        save_consultation(registro_completo)
                        st.success("Consulta registrada exitosamente en la base de datos.")
                except json.JSONDecodeError as e:
                    st.error("Error al decodificar la información del código QR.")
                    st.error(str(e))
                except Exception as e:
                    st.error("Ocurrió un error inesperado.")
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
        'Entidad Federativa', 'Domicilio', 'Telefono', 'Religion', 'Número de Expediente',
        'Médico Solicitante', 'Episodio', 'Ubicación', 'Fecha y Hora', 'Procedimiento',
        'Motivo del Estudio', 'Comparación', 'Técnica', 'Efectuado', 'Dictado', 'Número de Acceso',
        'Hallazgos', 'Impresión Diagnóstica'
    ]
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=all_fields)

    # Crear un DataFrame a partir de los datos de la consulta
    new_consultation_df = pd.DataFrame([consultation_data])

    # Agregar la nueva fila al DataFrame existente
    df = pd.concat([df, new_consultation_df], ignore_index=True)

    # Guardar el DataFrame actualizado en el archivo CSV
    df.to_csv(file_path, index=False)
