
# Configuración de clave OpenAI 🔐

Para ejecutar correctamente la aplicación **PlanIA Edu**, necesitas una clave de API válida de [OpenAI](https://platform.openai.com/account/api-keys).

---

## 🔧 OPCIÓN 1: Uso local (en tu computadora)

### Paso 1: Instala dependencias

Asegúrate de tener `python-dotenv` si deseas usar el archivo `.env`:

```bash
pip install python-dotenv
```

### Paso 2: Crea el archivo `.env` en la raíz del proyecto

Agrega la siguiente línea (reemplazando con tu propia clave):

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Paso 3: El script ya está configurado para leer esta variable

Gracias a esta línea en el código:

```python
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
```

---

## ☁️ OPCIÓN 2: Uso en Streamlit Cloud

1. Inicia sesión en [https://streamlit.io/cloud](https://streamlit.io/cloud).
2. Ve a tu aplicación desplegada y haz clic en **Settings** > **Secrets**.
3. Agrega tu clave así:

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

4. Listo. La aplicación funcionará automáticamente con la clave protegida.

---

## ⚠️ Seguridad

**No compartas tu clave pública** en redes sociales ni la subas a GitHub. Una clave expuesta puede ser utilizada por terceros para generar costos en tu cuenta.

---

## ❓ ¿Dónde obtengo la clave?

1. Regístrate o inicia sesión en [OpenAI](https://platform.openai.com).
2. Accede a [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys).
3. Haz clic en "Create new secret key".
