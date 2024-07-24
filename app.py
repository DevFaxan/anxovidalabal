import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu

# Función para validar credenciales
def validate_login(username, password):
    # Leer el archivo Excel con las credenciales
    credentials_df = pd.read_excel("admin_credentials.xlsx")
    # Comprobar si las credenciales son válidas
    if ((credentials_df['username'] == username) & (credentials_df['password'] == password)).any():
        return True
    return False

# Definir la página principal
def main_page():
    st.title("Welcome to the Home Page")
    st.write("This is the home section of the Streamlit app. You can find general information and updates here.")

def projects_page():
    st.title("Projects Overview")
    st.write("Here you can find information about various projects.")
    
    st.subheader("Project 1: Data Analysis")
    st.write("Description of Project 1...")
    
    st.subheader("Project 2: Machine Learning")
    st.write("Description of Project 2...")

def hr_analytics_page():
    st.title("HR Analytics Dashboard")
    st.write("Welcome to the HR Analytics section. Here you can find various insights and metrics related to human resources.")
    
    st.subheader("Employee Satisfaction")
    st.write("Details about employee satisfaction metrics...")
    
    st.subheader("Attrition Rate")
    st.write("Details about employee attrition rates...")
    
    st.subheader("Download Excel Template")
    with open("template.xlsx", "rb") as file:
        btn = st.download_button(
            label="Download Excel template",
            data=file,
            file_name="template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    st.subheader("Upload Completed Excel File for Analysis")
    uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "csv"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.write("DataFrame:")
            st.dataframe(df)
            
            st.subheader("PyGWalker Analysis")
            pyg_html = pyg.walk(df, env='Streamlit', return_html=True)
            components.html(pyg_html, scrolling=True, height=600)
        except Exception as e:
            st.error(f"Error loading or processing the file: {e}")

def finance_page():
    st.title("Finance Dashboard")
    st.write("Welcome to the Finance section. Here you can find financial metrics and insights.")
    
    st.subheader("Financial Performance")
    st.write("Details about financial performance metrics...")

def students_page():
    st.title("Students Dashboard")
    st.write("Welcome to the Students section. Please log in to access student metrics and insights.")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if validate_login(username, password):  # Lógica de autenticación básica
            st.session_state.logged_in = True
            st.experimental_rerun()  # Recargar la página para reflejar el estado de inicio de sesión
        else:
            st.error("Invalid username or password")

def students_dashboard():
    st.title("Student Performance Dashboard")
    st.write("Details about student performance metrics...")

def contact_page():
    st.title("Contact Us")
    st.write("Feel free to reach out to us through the following methods:")
    
    st.subheader("Email")
    st.write("contact@example.com")
    
    st.subheader("Phone")
    st.write("+123 456 7890")
    
    st.subheader("Address")
    st.write("123 Main Street, City, Country")

# Inicializar el estado de inicio de sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "Projects", "HR Analytics", "Finance", "Students", "Contact"],
        icons=["house", "book", "person", "coin", "table", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

# Mostrar la página correspondiente según la selección del menú y el estado de inicio de sesión
if selected == "Home":
    main_page()
elif selected == "Projects":
    projects_page()
elif selected == "HR Analytics":
    hr_analytics_page()
elif selected == "Finance":
    finance_page()
elif selected == "Students":
    if st.session_state.logged_in:
        students_dashboard()
    else:
        students_page()
elif selected == "Contact":
    contact_page()









