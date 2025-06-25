# PlanIA EDU 🎓🤖

**PlanIA EDU** es un asistente inteligente desarrollado por el **Ing. Marco Almeida Pacheco** con [Streamlit](https://streamlit.io). La aplicación permite a los docentes generar planificaciones pedagógicas automatizadas mediante inteligencia artificial, de forma rápida, ordenada y personalizada.

Este sistema fue creado como parte del trabajo de titulación de la Maestría en Tecnología e Innovación Educativa en la Universidad de Guayaquil, con aplicación inicial en la Facultad de Ciencias de la Salud de la Universidad Católica de Santiago de Guayaquil (UCSG), aunque es adaptable a cualquier institución y nivel educativo.

---

## 🧠 ¿Qué hace PlanIA EDU?

- Genera planificaciones pedagógicas interactivas basadas en IA, adaptadas al contexto de la educación superior en salud, pero aplicables a cualquier nivel educativo.
- Guarda un historial organizado en formato `.json`.
- Exporta planificaciones en formato PDF.
- Ofrece una interfaz intuitiva y amigable, diseñada para facilitar el trabajo docente en cualquier institución.

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

Este proyecto está licenciado bajo la [MIT License](LICENSE). Puedes usarlo, modificarlo y distribuirlo libremente, dando crédito al autor.

---

## 🤝 Autor

Desarrollado por **Ing. Marco Enrique Almeida Pacheco**. Este proyecto está orientado al fortalecimiento de la planificación pedagógica de los docentes de la Facultad de Ciencias de la Salud de la UCSG mediante inteligencia artificial, con posibilidad de uso en distintos niveles e instituciones educativas.
