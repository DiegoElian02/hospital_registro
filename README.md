# Aplicación de Registro de Pacientes en Streamlit

Esta aplicación permite registrar pacientes en un hospital y guardar sus datos en un archivo CSV. Cuenta con autenticación básica y diferentes niveles de acceso para administradores y usuarios.

## Características

- **Autenticación de Usuarios**: Sistema de login para usuarios y administradores.
- **Registro de Pacientes**: Formulario para ingresar datos de pacientes, con imágenes en la interfaz.
- **Vista de Tabla**: Los administradores pueden ver y filtrar la tabla de pacientes.
- **Navegación Personalizada**: Navegación entre páginas sin utilizar la barra lateral.
- **Cierre de Sesión**: Opción para cerrar sesión desde la página de registro.
- **Interfaz Personalizada**: Oculta la barra lateral para una experiencia más limpia.

## Estructura del Proyecto

```
- .streamlit/
  - config.toml
- data/
  - patients.csv
- images/
  - imagen1.png
  - imagen2.png
- pages/
  - login.py
  - register.py
  - view_table.py
- src/
  - authentication.py
- README.md
- requirements.txt
- app.py
```

- **`.streamlit/config.toml`**: Configuración para ocultar la barra lateral.
- **`data/`**: Almacena el archivo `patients.csv` con los datos de los pacientes.
- **`images/`**: Contiene las imágenes utilizadas en la aplicación.
- **`pages/`**: Incluye las diferentes páginas de la aplicación.
- **`src/`**: Contiene módulos auxiliares como la autenticación.
- **`app.py`**: Punto de entrada de la aplicación.
- **`requirements.txt`**: Lista de dependencias necesarias.
- **`README.md`**: Este archivo.

## Instalación y Ejecución

### Prerrequisitos

- **Python 3.7 o superior** instalado en tu sistema.
- **Pip** para manejar las instalaciones de paquetes.

### Pasos de Instalación

1. **Clonar el Repositorio**

   Clona el repositorio en tu máquina local:

   ```bash
   git clone https://github.com/DiegoElian02/hospital_registro
   ```

2. **Navegar al Directorio del Proyecto**

   ```bash
   cd tu_repositorio
   ```

3. **Crear un Entorno Virtual (Opcional pero Recomendado)**

   ```bash
   python -m venv venv
   ```

   Activa el entorno virtual:

   - En Windows:

     ```bash
     venv\Scripts\activate
     ```

   - En macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Instalar las Dependencias**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar el Archivo `config.toml`**

   Asegúrate de que el archivo `config.toml` está en la carpeta `.streamlit` y contiene:

   ```toml
   [client]
   showSidebarNavigation = false
   ```

6. **Agregar tus Imágenes**

   Coloca tus imágenes en la carpeta `images/` y asegúrate de que los nombres coincidan con los utilizados en el código (`imagen1.png`, `imagen2.png`).

7. **Ejecutar la Aplicación**

   ```bash
   streamlit run app.py
   ```

## Uso de la Aplicación

### Credenciales de Acceso

- **Administrador**
  - Usuario: `admin`
  - Contraseña: `admin`

- **Usuario**
  - Usuario: `usuario`
  - Contraseña: `usuario`

### Funcionalidades

1. **Página de Login**

   - Ingresa tus credenciales para acceder a la aplicación.
   - Si las credenciales son correctas, serás dirigido a la página de registro de pacientes.

2. **Página de Registro de Pacientes**

   - **Todos los Usuarios:**
     - Completa el formulario con los datos del paciente.
     - Haz clic en "Registrar" para guardar los datos.
     - Las imágenes se muestran en el lado izquierdo para mejorar la interfaz.

   - **Administrador:**
     - Además del botón "Registrar", verá el botón "Ver Tabla de Pacientes".
     - Puede cerrar sesión haciendo clic en "Cerrar Sesión" en la esquina superior derecha.

3. **Página de Tabla de Pacientes** (Solo Administrador)

   - Visualiza todos los pacientes registrados en una tabla.
   - Usa los filtros para buscar pacientes por nombre o género.
   - Haz clic en "Registrar Paciente" para volver a la página de registro.

### Cierre de Sesión

- En cualquier momento, puedes cerrar sesión haciendo clic en "Cerrar Sesión" en la esquina superior derecha de la página de registro.

## Dependencias

El archivo `requirements.txt` contiene las siguientes dependencias:

```txt
streamlit
pandas
```

Si has añadido paquetes adicionales (como `Pillow` para manipular imágenes), asegúrate de incluirlos en este archivo:

```txt
streamlit
pandas
Pillow
```
