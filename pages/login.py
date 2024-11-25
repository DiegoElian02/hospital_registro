# pages/login.py
import streamlit as st
from src.authentication import authenticate_user
import os

def show_login_page():
    # Crear columnas para posicionar el logo y el título
    col1, col2 = st.columns([8, 1])

    with col1:
        st.title("Login")

    with col2:
        # Ruta a la imagen del logo
        logo_path = os.path.join('images', 'logo.jpg')
        # Mostrar la imagen del logo
        st.image(logo_path, width=220)

    # Campos de entrada
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        user = authenticate_user(username, password)
        if user:
            st.session_state.authenticated = True
            st.session_state.user_role = 'admin' if user == 'admin' else 'user'
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

    # Aviso de Privacidad
    with st.expander("Aviso de Privacidad"):
        st.write("""
        **AVISO DE PRIVACIDAD SIMPLIFICADO DE LOS EXPEDIENTES CLÍNICOS**

        DigiMed, sistema de gestión y digitalización de expedientes clínicos, es responsable del tratamiento de los datos personales que nos proporcione.

        **Finalidades Principales:**

        Los datos personales recabados serán utilizados para:

        - Crear y mantener un expediente clínico digital actualizado.
        - Facilitar el acceso a información clínica para médicos y personal autorizado.
        - Generar estadísticas médicas y epidemiológicas para la toma de decisiones en el ámbito hospitalario.
        - Garantizar la seguridad y privacidad de los datos clínicos en cumplimiento con las normativas aplicables.

        **Finalidades Adicionales:**

        De manera adicional, los datos podrán ser utilizados para:

        - Optimizar los servicios hospitalarios mediante análisis de datos clínicos.
        - Enviar notificaciones sobre actualizaciones del sistema o cambios en el manejo de datos personales.

        En caso de que no desee que sus datos personales sean tratados para estas finalidades adicionales, puede manifestarlo mediante un correo electrónico a privacidad@digimed.com antes de la implementación de los datos en el sistema.

        **Transferencia de Datos:**

        Sus datos personales podrán ser compartidos con:

        - Instituciones gubernamentales de salud pública para monitoreo y evaluación de políticas sanitarias.
        - Autoridades regulatorias, en cumplimiento de normativas y auditorías correspondientes.

        Estas transferencias no requieren su consentimiento, ya que están fundamentadas y motivadas en las leyes aplicables.

        **Acceso y Consulta:**

        Usted puede consultar el aviso de privacidad integral, así como ejercer sus derechos de acceso, rectificación, cancelación y oposición (ARCO), visitando nuestro sitio web en [www.digimed.com/aviso-privacidad](http://www.digimed.com/aviso-privacidad).

        DigiMed garantiza la seguridad y protección de su información conforme a la NOM-004-SSA3-2012, NOM-024-SSA3-2012, Ley Federal de Protección de Datos Personales en Posesión de los Particulares, y demás normativas aplicables.
        """)
