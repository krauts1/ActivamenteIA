# 📄 ActivaMente AI Assistant

Este proyecto es un asistente de conocimiento que utiliza **RAG (Retrieval-Augmented Generation)** para responder preguntas sobre datos personalizados y permite ejecutar acciones a través de herramientas integradas.  
Incluye un **backend en FastAPI** y un **frontend en React**.

---

## 🚀 Características
- Subida de archivos PDF, TXT, CSV y Markdown.
- Procesamiento e indexación en una base de datos.
- Búsqueda semántica usando embeddings.
- Interfaz sencilla de chat para consultas.
- API documentada con Swagger.

---

## 📦 Tecnologías
**Backend**
- Python 3.11
- FastAPI
- Docker
- OpenAI API (embeddings)
- SQLAlchemy

**Frontend**
- React + Vite
- TypeScript
- Axios

---

## ⚙️ Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/activamente-ai.git
cd activamente-ai
```

### 2. Configurar el Backend
```bash
cd backend
cp .env.example .env
```
Edita el archivo .env con tus credenciales y configuración (API keys, rutas, etc.).

Luego instala dependencias y levanta el contenedor:
```bash
docker-compose up --build
```

Esto levantará la API en:
```bash
http://localhost:8000
```

### 3. Configurar el Frontend

```bash
cd frontend
cp .env.example .env
```

Edita el archivo .env para apuntar a la URL de tu backend, por ejemplo:
```bash
VITE_API_URL=http://localhost:8000
```

Instala las dependencias y levanta el servidor de desarrollo:
```bash
npm install
npm run dev
```

##📌 Uso

- Sube un archivo en el frontend.
- El backend lo procesa e indexa.
- Haz preguntas en el chat y el sistema buscará respuestas basadas en el contenido subido.

##🛠 Notas

El backend y frontend pueden correr en servidores separados, pero recuerda configurar CORS correctamente.

Puedes usar cualquier proveedor de embeddings compatible (por defecto OpenAI).
