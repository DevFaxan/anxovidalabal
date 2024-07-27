import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu
import os
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import cv2
import mediapipe as mp
import pygwalker as pyg

# Función para cargar animaciones Lottie desde una URL
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Cargar la animación Lottie
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_0yfsb3a1.json")

# Define file paths
datos_file = 'datos_pacientes.xlsx'
credenciales_file = 'credenciales.xlsx'
profesionales_file = 'profesionales.xlsx'
clientes_file = 'clientes.xlsx'
ejercicios_file = 'ejercicios_pacientes.xlsx'
credentials_file = 'credentials.xlsx'  # Archivo de credenciales para login
logo_file = 'TecHealth_Logo.png'

# Load or create the data file
def load_excel(file, columns):
    if os.path.exists(file):
        return pd.read_excel(file)
    else:
        return pd.DataFrame(columns=columns)

# Save data to an Excel file
def save_to_excel(df, file):
    df.to_excel(file, index=False)

# Load user credentials file
@st.cache_data
def load_credentials(file):
    if os.path.exists(file):
        return pd.read_excel(file)
    else:
        st.error(f"File '{file}' not found.")
        return pd.DataFrame(columns=['Nombre', 'DNI'])

# Validate user credentials
def validate_credentials(nombre, dni, df_credenciales):
    return not df_credenciales[(df_credenciales['Nombre'] == nombre) & (df_credenciales['DNI'] == dni)].empty

# Load login credentials
@st.cache_data
def load_login_credentials(file):
    if os.path.exists(file):
        return pd.read_excel(file)
    else:
        st.error(f"File '{file}' not found.")
        return pd.DataFrame(columns=['email', 'password'])

# Validate login credentials
def check_login_credentials(email, password, df_login_credentials):
    if email in df_login_credentials['email'].values:
        stored_password = df_login_credentials.loc[df_login_credentials['email'] == email, 'password'].values[0]
        if password == stored_password:
            return True
    return False

# Initialize dataframes
df_datos = load_excel(datos_file, ['Fecha', 'Nombre', 'DNI', 'Posición Corporal', 'Nombre Ejercicio', 'Repeticiones', 'Tiempo (min)', 'Kilos'])
df_credenciales = load_credentials(credenciales_file)
df_profesionales = load_excel(profesionales_file, ['ID', 'Nombre', 'Apellidos', 'Direccion', 'DNI', 'Telefono', 'Municipio', 'Codigo Postal', 'Tipo'])
df_clientes = load_excel(clientes_file, ['ID', 'Nombre', 'Apellidos', 'Direccion', 'DNI', 'Telefono', 'Municipio', 'Codigo Postal'])
df_ejercicios = load_excel(ejercicios_file, ['POSICIÓN CORPORAL', 'NOMBRE EJERCICIO'])
df_login_credentials = load_login_credentials(credentials_file)

# Cargar la imagen del logotipo
try:
    logo_image = Image.open(logo_file)
except FileNotFoundError:
    logo_image = None

