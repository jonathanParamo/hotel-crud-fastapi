from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="frontend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datos quemados

usuarios = [
    {"id": 1, "nombre": "root", "rol": "root"},
    {"id": 2, "nombre": "admin1", "rol": "admin"},
    {"id": 3, "nombre": "maria", "rol": "empleada"},
    {"id": 4, "nombre": "ana", "rol": "empleada"},
    {"id": 5, "nombre": "cliente1", "rol": "cliente"},
    {"id": 6, "nombre": "cliente2", "rol": "cliente"},
]

habitaciones = [
    {"id": 101, "tipo": "simple", "precio": 120000, "estado": "libre"},
    {"id": 102, "tipo": "doble", "precio": 160000, "estado": "ocupada"},
    {"id": 103, "tipo": "suite", "precio": 300000, "estado": "mantenimiento"},
    {"id": 104, "tipo": "simple", "precio": 120000, "estado": "ocupada"},
    {"id": 105, "tipo": "suite", "precio": 350000, "estado": "libre"},
]

estados_validos = ["libre", "ocupada", "mantenimiento"]

# endpoints

@app.get("/")
def home():
    return {"message": "API del Hotel funcionando"}


@app.get("/habitaciones")
def listar_habitaciones():
    return habitaciones


@app.get("/habitaciones/{id_h}")
def obtener_habitacion(id_h: int):
    hab = next((h for h in habitaciones if h["id"] == id_h), None)
    if not hab:
        raise HTTPException(404, "Habitación no encontrada")
    return hab


@app.put("/habitaciones/{id_h}/estado")
def cambiar_estado(id_h: int, nuevo_estado: str):
    if nuevo_estado not in estados_validos:
        raise HTTPException(400, "Estado inválido")

    for h in habitaciones:
        if h["id"] == id_h:
            h["estado"] = nuevo_estado
            return {"message": "Estado actualizado", "habitacion": h}

    raise HTTPException(404, "Habitación no encontrada")


@app.post("/habitaciones")
def crear_habitacion(id: int, tipo: str, precio: int, rol_usuario: str):
    if rol_usuario not in ["admin", "root"]:
        raise HTTPException(403, "No tienes permisos para crear habitaciones")

    if any(h["id"] == id for h in habitaciones):
        raise HTTPException(400, "La habitación ya existe")

    nueva = {"id": id, "tipo": tipo, "precio": precio, "estado": "libre"}
    habitaciones.append(nueva)

    return {"message": "Habitación creada", "habitacion": nueva}

@app.patch("/habitaciones/{id_h}")
def actualizar_parcial(id_h: int, tipo: Optional[str] = None, precio: Optional[int] = None, estado: Optional[str] = None):
    hab = next((h for h in habitaciones if h["id"] == id_h), None)

    if not hab:
        raise HTTPException(404, "Habitación no encontrada")

    if estado and estado not in estados_validos:
        raise HTTPException(400, "Estado inválido")

    if tipo:
        hab["tipo"] = tipo
    if precio:
        hab["precio"] = precio
    if estado:
        hab["estado"] = estado

    return {"message": "Cambios aplicados", "habitacion": hab}

@app.get("/usuarios")
def listar_usuarios():
    return usuarios

@app.get("/usuarios/{id_u}")
def obtener_usuario(id_u: int):
    user = next((u for u in usuarios if u["id"] == id_u), None)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    return user

@app.post("/usuarios")
def crear_usuario(id: int, nombre: str, rol: str):
    # validar rol
    roles_validos = ["root", "admin", "empleada", "cliente"]
    if rol not in roles_validos:
        raise HTTPException(400, "Rol inválido")

    if any(u["id"] == id for u in usuarios):
        raise HTTPException(400, "El usuario ya existe")

    nuevo = {"id": id, "nombre": nombre, "rol": rol}
    usuarios.append(nuevo)

    return {"message": "Usuario creado", "usuario": nuevo}

@app.put("/usuarios/{id_u}")
def actualizar_usuario(id_u: int, nombre: str, rol: str):
    user = next((u for u in usuarios if u["id"] == id_u), None)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    roles_validos = ["root", "admin", "empleada", "cliente"]
    if rol not in roles_validos:
        raise HTTPException(400, "Rol inválido")

    user["nombre"] = nombre
    user["rol"] = rol

    return {"message": "Usuario actualizado", "usuario": user}

@app.patch("/usuarios/{id_u}")
def actualizar_usuario_parcial(id_u: int, nombre: Optional[str] = None, rol: Optional[str] = None):
    user = next((u for u in usuarios if u["id"] == id_u), None)
    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    roles_validos = ["root", "admin", "empleada", "cliente"]

    if rol and rol not in roles_validos:
        raise HTTPException(400, "Rol inválido")

    if nombre:
        user["nombre"] = nombre
    if rol:
        user["rol"] = rol

    return {"message": "Cambios aplicados", "usuario": user}

@app.delete("/usuarios/{id_u}")
def eliminar_usuario(id_u: int):
    global usuarios
    user = next((u for u in usuarios if u["id"] == id_u), None)

    if not user:
        raise HTTPException(404, "Usuario no encontrado")

    usuarios = [u for u in usuarios if u["id"] != id_u]

    return {"message": "Usuario eliminado"}
