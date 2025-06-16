
# PlanIA EDU 🎓🤖

**PlanIA EDU** es un asistente inteligente desarrollado con [Streamlit](https://streamlit.io) que permite a los docentes de la Facultad de Ciencias de la Salud de la Universidad Católica de Santiago de Guayaquil (UCSG) generar planificaciones pedagógicas automatizadas mediante herramientas de inteligencia artificial. Este sistema fue diseñado y validado en el marco de mi trabajo de titulación de maestría en Tecnología e Innovación Educativa, con el propósito de fortalecer la planificación docente universitaria a través de soluciones tecnológicas contextualizadas.

---

## 🧠 ¿Qué hace PlanIA EDU?

- Genera planificaciones pedagógicas interactivas basadas en IA, adaptadas al contexto de la educación superior en salud.
- Guarda un historial organizado en formato `.json`.
- Exporta planificaciones en formato PDF.
- Ofrece una interfaz intuitiva y amigable, diseñada específicamente para docentes universitarios de la UCSG.

---

## 🚀 Cómo ejecutar esta app

### 1. Clona este repositorio

```bash
git clone https://github.com/malmeidap/plania-edu-cloud.git
cd plania-edu-cloud

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

streamlit run planiaedu_cloud.py
```

---

## 📁 Estructura del proyecto

```
plania-edu-cloud/
│
├── assets/
│   └── logo.png
├── historial_planificaciones.json
├── planiaedu_cloud.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml
```

---

## 🧾 Requisitos

- Python 3.8 o superior
- Librerías necesarias:
  - `streamlit`
  - `openai`
  - `reportlab`
  - `Pillow`

---

## 📄 Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE). El desarrollo forma parte de mi trabajo de titulación de la Maestría en Tecnología e Innovación Educativa de la Universidad de Guayaquil.

---

## 🤝 Autor

Desarrollado por **Ing. Marco Enrique Almeida Pacheco**, como parte de mi trabajo de titulación para optar al grado de Magíster en Tecnología e Innovación Educativa en la Universidad de Guayaquil. Este proyecto está orientado al fortalecimiento de la planificación pedagógica de los docentes de la Facultad de Ciencias de la Salud de la UCSG mediante inteligencia artificial.