# Autenticación de usuarios
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def login():
    st.sidebar.header("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type='password')
    login_button = st.sidebar.button("Login", key="login_button")

    if login_button:
        if check_login_credentials(email, password, df_login_credentials):
            st.sidebar.success("Login successful!")
            st.session_state['authenticated'] = True
        else:
            st.sidebar.error("Invalid email or password")

login()

# Sidebar menu with the logo and option menu
selected = None
with st.sidebar:
    if logo_image:
        st.image(logo_image, use_column_width=True)
    selected = option_menu(
        menu_title=None,
        options=["Home", "Data", "View Data", "Masters", "Analysis", "Video"],
        icons=["house", "table", "eye", "person", "bar-chart", "camera"],
        menu_icon="cast",
        default_index=0,
    )

# Define page functions
def home_page():
    with st.container():
        st.subheader("🏃 Bienvenido a TecHealth 🏃")
        st.title("💪 Salud y Tecnología a alcance de todos 🖥️ ")
        st.write("En TecHealth, fusionamos la innovación tecnológica con el cuidado de la salud para ofrecer soluciones accesibles que mejoren la calidad de vida de las personas. Descubre cómo nuestra tecnología puede ayudarte a mantener un estilo de vida saludable, prevenir enfermedades y optimizar tu recuperación.")
        with st.container():
            st.write("---")
            left_column, right_column = st.columns(2)
            with left_column:
                st.header("Nuestro Propósito")
                st.write(
                    """
                    Nuestro propósito en TecHealth es empoderar a individuos y comunidades proporcionando tecnología avanzada y soluciones de salud accesibles. Nos dedicamos a innovar y aplicar la tecnología de manera que cada persona pueda alcanzar su máximo potencial de bienestar. Estamos comprometidos con la creación de herramientas que faciliten un acceso equitativo a la salud, mejorando la vida de las personas a través de la prevención, la gestión y la rehabilitación de enfermedades.
                    """
                )
            with right_column:
                if lottie_coding:
                    st_lottie(lottie_coding, height=300, key="coding")
                else:
                    st.error("Lottie animation not loaded")

        with st.container():
            st.write("---")
            st.header("¿Quienes somos")
            image_column, text_column = st.columns((1, 2))
            with image_column:
                if logo_image:
                    st.image(logo_image)
                else:
                    st.error("Image not loaded")
            with text_column:
                st.write(
                    """
                    En TecHealth, te encontrarás con un portal integral donde la tecnología se une con el cuidado de la salud al servicio de individuos y profesionales del sector. Nuestra plataforma no solo ofrece información y herramientas para el público general, sino que también proporciona recursos especializados para profesionales de la salud. Explora soluciones avanzadas de gestión de pacientes, acceso a estudios de caso, formaciones continuas y tecnología de punta diseñada para optimizar los procesos médicos y mejorar los resultados clínicos. Todo esto, en un entorno que facilita el acceso a una atención sanitaria de calidad y a la vanguardia de la innovación tecnológica.
                    """
                )

def data_page():
    if not st.session_state['authenticated']:
        st.warning("Por favor, inicia sesión para acceder a esta página.")
        return
    
    st.title("Sesion")
    st.write("Introduce los datos del paciente y los ejercicios que realiza.")
    
    df_datos_local = load_excel(datos_file, df_datos.columns)
    
    with st.form("exercise_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            nombre = st.text_input("Nombre del Paciente", key="nombre_paciente")
            dni = st.text_input("DNI del Paciente", key="dni_paciente")
            posicion_corporal = st.selectbox("Posición del Cuerpo", df_ejercicios['POSICIÓN CORPORAL'].dropna().unique(), key="posicion_corporal")
        
        nombre_ejercicio = st.selectbox("Nombre del ejercicio", df_ejercicios['NOMBRE EJERCICIO'].dropna().unique(), key="nombre_ejercicio")
        
        with col2:
            repeticiones = st.number_input("Número de Repeticiones", min_value=0, step=1, key="repeticiones")
        
        with col3:
            tiempo = st.number_input("Tiempo (min)", min_value=0, step=1, key="tiempo")
            kilos = st.number_input("Kilos", min_value=0.0, step=0.5, key="kilos")
        
        submit_button = st.form_submit_button(label="Guardar")

    if submit_button:
        fecha = datetime.now().strftime("%Y-%m-%d")
        new_data = pd.DataFrame({
            'Fecha': [fecha],
            'Nombre': [nombre],
            'DNI': [dni],
            'Posición Corporal': [posicion_corporal],
            'Nombre Ejercicio': [nombre_ejercicio],
            'Repeticiones': [repeticiones],
            'Tiempo (min)': [tiempo],
            'Kilos': [kilos]
        })
        df_datos_local = pd.concat([df_datos_local, new_data], ignore_index=True)
        save_to_excel(df_datos_local, datos_file)
        st.success("Datos guardados correctamente.")

def view_data_page():
    if not st.session_state['authenticated']:
        st.warning("Por favor, inicia sesión para acceder a esta página.")
        return

    st.title("Datos Guardados")
    st.write("Introduce el Nombre y DNI del Paciente para acceder a los datos.")
    nombre_input = st.text_input("Nombre del Paciente", key="nombre_input")
    dni_input = st.text_input("DNI del Paciente", key="dni_input")
    if st.button("Ver Datos", key="ver_datos"):
        if validate_credentials(nombre_input, dni_input, df_credenciales):
            df_datos_local = load_excel(datos_file, df_datos.columns)
            datos_filtrados = df_datos_local[(df_datos_local['Nombre'] == nombre_input) & (df_datos_local['DNI'] == dni_input)]
            if not datos_filtrados.empty:
                st.dataframe(datos_filtrados)
            else:
                st.error("No se encontraron datos de este paciente.")
        else:
            st.error("Datos incorrectos. Inténtalo de nuevo.")

def masters_page():
    if not st.session_state['authenticated']:
        st.warning("Por favor, inicia sesión para acceder a esta página.")
        return

    st.title("Gestión de Profesionales y Clientes")
    st.write("Registrar nuevos profesionales y clientes, y gestionar los existentes.")
    
    tab1, tab2 = st.tabs(["Profesionales", "Clientes"])
    
    with tab1:
        st.subheader("Registro de Profesionales")
        
        # Reload df_profesionales to ensure it includes any newly added professionals
        df_profesionales_local = load_excel(profesionales_file, df_profesionales.columns)
        
        # Generate a new unique ID for the professional
        if not df_profesionales_local.empty:
            new_id = df_profesionales_local['ID'].max() + 1
        else:
            new_id = 1
        
        with st.form("professional_form"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("ID de Profesional", value=new_id, disabled=True, key="profesional_id")
                nombre = st.text_input("Nombre", key="profesional_nombre")
                apellidos = st.text_input("Apellidos", key="profesional_apellidos")
                direccion = st.text_input("Dirección", key="profesional_direccion")
                tipo = st.selectbox("Tipo de Profesional", ["Fisioterapeuta", "Recuperador", "Entrenador"], key="profesional_tipo")
            
            with col2:
                dni = st.text_input("DNI", key="profesional_dni")
                telefono = st.text_input("Teléfono", key="profesional_telefono")
                municipio = st.text_input("Municipio", key="profesional_municipio")
                codigo_postal = st.text_input("Código Postal", key="profesional_codigo_postal")
            
            submit_button = st.form_submit_button(label="Registrar Profesional")

        if submit_button:
            new_professional = pd.DataFrame({
                'ID': [new_id],
                'Nombre': [nombre],
                'Apellidos': [apellidos],
                'Direccion': [direccion],
                'DNI': [dni],
                'Telefono': [telefono],
                'Municipio': [municipio],
                'Codigo Postal': [codigo_postal],
                'Tipo': [tipo]
            })
            df_profesionales_local = pd.concat([df_profesionales_local, new_professional], ignore_index=True)
            save_to_excel(df_profesionales_local, profesionales_file)
            st.success("Profesional registrado correctamente.")
        
        st.subheader("Consultar Información de Profesionales")
        professional_id_input = st.text_input("Introduce ID del Profesional", key="consulta_profesional_id")
        
        if st.button("Ver Información de Profesional", key="consulta_profesional_btn"):
            if not professional_id_input:
                st.error("Por favor, introduce un ID de Profesional.")
            else:
                professional_info = df_profesionales_local[df_profesionales_local['ID'] == int(professional_id_input)]
                if not professional_info.empty:
                    st.dataframe(professional_info)
                else:
                    st.error("Profesional no encontrado.")
    
    with tab2:
        st.subheader("Registro de Clientes")
        
        # Reload df_clientes to ensure it includes any newly added clients
        df_clientes_local = load_excel(clientes_file, df_clientes.columns)
        
        # Generate a new unique ID for the client
        if not df_clientes_local.empty:
            new_id = df_clientes_local['ID'].max() + 1
        else:
            new_id = 1
        
        with st.form("client_form"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("ID de Cliente", value=new_id, disabled=True, key="cliente_id")
                nombre = st.text_input("Nombre", key="cliente_nombre")
                apellidos = st.text_input("Apellidos", key="cliente_apellidos")
                direccion = st.text_input("Dirección", key="cliente_direccion")
            
            with col2:
                dni = st.text_input("DNI", key="cliente_dni")
                telefono = st.text_input("Teléfono", key="cliente_telefono")
                municipio = st.text_input("Municipio", key="cliente_municipio")
                codigo_postal = st.text_input("Código Postal", key="cliente_codigo_postal")
            
            submit_button = st.form_submit_button(label="Registrar Cliente")
        
        if submit_button:
            new_client = pd.DataFrame({
                'ID': [new_id],
                'Nombre': [nombre],
                'Apellidos': [apellidos],
                'Direccion': [direccion],
                'DNI': [dni],
                'Telefono': [telefono],
                'Municipio': [municipio],
                'Codigo Postal': [codigo_postal]
            })
            df_clientes_local = pd.concat([df_clientes_local, new_client], ignore_index=True)
            save_to_excel(df_clientes_local, clientes_file)
            st.success("Cliente registrado correctamente.")
        
        st.subheader("Consultar Información de Clientes")
        client_id_input = st.text_input("Introduce ID del Cliente", key="consulta_cliente_id")
        
        if st.button("Ver Información de Cliente", key="consulta_cliente_btn"):
            if not client_id_input:
                st.error("Por favor, introduce un ID de Cliente.")
            else:
                client_info = df_clientes_local[df_clientes_local['ID'] == int(client_id_input)]
                if not client_info.empty:
                    st.dataframe(client_info)
                else:
                    st.error("Cliente no encontrado.")

def analysis_page():
    if not st.session_state['authenticated']:
        st.warning("Por favor, inicia sesión para acceder a esta página.")
        return

    st.title("Análisis de Datos de Pacientes")
    st.write("Explora y analiza los datos de ejercicios de los pacientes.")
    
    df_datos_local = load_excel(datos_file, df_datos.columns)
    
    if not df_datos_local.empty:
        # Utiliza Pygwalker para mostrar el análisis
        pygwalker_html = pyg.walk(df_datos_local)
        st.components.v1.html(pygwalker_html.to_html(), height=800, scrolling=True)
    else:
        st.warning("No hay datos disponibles para su análisis.")

def video_page():
    if not st.session_state['authenticated']:
        st.warning("Por favor, inicia sesión para acceder a esta página.")
        return

    st.title("Video")
    st.write("En esta página analizamos tus movimientos")
    
    st.write("Activando la cámara...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        st.error("No se pudo abrir la cámara.")
        return
    
    stframe = st.empty()
    close_camera = st.sidebar.button("Cerrar Cámara", key="cerrar_camara")

    pose = mp.solutions.pose.Pose(
        min_tracking_confidence=0.5,
        min_detection_confidence=0.5)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Error al capturar el frame de la cámara")
            break
        
        # Convertir la imagen a RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        
        mp.solutions.drawing_utils.draw_landmarks(
            image,
            results.pose_landmarks,
            mp.solutions.pose.POSE_CONNECTIONS,
            mp.solutions.drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
            mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
        
        stframe.image(image, channels="RGB", use_column_width=True)
        
        if close_camera:
            cap.release()
            break

# Display the corresponding page based on menu selection
if selected == "Home":
    home_page()
elif selected == "Data":
    data_page()
elif selected == "View Data":
    view_data_page()
elif selected == "Masters":
    masters_page()
elif selected == "Analysis":
    analysis_page()
elif selected == "Video":
    video_page()
