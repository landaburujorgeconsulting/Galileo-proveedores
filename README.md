# GALILEO – Diagnóstico de Sostenibilidad para Proveedores
### Aplicación web Flask · PDF con ReportLab · Google Drive API

---

## Descripción

Formulario web de diagnóstico ESG con **14 secciones y 60 preguntas** estructuradas bajo normativa GRI 2021, ISO 20400, UNGPs, TCFD, ESRS, ISO 45001 e ISO 14001.

Al enviar el formulario:
- Se genera un **PDF profesional** con todas las respuestas (verde militar, sans-serif).
- El PDF se **sube automáticamente** a la carpeta de Google Drive configurada.
- El PDF **no se descarga** en el dispositivo del respondente.

---

## Estructura del proyecto

```
galileo-esg/
├── app.py              # Aplicación Flask principal (rutas, lógica)
├── form_data.py        # Definición de las 14 secciones y 60 preguntas
├── pdf_generator.py    # Generación del PDF con ReportLab (puro Python)
├── drive_uploader.py   # Subida del PDF a Google Drive
├── templates/
│   ├── form.html       # Formulario web (Jinja2, renderizado desde Python)
│   └── success.html    # Pantalla de confirmación
├── static/
│   └── style.css       # Estilos (verde militar, sans-serif)
├── requirements.txt
├── .env.example        # Plantilla de variables de entorno
└── README.md
```

---

## Instalación rápida

### 1. Clonar / copiar el proyecto

```bash
cd mi-carpeta
# si usás git:
git clone <repositorio> galileo-esg && cd galileo-esg
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Crear el archivo `.env`

```bash
cp .env.example .env
# Editar .env con el editor de tu preferencia
```

---

## Configuración de Google Drive

### Paso 1 – Crear proyecto en Google Cloud Console

1. Ir a https://console.cloud.google.com/
2. Crear un nuevo proyecto (ej: `galileo-esg`).
3. En el menú lateral → **APIs y Servicios** → **Habilitar APIs**.
4. Buscar y habilitar **Google Drive API**.

### Paso 2 – Crear cuenta de servicio (Service Account)

1. En **APIs y Servicios** → **Credenciales** → **Crear credenciales** → **Cuenta de servicio**.
2. Completar nombre (ej: `galileo-drive-uploader`) y hacer clic en **Crear**.
3. No es necesario asignar roles especiales.
4. En la lista de cuentas de servicio, hacer clic en la cuenta creada.
5. Ir a la pestaña **Claves** → **Agregar clave** → **Crear nueva clave** → tipo **JSON**.
6. Se descargará un archivo `.json`. **Renombrarlo a `credentials.json`** y copiarlo a la raíz del proyecto.

### Paso 3 – Compartir la carpeta de Drive con el Service Account

1. Abrir Google Drive en el navegador.
2. Ir a la carpeta donde se guardarán los PDFs (o crearla).
3. Click derecho → **Compartir**.
4. En el campo de correo, pegar el email del Service Account (ej: `galileo-drive-uploader@galileo-esg.iam.gserviceaccount.com`).
5. Darle permiso de **Editor**.
6. Copiar el **ID de la carpeta** desde la URL del navegador:
   ```
   https://drive.google.com/drive/folders/1AbCdEfGhIjKlMnOpQrStUvWx
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   ```
7. Pegar ese ID en el `.env` como `DRIVE_FOLDER_ID`.

### Paso 4 – Completar el `.env`

```env
SECRET_KEY=una-clave-secreta-larga-y-aleatoria
DRIVE_FOLDER_ID=1AbCdEfGhIjKlMnOpQrStUvWx
GOOGLE_CREDENTIALS_PATH=credentials.json
PORT=5000
FLASK_DEBUG=false
SKIP_DRIVE_UPLOAD=false
```

---

## Ejecutar la aplicación

```bash
source venv/bin/activate
python app.py
```

Abrir en el navegador: http://localhost:5000

---

## Probar sin Google Drive

Para probar el formulario y la generación del PDF sin configurar Drive:

```env
SKIP_DRIVE_UPLOAD=true
```

El PDF se generará correctamente en memoria pero no se subirá a ninguna carpeta.

---

## Despliegue en producción

### Opción A – Gunicorn (recomendado)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Opción B – Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Opción C – Render / Railway / Fly.io

Subir el repositorio, configurar las variables de entorno en el panel, y listo.

---

## Seguridad

- Nunca subir `credentials.json` ni `.env` a un repositorio público.
- Agregar ambos al `.gitignore`:
  ```
  .env
  credentials.json
  ```
- En producción, usar HTTPS y una `SECRET_KEY` aleatoria larga.

---

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| Framework web | Python / Flask |
| Template engine | Jinja2 (mínimo HTML, datos desde Python) |
| Generación PDF | Python / ReportLab |
| Subida a Drive | Python / Google Drive API v3 |
| Estilos | CSS (verde militar, sans-serif, sin frameworks) |
| JS | Mínimo inline (solo UX: progress bar, campos condicionales) |

---

Plataforma **GALILEO** · Diagnóstico ESG para Proveedores
