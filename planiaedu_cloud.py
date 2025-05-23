import streamlit as st
import openai
openai.api_key = st.secrets["OPENAI_API_KEY"]
# Verificación temprana de API Key
if not openai.api_key or not openai.api_key.startswith("sk-"):
    st.error("🔐 Error: No se ha configurado correctamente la clave de OpenAI. Por favor, revisa la sección de 'Secrets' en Streamlit Cloud.")
    st.stop()

# Función auxiliar para manejar llamadas seguras a OpenAI
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
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image as ReportLabImage
from PIL import Image
import io
import os
import json
import time

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



# Estado de sesión
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Eres PlanIA Edu, un asistente pedagógico para docentes universitarios."}
    ]
    st.session_state.step = "inicio"
    st.session_state.respuestas = {}
    
def send_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

def finalizar_planificacion():
    nueva_plan = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "datos": st.session_state.respuestas.copy()
    }
    st.session_state.historial_planificaciones.insert(0, nueva_plan)
    st.session_state.respuestas.clear()
    st.session_state.messages = [{"role": "system", "content": "Eres PlanIA Edu..."}]
    st.session_state.step = "inicio"
    
def limpiar_valor(valor):
    valor = str(valor).strip()
    if valor.lower() in ["créalos tú","créalos tu", "crealos tu", "no sé","no se", "ok", "sí", "si", "no", "", " ", "ninguno"]:
        return "No especificado"
    return valor

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

# Paso 0: Saludo e identificación del docente
if step_index == 0:
    st.markdown("👋 ¡Hola! Soy **PlanIA Edu**, tu asistente pedagógico.")
    st.markdown("Voy a ayudarte a planificar tus clases universitarias con inteligencia artificial.")
    st.markdown("¿Cómo te llamas?")
    user_input = st.text_input("Tu nombre")
    if st.button("Comenzar"):
        st.session_state.respuestas["docente_nombre"] = user_input
        send_message("bot", f"¡Bienvenido/a, {user_input}! 🎓")
        send_message("bot", "¿Cuál es la asignatura que imparte?")
        st.session_state.step = "asignatura"
        st.rerun()

# Paso 1: Asignatura
elif step_index == 1:
    st.markdown("🎓 ¿Cuál es la asignatura que imparte?")
    user_input = st.text_input("Asignatura")
    if st.button("Siguiente"):
        st.session_state.respuestas["asignatura"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Sobre qué tema específico trabajará esta clase?")
        st.session_state.step = "tema"
        st.rerun()

# Paso 2: Tema
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

# Paso 3: Duración de la clase
elif step_index == 3:
    user_input = st.text_input("Duración de la clase")
    if st.button("Siguiente"):
        st.session_state.respuestas["duracion_clase"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Cuál es el área de conocimiento?")
        st.markdown("📌 Opciones: Educación, Ciencias de la Salud, Ingeniería y Tecnología, Ciencias Sociales, Artes y Humanidades, Otro")
        st.session_state.step = "area_conocimiento"
        st.rerun()

# Paso 4: Área de conocimiento
elif step_index == 4:
    user_input = st.selectbox("Área de conocimiento", [
        "Educación", "Ciencias de la Salud", "Ingeniería y Tecnología",
        "Ciencias Sociales", "Artes y Humanidades", "Otro"
    ])
    if st.button("Siguiente"):
        st.session_state.respuestas["area_conocimiento"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Cuál es el nivel académico? (Técnico / Pregrado / Posgrado)")
        st.session_state.step = "nivel_academico"
        st.rerun()

# Paso 5: Nivel académico
elif step_index == 5:
    user_input = st.selectbox("Nivel académico", ["Técnico", "Pregrado", "Posgrado"])
    if st.button("Siguiente"):
        st.session_state.respuestas["nivel_academico"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Qué tipo de materia es? (Teórica / Práctica / Mixta)")
        st.session_state.step = "tipo_materia"
        st.rerun()

# Paso 6: Tipo de materia
elif step_index == 6:
    user_input = st.selectbox("Tipo de materia", ["Teórica", "Práctica", "Mixta"])
    if st.button("Siguiente"):
        st.session_state.respuestas["tipo_materia"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Cuál es tu nivel de experiencia docente? (Principiante / Intermedio / Avanzado)")
        st.session_state.step = "experiencia_docente"
        st.rerun()

# Paso 7: Experiencia docente
elif step_index == 7:
    user_input = st.selectbox("Nivel de experiencia docente", ["Principiante", "Intermedio", "Avanzado"])
    if st.button("Siguiente"):
        st.session_state.respuestas["experiencia_docente"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Cómo calificarías tu frecuencia de uso de tecnologías educativas? (Bajo / Medio / Alto)")
        st.session_state.step = "frecuencia_tecno"
        st.rerun()

# Paso 8: Frecuencia de uso de tecnologías educativas
elif step_index == 8:
    user_input = st.selectbox("Frecuencia de uso de tecnologías educativas", ["Bajo", "Medio", "Alto"])
    if st.button("Siguiente"):
        st.session_state.respuestas["frecuencia_tecno"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Qué tipo de clase tienes? (Presencial / Virtual / Híbrida / Semipresencial / A distancia)")
        st.session_state.step = "tipo_clase"
        st.rerun()

# Paso 9: Tipo de clase
elif step_index == 9:
    user_input = st.selectbox("Tipo de clase", [
        "Presencial", "Virtual", "Híbrida", "Semipresencial", "A distancia"
    ])
    if st.button("Siguiente"):
        st.session_state.respuestas["tipo_clase"] = user_input
        send_message("user", user_input)
        send_message("bot", "¿Cuáles son los objetivos de aprendizaje de esta clase?")
        st.markdown("💡 Ejemplo: Al finalizar, los estudiantes deberán ser capaces de...")
        st.markdown("Si necesitas ayuda, dime: 'Créame unos objetivos'")
        st.session_state.step = "objetivos"
        st.rerun()

# Paso 10: Objetivos de aprendizaje
elif step_index == 10:
    user_input = st.text_input("Objetivos de aprendizaje")
    if st.button("Siguiente"):
        asignatura = st.session_state.respuestas.get("asignatura", "")
        tema = st.session_state.respuestas.get("tema", "")

        if user_input.strip().lower() in ["créalos tú","créalos tu", "crealos tu", "no sé","no se", "ok", "sí", "si", "no", "", " ", "ninguno"]:
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
elif step_index == 11:
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

# Paso 12: Herramientas
elif step_index == 12:
    send_message("bot", "¿Te gustaría que te proponga actividades didácticas específicas?")
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

# Paso 13: Actividades
elif step_index == 13:
    send_message("bot", "¿Necesitas guías o tutoriales sobre buenas prácticas éticas al usar IA?")
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

# Paso 14: Recomendaciones finales
elif step_index == 14:
    st.success("✅ ¡Tu planificación está lista!")
    st.subheader("Resumen Final:")

    for key, value in st.session_state.respuestas.items():
        if key == "docente_nombre":
            st.markdown(f"- **Nombre del docente**: {limpiar_valor(value)}")
        else:
            st.markdown(f"- **{key.replace('_', ' ').title()}**: {limpiar_valor(value)}")

    pdf_content = generar_pdf(st.session_state.respuestas)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.download_button(
            label="📄 Descargar planificación en PDF",
            data=pdf_content,
            file_name=f"planificacion_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf"
        )
    with col2:
        if st.button("Guardar y nueva planificación"):
            finalizar_planificacion()
            st.rerun()