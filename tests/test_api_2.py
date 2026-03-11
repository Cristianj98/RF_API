"""Script de testing negativo automatico para la API de Campeonatos."""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Credenciales
ADMIN = {"username": "andresreyna", "password": "password123"}
JUGADOR = {"username": "jose72", "password": "password123"}

# Colores para la consola
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

resultados = []


def log(nombre, response, esperado):
    """Registra el resultado de un test."""
    status = response.status_code
    ok = status == esperado
    color = GREEN if ok else RED
    simbolo = "✅" if ok else "❌"

    print(f"  {simbolo} {color}{nombre}{RESET}")
    print(f"     Esperado: {esperado} | Obtenido: {status}")

    if not ok:
        try:
            detalle = response.json()
            print(f"     Respuesta: {json.dumps(detalle, ensure_ascii=False)}")
        except Exception:
            print(f"     Respuesta raw: {response.text[:200]}")

    resultados.append({
        "test": nombre,
        "esperado": esperado,
        "obtenido": status,
        "ok": ok
    })


def get_token(username, password):
    """Obtiene token JWT."""
    r = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": username, "password": password}
    )
    if r.status_code == 200:
        return r.json().get("access_token")
    return None


def headers(token):
    return {"Authorization": f"Bearer {token}"}


# ─────────────────────────────────────────────
print(f"\n{BOLD}{BLUE}{'='*55}{RESET}")
print(f"{BOLD}{BLUE}   TEST SUITE - API Campeonatos de Fútbol{RESET}")
print(f"{BOLD}{BLUE}{'='*55}{RESET}\n")

# ─────────────────────────────────────────────
print(f"{BOLD}🔐 [1] AUTENTICACIÓN{RESET}")

# Login correcto admin
r = requests.post(f"{BASE_URL}/auth/login", data=ADMIN)
log("Login admin válido", r, 200)
token_admin = r.json().get("access_token") if r.status_code == 200 else None

# Login correcto jugador
r = requests.post(f"{BASE_URL}/auth/login", data=JUGADOR)
log("Login jugador válido", r, 200)
token_jugador = r.json().get("access_token") if r.status_code == 200 else None

# Usuario no existe
r = requests.post(f"{BASE_URL}/auth/login",
                  data={"username": "noexiste123", "password": "pass"})
log("Login usuario inexistente", r, 401)

# Contraseña incorrecta
r = requests.post(f"{BASE_URL}/auth/login",
                  data={"username": ADMIN["username"], "password": "incorrecta"})
log("Login contraseña incorrecta", r, 401)

# Sin token
r = requests.get(f"{BASE_URL}/auth/me")
log("GET /auth/me sin token", r, 401)

# Token falso
r = requests.get(f"{BASE_URL}/auth/me",
                 headers={"Authorization": "Bearer tokenfalsoxyz123"})
log("GET /auth/me con token falso", r, 401)

# Token malformado
r = requests.get(f"{BASE_URL}/auth/me",
                 headers={"Authorization": "tokensinbearer"})
log("GET /auth/me token malformado", r, 401)

# ─────────────────────────────────────────────
print(f"\n{BOLD}👤 [2] USUARIOS{RESET}")

if token_admin:
    # Crear usuario con email inválido
    r = requests.post(f"{BASE_URL}/usuarios/", headers=headers(token_admin), json={
        "nombres": "Test", "apellidos": "User", "cedula": "9999999999",
        "username": "testuser99", "password": "pass123",
        "email": "emailinvalido", "rol": "Jugador"
    })
    log("Crear usuario con email inválido", r, 422)

    # Crear usuario sin campos obligatorios
    r = requests.post(f"{BASE_URL}/usuarios/", headers=headers(token_admin), json={
        "nombres": "Solo nombre"
    })
    log("Crear usuario sin campos obligatorios", r, 422)

    # Obtener usuario inexistente
    r = requests.get(f"{BASE_URL}/usuarios/99999",
                     headers=headers(token_admin))
    log("GET usuario inexistente (ID 99999)", r, 404)

    # Jugador intenta crear usuario (sin permisos)
    if token_jugador:
        r = requests.post(f"{BASE_URL}/usuarios/", headers=headers(token_jugador), json={
            "nombres": "Hack", "apellidos": "Attempt", "cedula": "1111111111",
            "username": "hackuser", "password": "hack123",
            "email": "hack@test.com", "rol": "Administrador"
        })
        log("Jugador intenta crear usuario (sin permisos)", r, 403)

    # Jugador intenta editar otro usuario
    if token_jugador:
        r = requests.put(f"{BASE_URL}/usuarios/1", headers=headers(token_jugador), json={
            "nombres": "Editado sin permiso"
        })
        log("Jugador edita otro usuario (sin permisos)", r, 403)

# ─────────────────────────────────────────────
print(f"\n{BOLD}🏆 [3] CAMPEONATOS{RESET}")

