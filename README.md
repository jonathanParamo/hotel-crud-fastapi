# Sena Hotel Management API

API desarrollada en FastAPI para la gestión básica de un hotel. Incluye manejo de:

- Habitaciones
- Estados de habitaciones (libre, ocupada, mantenimiento)
- Usuarios (root, admin, empleados, clientes)
- CRUD básico sin base de datos (datos quemados)
- Ejecución por Docker / Docker Compose

---

## Tecnologías utilizadas

- **Python 3.10+**
- **FastAPI**
- **Uvicorn**
- **Docker**
- **Docker Compose**

---

## Estructura del proyecto

proyecto/
│── main.py
│── requirements.txt
│── Dockerfile
│── docker-compose.yml
└── README.md

--- yaml

## Cómo correr el proyecto en local

### 1 Crear entorno (opcional)

python3 -m venv venv
source venv/bin/activate

## 2 Instalar dependencias:

pip install -r requirements.txt

## 3 Ejecutar FastAPI

uvicorn main:app --reload

## 4 Abrir en el navegador

http://localhost:8000

### Documentación automática

FastAPI genera documentación interactiva:

Swagger → http://localhost:8000/docs

Redoc → http://localhost:8000/redoc

### Ejemplos de Endpoints

#Listar habitaciones
GET /habitaciones

# Obtener habitación por ID

GET /habitaciones/1

# Cambiar estado de habitación

PUT /habitaciones/{id_h}/estado?nuevo_estado=ocupada

# Crear habitación

POST /habitaciones?id=20&tipo=doble&precio=120000&rol_usuario=admin

```

🐳 Docker y Docker Compose

# Ejecutar con Docker Compose

docker compose up --build

La api queda en: http://localhost:8000

# Notas

Los datos son quemados, no hay base de datos.

Al reiniciar el servidor, todo vuelve a los valores iniciales.

Ideal para prácticas del SENA en desarrollo backend.

### Autor

Jonathan A. Guaydia Páramo.
```
