# PlanIA Edu 🎓🤖

**PlanIA Edu** es un asistente inteligente desarrollado con [Streamlit](https://streamlit.io) que permite a docentes generar planificaciones pedagógicas automatizadas mediante herramientas de inteligencia artificial. Está diseñado para ser útil por docentes de cualquier nivel educativo.

---

## 🧠 ¿Qué hace PlanIA Edu?

- Genera planificaciones pedagógicas interactivas basadas en IA.
- Guarda un historial organizado en formato `.json`.
- Exporta planificaciones en formato PDF.
- Ofrece una interfaz intuitiva, con carga visual optimizada para docentes.

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

Este proyecto está licenciado bajo la [MIT License](LICENSE).

---

## 🤝 Autor

Desarrollado por **Marco Almeida**, con el propósito de apoyar a docentes de todos los niveles educativos en la planificación pedagógica con inteligencia artificial.