if token_admin:
    # Obtener campeonato inexistente
    r = requests.get(f"{BASE_URL}/campeonatos/99999",
                     headers=headers(token_admin))
    log("GET campeonato inexistente", r, 404)

    # Jugador intenta crear campeonato
    if token_jugador:
        r = requests.post(f"{BASE_URL}/campeonatos/", headers=headers(token_jugador), json={
            "nombre": "Campeonato Hack", "estado": "activo"
        })
        log("Jugador intenta crear campeonato (sin permisos)", r, 403)

    # Crear campeonato sin nombre
    r = requests.post(f"{BASE_URL}/campeonatos/", headers=headers(token_admin), json={
        "descripcion": "Sin nombre este campeonato"
    })
    log("Crear campeonato sin nombre", r, 422)

    # Eliminar campeonato inexistente
    r = requests.delete(f"{BASE_URL}/campeonatos/99999",
                        headers=headers(token_admin))
    log("DELETE campeonato inexistente", r, 404)

# ─────────────────────────────────────────────
print(f"\n{BOLD}⚽ [4] EQUIPOS{RESET}")

if token_admin:
    # Crear equipo con campeonato inexistente
    r = requests.post(f"{BASE_URL}/equipos/", headers=headers(token_admin), json={
        "nombre": "Equipo Fantasma", "campeonato_id": 99999
    })
    log("Crear equipo con campeonato inexistente", r, 404)

    # Obtener equipo inexistente
    r = requests.get(f"{BASE_URL}/equipos/99999", headers=headers(token_admin))
    log("GET equipo inexistente", r, 404)

    # Jugador intenta crear equipo
    if token_jugador:
        r = requests.post(f"{BASE_URL}/equipos/", headers=headers(token_jugador), json={
            "nombre": "Equipo Hack", "campeonato_id": 1
        })
        log("Jugador intenta crear equipo (sin permisos)", r, 403)

    # Sin token intenta listar equipos
    r = requests.get(f"{BASE_URL}/equipos/")
    log("GET equipos sin token", r, 401)

# ─────────────────────────────────────────────
print(f"\n{BOLD}👥 [5] JUGADORES EN EQUIPOS{RESET}")

if token_admin:
    # Asignar jugador a equipo inexistente
    r = requests.post(f"{BASE_URL}/jugadores-equipos/", headers=headers(token_admin), json={
        "usuario_id": 1, "equipo_id": 99999
    })
    log("Asignar jugador a equipo inexistente", r, 404)

    # Asignar usuario inexistente como jugador
    r = requests.post(f"{BASE_URL}/jugadores-equipos/", headers=headers(token_admin), json={
        "usuario_id": 99999, "equipo_id": 1
    })
    log("Asignar usuario inexistente como jugador", r, 404)

    # Asignar admin como jugador (rol incorrecto)
    r = requests.post(f"{BASE_URL}/jugadores-equipos/", headers=headers(token_admin), json={
        "usuario_id": 1, "equipo_id": 1
    })
    log("Asignar usuario con rol incorrecto como jugador", r, 400)

    # Jugador intenta asignar jugadores
    if token_jugador:
        r = requests.post(f"{BASE_URL}/jugadores-equipos/", headers=headers(token_jugador), json={
            "usuario_id": 1, "equipo_id": 1
        })
        log("Jugador intenta asignar jugadores (sin permisos)", r, 403)

# ─────────────────────────────────────────────
print(f"\n{BOLD}🏛️ [6] DIRECTIVA DE EQUIPOS{RESET}")

if token_admin:
    # Asignar directivo a equipo inexistente
    r = requests.post(f"{BASE_URL}/directiva-equipos/", headers=headers(token_admin), json={
        "usuario_id": 1, "equipo_id": 99999, "subrol": "Presidente"
    })
    log("Asignar directivo a equipo inexistente", r, 404)

    # Subrol inválido
    r = requests.post(f"{BASE_URL}/directiva-equipos/", headers=headers(token_admin), json={
        "usuario_id": 1, "equipo_id": 1, "subrol": "RolInvalido"
    })
    log("Asignar directivo con subrol inválido", r, 422)

    # Asignar usuario inexistente como directivo
    r = requests.post(f"{BASE_URL}/directiva-equipos/", headers=headers(token_admin), json={
        "usuario_id": 99999, "equipo_id": 1, "subrol": "Presidente"
    })
    log("Asignar usuario inexistente como directivo", r, 404)

# ─────────────────────────────────────────────
# RESUMEN FINAL
total = len(resultados)
passed = sum(1 for r in resultados if r["ok"])
failed = total - passed

print(f"\n{BOLD}{BLUE}{'='*55}{RESET}")
print(f"{BOLD}📊 RESUMEN FINAL{RESET}")
print(f"{BOLD}{BLUE}{'='*55}{RESET}")
print(f"  Total tests : {total}")
print(f"  {GREEN}Pasaron    : {passed} ✅{RESET}")
print(f"  {RED}Fallaron   : {failed} ❌{RESET}")
print(f"  Cobertura  : {(passed/total*100):.1f}%\n")

if failed > 0:
    print(f"{BOLD}{RED}Tests fallidos:{RESET}")
    for r in resultados:
        if not r["ok"]:
            print(f"  ❌ {r['test']}")
            print(f"     Esperado {r['esperado']} → Obtenido {r['obtenido']}")
    print()

print(f"{BOLD}{BLUE}{'='*55}{RESET}\n")
