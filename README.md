
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
git clone https://github.com/malmeidap/plania-edu.git
cd plania-edu
```

### 2. Instala los requisitos

Se recomienda usar un entorno virtual (opcional):

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Ejecuta la aplicación

```bash
streamlit run planiaedu.py
```

---

## ☁️ Despliegue en Streamlit Cloud

1. Sube este repositorio a tu cuenta de GitHub.
2. Ve a [https://streamlit.io/cloud](https://streamlit.io/cloud) y haz login con GitHub.
3. Selecciona el repositorio `plania-edu`.
4. Configura el archivo principal como: `planiaedu.py`.
5. ¡Tu aplicación estará disponible con una URL pública!

---

## 📁 Estructura del proyecto

```
plania-edu/
│
├── assets/
│   └── logo.png
├── historial_planificaciones.json
├── planiaedu.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── config.toml
```

---

## 🧾 Requisitos

- Python 3.8 o superior
- Librerías:
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
