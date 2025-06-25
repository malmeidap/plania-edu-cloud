# ==============================================================================
# PlanIA Edu – Asistente Pedagógico con Inteligencia Artificial
# Desarrollado por: Ing. Marco Enrique Almeida Pacheco
# Proyecto de titulación de la Maestría en Tecnología e Innovación Educativa
# Universidad de Guayaquil – Facultad de Filosofía
# Fecha de entrega: Junio 2025
# ==============================================================================
# 🔹 Librerías estándar de Python
import os
import io
import json
import time
from datetime import datetime
from re import findall

# 🔸 Librerías externas
import streamlit as st
import openai
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image as ReportLabImage

openai.api_key = st.secrets["OPENAI_API_KEY"]
# Verificación temprana de API Key
if not openai.api_key or not openai.api_key.startswith("sk-"):
    st.error("🔐 Error: No se ha configurado correctamente la clave de OpenAI. Por favor, revisa la sección de 'Secrets' en Streamlit Cloud.")
    st.stop()

# ----------------------------------------------------------------------
# Función: consulta_openai(prompt)
# Descripción: Envía un mensaje (prompt) al modelo GPT-3.5-turbo de OpenAI
#              y devuelve la respuesta generada por la IA.
# Parámetros:
#   - prompt (str): Texto de entrada con la solicitud del usuario.
# Retorna:
#   - str: Contenido de la respuesta generada por la IA.
# ----------------------------------------------------------------------
def consulta_openai(prompt):
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return respuesta.choices[0].message.content.strip()
    except openai.error.AuthenticationError:
        return "⚠️ Error de autenticación con OpenAI. Verifica tu clave API."
    except openai.error.RateLimitError:
        return "⚠️ Se ha superado el límite de uso de la API. Intenta más tarde."
    except openai.error.OpenAIError as e:
        return f"⚠️ Error al conectar con OpenAI: {str(e)}"
    except Exception as e:
        return f"⚠️ Error inesperado: {str(e)}"

# Configuración inicial
st.set_page_config(page_title="PlanIA Edu - Asistente Pedagógico", layout="centered")

