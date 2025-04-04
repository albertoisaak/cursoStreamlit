import streamlit as st
import cv2
import numpy as np
import sqlite3
import qrcode
import io
from PIL import Image



# Crear/conectar la base de datos
conn = sqlite3.connect("accesos.db")
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS accesos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        qr_code TEXT UNIQUE
    )
""")
conn.commit()

# Streamlit App
st.title("🔐 Control de Acceso con QR")

# Sección para generar QR
st.header("📌 Generar Código QR")

nombre = st.text_input("Nombre de la persona:")
if st.button("Generar QR"):
    if nombre:
        qr_code = f"ACCESO-{nombre.upper()}"
        
        # Crear el QR
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_code)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        
        # Guardar en la base de datos
        try:
            cursor.execute("INSERT INTO accesos (nombre, qr_code) VALUES (?, ?)", (nombre, qr_code))
            conn.commit()
            st.success(f"✅ QR generado y guardado para {nombre}")

            # Convertir QR a imagen y mostrar
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.image(buf.getvalue(), caption="Código QR", use_column_width=True)
        except sqlite3.IntegrityError:
            st.error("⚠️ Este usuario ya tiene un QR asignado.")
    else:
        st.warning("⚠️ Ingresa un nombre para generar el QR.")

# Línea divisoria
st.markdown("---")

# Sección para escanear QR
st.header("📸 Escanear Código QR")

uploaded_file = st.file_uploader("📤 Sube una imagen con código QR", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    image = np.array(image)



    # Verificar si la imagen tiene 3 canales (RGB) o 1 canal (Grayscale)
    if len(image.shape) == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    elif len(image.shape) == 2:  # Ya es escala de grises
        gray = image
    else:
        st.error("❌ Formato de imagen no reconocido.")
        st.stop() 


    # Detector de QR
    qr_detector = cv2.QRCodeDetector()
    data, bbox, _ = qr_detector.detectAndDecode(gray)

    if data:
        st.success(f"✅ Código QR detectado: {data}")
        
        # Verificar en la base de datos
        cursor.execute("SELECT nombre FROM accesos WHERE qr_code = ?", (data,))
        resultado = cursor.fetchone()
        
        if resultado:
            st.success(f"🎉 Acceso autorizado para: {resultado[0]}")
        else:
            st.error("🚫 Acceso denegado. QR no registrado.")
    else:
        st.error("❌ No se detectó ningún código QR válido.")

st.title("📷 Lector de QR con Cámara")

# Botón para activar la cámara
start_camera = st.button("Activar Cámara")

if start_camera:
    # Capturar video desde la cámara
    cap = cv2.VideoCapture(1)
    stframe = st.empty()  # Placeholder para mostrar los frames

    # Crear el detector de QR
    qr_detector = cv2.QRCodeDetector()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("No se pudo acceder a la cámara.")
            break

        # Detectar y decodificar QR
        data, bbox, _ = qr_detector.detectAndDecode(frame)

        if bbox is not None:  # Si se detecta un QR
            bbox = bbox.astype(int)  # Convertir las coordenadas a enteros
            for i in range(len(bbox)):
                pt1 = tuple(bbox[i][0])  # Convertir a tupla
                pt2 = tuple(bbox[(i + 1) % len(bbox)][0])  # Convertir a tupla
                cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

            if data:
                st.success(f"QR Detectado: {data}")  # Mostrar el contenido del QR
                break  # Salir del bucle si se detecta un QR válido

        # Mostrar el frame en Streamlit
        stframe.image(frame, channels="BGR")

    # Liberar la cámara
    cap.release()

# Cerrar conexión a la base de datos
conn.close()
