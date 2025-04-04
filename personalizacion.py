import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Mi App Bonita",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado embebido con Google Fonts y animaciones
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;700&family=Pacifico&display=swap');

        html, body, [class*="css"] {
            font-family: 'Raleway', sans-serif;
            background-color: #f0f2f6;
        }

        .titulo {
            font-family: 'Pacifico', cursive;
            font-size: 3rem;
            color: #ff4b4b;
            text-align: center;
            margin-top: 1rem;
            animation: fadeIn 2s ease-in-out;
        }

        .parrafo {
            font-size: 1.2rem;
            color: #444;
            text-align: center;
            margin-bottom: 2rem;
        }

        .respuesta {
            font-size: 1.1rem;
            color: #1a1a1a;
            background-color: #eaffea;
            border-left: 6px solid #3cb371;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }

        .boton-respuesta {
            background-color: #4a90e2;
            color: white;
            padding: 0.7rem;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
            transition: 0.3s;
        }

        .boton-respuesta:hover {
            background-color: #1c6dd0;
            transform: scale(1.05);
        }

        @keyframes fadeIn {
            0% {opacity: 0;}
            100% {opacity: 1;}
        }
    </style>
""", unsafe_allow_html=True)

# Título y descripción
st.markdown("<div class='titulo'>🎨 Mi App Personalizada</div>", unsafe_allow_html=True)
st.markdown("<div class='parrafo'>Con Streamlit + CSS podemos hacer cosas muy cool 😎</div>", unsafe_allow_html=True)

# Entradas con layout
col1, col2 = st.columns([1, 2])
with col1:
    nombre = st.text_input("¿Cómo te llamas?", placeholder="Escribe tu nombre")

with col2:
    color_fav = st.color_picker("Elige tu color favorito", "#ff4b4b")

# Mostrar saludo personalizado
if nombre:
    st.markdown(f"<div class='respuesta'>👋 ¡Hola, <strong>{nombre}</strong>! Gracias por usar la app.</div>", unsafe_allow_html=True)

# Botón con animación
if st.button("Haz clic aquí ✨"):
    st.markdown("<div class='boton-respuesta'>¡Boom! 🎉 Diste clic en el botón animado</div>", unsafe_allow_html=True)

# Footer
st.markdown("<br><hr><p style='text-align: center; font-size: 0.9rem;'>Hecho con 💖 y Streamlit</p>", unsafe_allow_html=True)