# Inyecta estilo CSS personalizado
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
            font-family: 'Segoe UI', sans-serif;
        }
        .chat-message {
            padding: 12px 16px;
            margin: 6px 0;
            border-radius: 10px;
            max-width: 75%;
            line-height: 1.4;
        }
        .user { background-color: #DCF8C6; margin-left: auto; text-align: right; }
        .bot { background-color: #eef2f6; margin-right: auto; text-align: left; }

        .plan-card {
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }

        .btn-plan {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 6px;
            cursor: pointer;
        }

        .btn-plan:hover {
            background-color: #0056b3;
        }

        .header-title {
            font-size: 2rem;
            font-weight: bold;
            color: #1f2937;
            text-align: center;
            margin-bottom: 1rem;
        }

        .sub-header {
            font-size: 1.1rem;
            color: #4b5563;
            text-align: center;
            margin-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Título bonito
st.markdown('<div class="header-title">🧠 PlanIA Edu</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Asistente Pedagógico con Inteligencia Artificial</div>', unsafe_allow_html=True)

# Mostrar introducción animada solo una vez
if "introduccion_completa" not in st.session_state:
    st.markdown(
        """
        <div style="text-align: center; font-size: 24px; color: #333;">
            <strong>Cargando PlanIA Edu...</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)
        time.sleep(0.02)  # Simula progreso lento
    st.empty()
    st.session_state.introduccion_completa = True

# API Key – En producción usa variables de entorno


# Inicializa el estado de la sesión en Streamlit si es la primera vez que se carga la app
# Estado de sesión
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Eres PlanIA Edu, un asistente pedagógico para docentes universitarios."}
    ]
    st.session_state.step = "inicio"
    st.session_state.respuestas = {}
    
# ----------------------------------------------------------------------
# Función: send_message(role, content)
# Descripción: Agrega un mensaje al historial de conversación de la sesión.
# Parámetros:
#   - role (str): Rol del emisor del mensaje ('user' o 'bot').
#   - content (str): Contenido textual del mensaje.
# ----------------------------------------------------------------------
def send_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# ----------------------------------------------------------------------
# Función: finalizar_planificacion()
# Descripción: Cierra el flujo del asistente mostrando un mensaje de éxito
#              y activa la opción para descargar la planificación en PDF.
# ----------------------------------------------------------------------
def finalizar_planificacion():
    st.session_state.respuestas.clear()
    st.session_state.messages = [{"role": "system", "content": "Eres PlanIA Edu, un asistente pedagógico para docentes universitarios."}]
    st.session_state.step = "inicio"
    
def limpiar_valor(valor):
    valor = str(valor).strip()
    if valor.lower() in ["créalos tú","créalos tu", "crealos tu", "no sé","no se", "ok", "sí", "si", "no", "", " ", "ninguno"]:
        return "No especificado"
    return valor

# ----------------------------------------------------------------------
# Función: generar_pdf(respuestas)
# Descripción: Genera un documento PDF con el contenido de una planificación
#              pedagógica, a partir de las respuestas recopiladas por el sistema.
#              Utiliza ReportLab para construir la estructura y formato del documento.
# Parámetros:
#   - respuestas (dict): Diccionario con los campos completados durante el flujo del asistente.
# Retorna:
#   - buffer (BytesIO): Objeto en memoria con el PDF generado listo para descarga.
# ----------------------------------------------------------------------
def generar_pdf(respuestas):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    story = []

    # Estilos personalizados
    styles.add(ParagraphStyle(name='Titulo', fontSize=16, leading=22, textColor="#bd1c35", spaceAfter=10))
    styles.add(ParagraphStyle(name='Subtitulo', fontSize=12, leading=16, textColor="#447ac7", spaceBefore=12, spaceAfter=6))
    styles.add(ParagraphStyle(name='Cuerpo', fontSize=12, leading=18, spaceBefore=6, spaceAfter=12))

    # Agregar logo si existe
    if os.path.exists("assets/logo.png"):
        logo = ReportLabImage("assets/logo.png", width=150, height=60)
        story.append(logo)
        story.append(Spacer(1, 0.3 * inch))

    # Título principal
    story.append(Paragraph("PlanIA Edu - Planificación Pedagógica", styles['Titulo']))
    story.append(Spacer(1, 0.2 * inch))

    # Información general
    story.append(Paragraph("Datos de la planificación:", styles['Subtitulo']))
    datos_principales = {
        "Nombre del docente": respuestas.get('docente_nombre', 'Sin nombre'),
        "Asignatura": respuestas.get('asignatura', 'No especificado'),
        "Tema": respuestas.get('tema', 'No especificado'),
        "Duración": respuestas.get('duracion_clase', 'No especificado')
    }
    for label, val in datos_principales.items():
        story.append(Paragraph(f"<strong>{label}:</strong> {val}", styles['Cuerpo']))

    story.append(Spacer(1, 0.2 * inch))

    # Mapeo de claves a nombres legibles (ya corregidos)
    label_mapping = {
        "area_conocimiento": "Área de conocimiento",
        "nivel_academico": "Nivel académico",
        "tipo_materia": "Tipo de materia",
        "experiencia_docente": "Experiencia docente",
        "frecuencia_tecno": "Frecuencia de uso de tecnologías educativas",
        "tipo_clase": "Tipo de clase",
        "objetivos": "Objetivos de aprendizaje",
        "nivel_tecnologico": "Nivel de conocimientos tecnológicos",
        "herramientas": "Herramientas IA recomendadas",
        "actividades": "Actividades didácticas",
        "recomendaciones": "Recomendaciones éticas"
    }

    # Agregar cada campo al PDF
    from re import findall

    for key, label in label_mapping.items():
        value = limpiar_valor(respuestas.get(key, ""))
        if value == "No especificado":
            continue

        story.append(Paragraph(f"<strong>{label}:</strong>", styles['Subtitulo']))
        lines = value.split('\n')
        for line in lines:
            if line.strip():
                story.append(Paragraph(line.strip(), styles['Cuerpo']))
        story.append(Spacer(1, 0.1 * inch))

    # Tabla de actividades (si existen)
    if "actividades" in respuestas and respuestas["actividades"] != "No especificado":
        story.append(Paragraph("<strong>Bloques de tiempo sugeridos:</strong>", styles['Subtitulo']))
        bloques = []
        bloque_lines = [linea.strip() for linea in respuestas["actividades"].split('\n') if "bloque" in linea.lower()]

        for linea in bloque_lines:
            bloque_match = findall(r"Bloque (\d+).*?(\d+ minutos).*?:.*?(.*)", linea)
            if bloque_match:
                num_bloque, duracion, descripcion = bloque_match[0]
                bloques.append([f"Bloque {num_bloque} ({duracion})", descripcion[:100] + "..."])

        if bloques:
            data = [["Bloque", "Actividad"]]
            data += bloques
            t = Table(data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), "#447ac7"),
                ('TEXTCOLOR', (0, 0), (-1, 0), "#ffffff"),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), "#f9f9f9"),
                ('GRID', (0, 0), (-1, -1), 1, "#cccccc")
            ]))
            story.append(t)
            story.append(Spacer(1, 0.2 * inch))

    # Pie de página
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("<font color='#bcc2d0' size='8'>© PlanIA Edu - Asistente Pedagógico con IA</font>",
                           styles['Normal']))

    # Construir PDF
    
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("<font size='10'>---<br/>Este documento fue generado automáticamente por la herramienta<br/><strong>📘 PlanIA Edu - Asistente Pedagógico con IA</strong><br/>Desarrollado por Marco Almeida Pacheco – 2025</font>", styles['Normal']))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# Mostrar mensajes del chat
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(f'<div class="bot chat-message"><strong>🧠 PlanIA:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "user":
        st.markdown(f'<div class="user chat-message"><strong>👤 Tú:</strong> {msg["content"]}</div>', unsafe_allow_html=True)

# Mostrar historial de planificaciones

# Flujo conversacional
steps = [
    "inicio", "asignatura", "tema", "duracion_clase", 
    "area_conocimiento", "nivel_academico", "tipo_materia",
    "experiencia_docente", "frecuencia_tecno", "tipo_clase", 
    "objetivos", "nivel_tecnologico", "herramientas", "actividades", "recomendaciones"
]

step_index = steps.index(st.session_state.step) if st.session_state.step in steps else 0

# Paso 0: Bienvenida e identificación del docente
# Muestra mensaje inicial, solicita el nombre y configura el siguiente paso tras hacer clic en "Comenzar"
if step_index == 0:
    st.markdown("👋 ¡Hola! Soy **PlanIA Edu**, tu asistente pedagógico.")
    st.markdown("Voy a ayudarte a planificar tus clases universitarias con inteligencia artificial.")
    st.markdown("¿Cómo te llamas?")
    user_input = st.text_input("Tu nombre")

    # Pie de firma institucional (dentro del bloque if)
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; font-size: 13px;'>"
        "Desarrollado por <strong>Ing. Marco Almeida Pacheco</strong> (Junio 2025)<br/>"
        "<em>Trabajo de titulación de la Maestría en Tecnología e Innovación Educativa - Universidad de Guayaquil</em><br/>"
        "<em>Validado en la Facultad de Ciencias de la Salud - UCSG</em>"
        "</div>",
        unsafe_allow_html=True
    )

    if st.button("Comenzar"):
        st.session_state.respuestas["docente_nombre"] = user_input
        send_message("bot", f"¡Bienvenido/a, {user_input}! 🎓")
        send_message("bot", "¿Cuál es la asignatura que imparte?")
        st.session_state.step = "asignatura"
        st.rerun()

# Paso 1: Solicita el nombre de la asignatura que imparte el docente
# Luego avanza al siguiente paso para conocer el objetivo de aprendizaje
elif step_index == 1:
    st.markdown("🎓 ¿Cuál es la asignatura que impartes?")
    user_input = st.text_input("Asignatura")
    if st.button("Siguiente"):
        st.session_state.respuestas["asignatura"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Sobre qué tema específico trabajará esta clase?")
        st.session_state.step = "tema"
        st.rerun()

# Paso 2: Solicita el objetivo de aprendizaje de la clase
# Esta información será utilizada por la IA para contextualizar la planificación
elif step_index == 2:
    st.markdown("📘 ¿Cuál es el tema central de tu clase?")
    st.markdown("💡 Ejemplo: Ecuaciones cuadráticas, Células eucariotas...")
    user_input = st.text_input("Tema de la clase")
    if st.button("Siguiente"):
        st.session_state.respuestas["tema"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Cuánto tiempo durará la clase? Ejemplo: 45 minutos, 1 hora")
        st.session_state.step = "duracion_clase"
        st.rerun()

# Paso 3: Solicita los temas o contenidos que se abordarán en la clase
# Esta información se usará para generar las actividades y materiales pertinentes
elif step_index == 3:
    st.markdown("🕒 ¿Cuánto tiempo durará la clase?")
    st.markdown("💡 Ejemplo: 45 minutos, 90 minutos, 2 horas, ...")
    user_input = st.text_input("Duración de la clase")
    if st.button("Siguiente"):
        st.session_state.respuestas["duracion_clase"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Cuál es el área de conocimiento?")
        st.markdown("📌 Opciones: Educación, Ciencias de la Salud, Ingeniería y Tecnología, Ciencias Sociales, Artes y Humanidades, Otro")
        st.session_state.step = "area_conocimiento"
        st.rerun()

# Paso 4: Selección del área de conocimiento
# Permite contextualizar la planificación según la disciplina académica del docente
elif step_index == 4:
    st.markdown("🎓 Selecciona el área de conocimiento.")
    user_input = st.selectbox("Área de conocimiento", [
        "Educación", "Ciencias de la Salud", "Ingeniería y Tecnología",
        "Ciencias Sociales", "Artes y Humanidades", "Otro"
    ])
    if st.button("Siguiente"):
        st.session_state.respuestas["area_conocimiento"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Cuál es el nivel académico? (Técnico / Pregrado / Posgrado)")
        st.markdown("📘 **Guía:** Selecciona el nivel educativo al que está dirigida esta clase:")
        st.markdown("- **Técnico**: Programas de formación técnica profesional o tecnológica.")
        st.markdown("- **Pregrado**: Carreras universitarias como licenciaturas e ingenierías.")
        st.markdown("- **Posgrado**: Maestrías, especializaciones y doctorados.")
        st.session_state.step = "nivel_academico"
        st.rerun()



# Paso 5: Selección del nivel académico
# Define el nivel educativo al que está dirigida la planificación (ej. pregrado, posgrado)
elif step_index == 5:
    st.markdown("💡 Selecciona el nivel académico que corresponde con la planificación de tu clase.")
    user_input = st.selectbox("Nivel académico", ["Técnico", "Pregrado", "Grado", "Posgrado"])
    if st.button("Siguiente"):
        st.session_state.respuestas["nivel_academico"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Qué tipo de materia es? (Teórica / Práctica / Mixta)")
        st.session_state.step = "tipo_materia"
        st.rerun()

# Paso 6: Tipo de materia (teórica, práctica o mixta)
# Permite adaptar la planificación según la naturaleza del enfoque pedagógico de la clase
elif step_index == 6:
    st.markdown("📘 Selecciona si tu clase es de tipo teórico, práctico o una combinación de ambos.")
    st.markdown("🔎 **Teórica**: Clases centradas en el desarrollo conceptual, fundamentación académica y exposición de contenidos.")
    st.markdown("🔬 **Práctica**: Clases orientadas a la aplicación directa, ejercicios, laboratorios o simulaciones.")
    st.markdown("⚖️ **Mixta**: Combina exposición teórica con actividades prácticas complementarias.")
    user_input = st.selectbox("Tipo de materia", ["Teórica", "Práctica", "Mixta"])
    if st.button("Siguiente"):
        st.session_state.respuestas["tipo_materia"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Cuál es tu nivel de experiencia docente? (Principiante / Intermedio / Avanzado)")
        st.session_state.step = "experiencia_docente"
        st.rerun()

# Paso 7: Nivel de experiencia docente
# Recoge la trayectoria profesional del usuario como docente para ajustar el enfoque de la planificación
elif step_index == 7:
    st.markdown("🧑‍🏫 Selecciona el nivel que más se ajuste a tu trayectoria como docente.")
    st.markdown("🧾 Principiante: <1 año | Intermedio: 1-10 años | Avanzado: >10 años")
    user_input = st.selectbox("Nivel de experiencia docente", ["Principiante", "Intermedio", "Avanzado"])
    if st.button("Siguiente"):
        st.session_state.respuestas["experiencia_docente"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Cómo calificarías tu frecuencia de uso de tecnologías educativas? (Bajo / Medio / Alto)")
        st.session_state.step = "frecuencia_tecno"
        st.rerun()

# Paso 8: Frecuencia de uso de tecnologías educativas
# Recoge el nivel de familiaridad del docente con herramientas digitales para adaptar la planificación
elif step_index == 8:
    st.markdown("💡 Señala con qué frecuencia utilizas herramientas digitales o plataformas educativas.")
    st.markdown("📶 Bajo: Uso ocasional | Medio: Uso regular | Alto: Uso intensivo o cotidiano")
    user_input = st.selectbox("Frecuencia de uso de tecnologías educativas", ["Bajo", "Medio", "Alto"])
    if st.button("Siguiente"):
        st.session_state.respuestas["frecuencia_tecno"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Qué tipo de clase tienes? (Presencial / Virtual / Híbrida / Semipresencial / A distancia)")
        st.session_state.step = "tipo_clase"
        st.rerun()

# Paso 9: Tipo de clase
# Permite identificar la modalidad de enseñanza (presencial, virtual, híbrida, etc.) para contextualizar la planificación
elif step_index == 9:
    st.markdown("🏫 Selecciona la modalidad que corresponde al entorno en que impartes tu clase.")
    st.markdown("📚 Presencial: En aula física | Virtual: Completamente en línea | Híbrida: Combina presencial y virtual | Semipresencial: Mayormente presencial, algunas sesiones virtuales | A distancia: Sincrónica o asincrónica, sin presencia física")
    user_input = st.selectbox("Tipo de clase", [
        "Presencial", "Virtual", "Híbrida", "Semipresencial", "A distancia"
    ])
    if st.button("Siguiente"):
        st.session_state.respuestas["tipo_clase"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Cuáles son los objetivos de aprendizaje de esta clase?")
        st.markdown("✏️ Puedes redactar tus propios objetivos o dejar que el asistente los proponga automáticamente.")
        st.markdown("🧠 Si escribes frases como **'créalos tú'**, **'sugiérelos'**, o incluso lo dejas vacío, PlanIA Edu generará objetivos pedagógicos adecuados para tu asignatura.")
        st.markdown("💡 Ejemplo de objetivo redactado: 'Al finalizar la clase, los estudiantes deberán ser capaces de resolver funciones lógicas aplicadas en programación.'")
        st.session_state.step = "objetivos"
        st.rerun()


# Paso 10: Objetivos de aprendizaje
# El docente puede ingresar sus objetivos o solicitar que la IA los genere automáticamente según la asignatura y el tema.
# Se procesan expresiones comunes que indican delegación al asistente (ej. "sugiérelos", "créalos tú", etc.).
elif step_index == 10:
    st.markdown("🎯 Escribe tus objetivos o deja que el asistente los genere automáticamente.")
    st.markdown("📌 Si escribes frases como 'créalos tú', 'sugiérelos' o dejas el campo vacío, se generarán sugerencias.")
    st.markdown("💡 Ejemplo: 'Al finalizar la clase, los estudiantes deberán ser capaces de analizar textos científicos en inglés técnico.'")
    user_input = st.text_input("Objetivos de aprendizaje")
    if st.button("Siguiente"):
        asignatura = st.session_state.respuestas.get("asignatura", "")
        tema = st.session_state.respuestas.get("tema", "")

        if user_input.strip().lower() in ["créalos tú","sugiérelos", "créalos tu", "crealos tu", "crealos tú", "no sé","no se", "ok", "sí", "si", "no", "", " ", "ninguno"]:
            prompt = f"Sugiere 3 objetivos claros para una clase de '{asignatura}' sobre '{tema}', nivel universitario."
            try:
                obj_ia = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
                user_input = obj_ia.choices[0].message.content.strip()
            except Exception as e:
                user_input = "1. Comprender el concepto de ecuación cuadrática.\n2. Aplicar métodos de resolución paso a paso.\n3. Graficar funciones y analizar resultados."

        st.session_state.respuestas["objetivos"] = user_input.strip()
        send_message("user", user_input)
        send_message("bot", "¿Cómo calificarías tu nivel de familiaridad con herramientas digitales? (Bajo / Medio / Alto)")
        st.session_state.step = "nivel_tecnologico"
        st.rerun()

# Paso 11: Nivel de conocimientos tecnológicos
# Permite evaluar el dominio del docente sobre tecnologías digitales aplicadas a la enseñanza.
# A partir de esta información, la IA sugiere 3 herramientas educativas adecuadas al contexto del usuario.
elif step_index == 11:
    st.markdown("💻 Selecciona tu nivel de dominio de tecnologías digitales aplicadas a la docencia.")
    st.markdown("🔍 Bajo: Conocimientos básicos | Medio: Uso habitual de plataformas | Alto: Dominio de herramientas avanzadas")
    user_input = st.selectbox("Nivel de conocimientos tecnológicos", ["Bajo", "Medio", "Alto"])
    if st.button("Siguiente"):
        st.session_state.respuestas["nivel_tecnologico"] = user_input
        send_message("user", user_input)

        # Generar herramientas con IA
        prompt = f"""
        Sugiere 3 herramientas de IA educativa adecuadas para una clase de '{st.session_state.respuestas.get("asignatura", "")}'
        sobre '{st.session_state.respuestas.get("tema", "")}', tipo de clase '{st.session_state.respuestas.get("tipo_clase", "")}',
        nivel tecnológico '{st.session_state.respuestas.get("nivel_tecnologico", "")}'
        """
        try:
            respuesta_ia = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
            herramientas = respuesta_ia.choices[0].message.content.strip()
        except Exception as e:
            herramientas = "⚠️ Error al conectar con OpenAI."

        st.session_state.respuestas["herramientas"] = herramientas
        send_message("bot", herramientas)
        st.session_state.step = "herramientas"
        st.rerun()

# Paso 12: Generación de actividades didácticas con IA
# El docente decide si desea recibir sugerencias automáticas. Si responde "sí", la IA propone actividades
# estructuradas por bloques de tiempo usando las herramientas tecnológicas disponibles y los objetivos definidos.
elif step_index == 12:
    send_message("bot", "¿Deseas que el asistente proponga actividades didácticas basadas en IA?")
    st.markdown("🛠️ Decide si deseas que el asistente proponga actividades didácticas personalizadas usando IA.")
    st.markdown("✅ Escribe **sí** si deseas sugerencias automáticas, o **no** si prefieres proponerlas tú mismo.")
    user_input = st.text_input("¿Deseas actividades?")
    if st.button("Siguiente"):
        send_message("user", user_input)
        herramientas = st.session_state.respuestas.get("herramientas", "")
        objetivo = st.session_state.respuestas.get("objetivos", "enseñar conceptos básicos")
        duracion = st.session_state.respuestas.get("duracion_clase", "1 hora")

        prompt = f"""
        Propon 2 o 3 actividades didácticas usando {herramientas} para lograr estos objetivos:
        {objetivo}

        La clase tiene una duración total de {duracion}.
        Divide el tiempo en bloques claros y sugiere cómo distribuirlos.
        Usa formato: 'Bloque X (Y minutos): Descripción breve'
        """
        try:
            respuesta_ia = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
            actividades = respuesta_ia.choices[0].message.content.strip()
        except Exception as e:
            actividades = "⚠️ Error al generar actividades."

        st.session_state.respuestas["actividades"] = actividades
        send_message("bot", actividades)
        st.session_state.step = "actividades"
        st.rerun()

# Paso 13: Recomendaciones éticas sobre el uso de IA
# El docente decide si desea recibir sugerencias de buenas prácticas éticas. Si responde "sí", la IA
# proporciona 3 recomendaciones para aplicar la inteligencia artificial de manera responsable en el aula.
elif step_index == 13:
    send_message("bot", "📘 Las buenas prácticas éticas al usar IA ayudan a garantizar una educación responsable.")
    st.markdown("📘 Las buenas prácticas éticas al usar IA ayudan a garantizar una educación responsable.")
    st.markdown("🧭 Elige si deseas recibir sugerencias éticas para aplicar la inteligencia artificial en tu clase.")
    st.markdown("✅ Escribe **sí** para recibirlas automáticamente, o **no** si prefieres omitirlas.")
    user_input = st.text_input("¿Deseas recomendaciones éticas?")
    if st.button("Finalizar"):
        send_message("user", user_input)
        prompt = "¿Cuáles son 3 buenas prácticas éticas al usar IA en la educación universitaria?"
        try:
            respuesta_ia = openai.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
            recomendaciones = respuesta_ia.choices[0].message.content.strip()
        except Exception as e:
            recomendaciones = "⚠️ Error al obtener recomendaciones éticas."

        st.session_state.respuestas["recomendaciones"] = recomendaciones
        send_message("bot", recomendaciones)
        st.session_state.step = "recomendaciones"
        st.rerun()

# Paso 14: Recomendaciones finales y descarga del PDF
# Muestra el resumen completo de la planificación generada, permite descargar el documento en PDF
# y ofrece la opción de iniciar una nueva planificación docente.
elif step_index == 14:
    st.success("✅ ¡Tu planificación está lista!")
    st.subheader("Resumen Final:")

    for key, value in st.session_state.respuestas.items():
        if key == "docente_nombre":
            st.markdown(f"- **Nombre del docente**: {limpiar_valor(value)}")
        else:
            st.markdown(f"- **{key.replace('_', ' ').title()}**: {limpiar_valor(value)}")

    pdf_content = generar_pdf(st.session_state.respuestas)

    st.markdown("💾 **Antes de continuar, asegúrate de descargar tu planificación en PDF.**")
    st.markdown("_Este documento no se guarda automáticamente. Si deseas iniciar otra planificación, puedes hacerlo después de descargar._")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.download_button(
            label="📄 Descargar planificación en PDF",
            data=pdf_content,
            file_name=f"planificacion_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf"
        )
    with col2:
        if st.button("🆕 Generar nueva planificación"):
            finalizar_planificacion()
            st.rerun()
# Desarrollado por Ing. Marco Enrique Almeida Pacheco – Junio 2025
