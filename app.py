# app.py
import streamlit as st
from src.authentication import authenticate_user

# Configuración de la página
showSidebarNavigation = False
st.set_page_config(page_title="Hospital App", layout="wide")

# Autenticación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'page' not in st.session_state:
    st.session_state.page = 'Registrar Paciente'

if not st.session_state.authenticated:
    from pages import login
    login.show_login_page()
else:
    user_role = st.session_state.user_role
    # Navegación entre páginas
    if st.session_state.page == 'Registrar Paciente':
        from pages import register
        register.show_register_page(user_role)
    elif st.session_state.page == 'Ver Tabla':
        from pages import view_table
        view_table.show_table_page()
    elif st.session_state.page == 'Escanear QR':  # Nueva página de escaneo QR
        from pages import QR_scanner
        QR_scanner.show_qr_scanner_page()
