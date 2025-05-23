
# PlanIA Edu - Asistente Pedagógico con IA

Este proyecto es una aplicación desarrollada con **Streamlit** que actúa como asistente inteligente para la planificación pedagógica, integrando herramientas de inteligencia artificial.

---

## 🚀 Despliegue en Producción con Streamlit Cloud

### 1. Requisitos previos

- Cuenta en [GitHub](https://github.com)
- Cuenta en [Streamlit Cloud](https://streamlit.io/cloud)
- Clave API de OpenAI

---

### 2. Clona o sube este repositorio a tu cuenta de GitHub

Puedes usar la interfaz de GitHub para crear un nuevo repositorio y subir manualmente los archivos de la carpeta `plania_edu_cloud/`, o clonar directamente:

```bash
git clone https://github.com/tu-usuario/plania-edu.git
```

---

### 3. Conecta tu repositorio en Streamlit Cloud

- Ve a [Streamlit Cloud](https://streamlit.io/cloud)
- Haz clic en **"New app"**
- Selecciona el repositorio: `plania-edu`
- Especifica el archivo principal como: `planiaedu_cloud.py`

---

### 4. Configura tu API Key

En la sección **Settings → Secrets** agrega lo siguiente:

```
OPENAI_API_KEY=tu_clave_personal_de_openai
```

---

### 5. Ejecuta la app

Streamlit lanzará automáticamente la aplicación tras la instalación de dependencias listadas en `requirements.txt`.

---

## 📁 Estructura del proyecto

```
plania_edu_cloud/
│
├── planiaedu_cloud.py           # Archivo principal de la app
├── requirements.txt             # Dependencias
├── historial_planificaciones.json
├── assets/logo.png              # Imagen usada en la app
├── .streamlit/config.toml       # Configuración de interfaz
└── README.md                    # Este documento
```

---

## 🧠 Créditos

Proyecto desarrollado por Marco Almeida Pacheco para fines educativos en el contexto de la Maestría en Tecnología e Innovación Educativa.
