"""Script avanzado para poblar la base de datos con datos aleatorios."""
import asyncio
import sys
from pathlib import Path
from faker import Faker
from datetime import datetime, timedelta
import random

root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from app.core.security import get_password_hash
from app.database import AsyncSessionLocal
from app.models.usuario import Usuario
from app.models.campeonato import Campeonato
from app.models.reporte_jugador import ReporteJugador


# Configurar Faker en español
fake = Faker('es_ES')


async def seed_database():
    """Poblar la base de datos con datos aleatorios."""
    async with AsyncSessionLocal() as db:
        try:
            print("🌱 Iniciando seed avanzado con datos aleatorios...")

            # ============================================
            # 1. CREAR CAMPEONATOS
            # ============================================
            print("\n📋 Creando campeonatos...")

            nombres_campeonatos = [
                "Copa San Andrés",
                "Torneo Relámpago",
                "Liga Barrial",
                "Campeonato Intercantonal",
                "Copa de Verano",
                "Torneo de Integración"
            ]

            estados = ["activo", "activo", "activo",
                       "finalizado", "suspendido"]

            campeonatos = []
            for i in range(5):  # 5 campeonatos aleatorios
                nombre_base = random.choice(nombres_campeonatos)
                year = random.randint(2023, 2026)

                # Fechas aleatorias
                fecha_inicio = fake.date_between(
                    start_date='-1y', end_date='today')
                fecha_fin = fecha_inicio + \
                    timedelta(days=random.randint(30, 120))

                campeonato = Campeonato(
                    nombre=f"{nombre_base} {year}",
                    descripcion=fake.text(max_nb_chars=200),
                    fecha_inicio=datetime.combine(
                        fecha_inicio, datetime.min.time()),
                    fecha_fin=datetime.combine(fecha_fin, datetime.min.time()),
                    canton=random.choice(["Píllaro", "Ambato", "Latacunga"]),
                    parroquia=random.choice(
                        ["San Andrés", "Matriz", "La Merced"]),
                    estado=random.choice(estados)
                )
                db.add(campeonato)
                campeonatos.append(campeonato)

            await db.commit()
            for c in campeonatos:
                await db.refresh(c)

            print(f"✅ Creados {len(campeonatos)} campeonatos")

            # ============================================
            # 2. CREAR USUARIOS
            # ============================================
            print("\n⚽ Creando usuarios...")

            roles_distribucion = (
                ["Jugador"] * 15 +  # 15 jugadores
                ["Directivo"] * 3 +  # 3 directivos
                ["DirectivoCampeonato"] * 2 +  # 2 directivos de campeonato
                ["Administrador"] * 1  # 1 admin
            )

            usuarios = []
            cedulas_usadas = set()
            usernames_usados = set()
            emails_usados = set()

            # Crear usuario admin predeterminado
            admin = Usuario(
                nombres="Admin",
                apellidos="Sistema",
                cedula="9999999999",
                username="admin",
                password=get_password_hash("admin123"),
                email="admin@ldpsa.com",
                telefono=fake.phone_number(),
                direction=fake.street_address(),
                canton="Píllaro",
                parroquia="San Andrés",
                barrio=fake.city_suffix(),
                rol="SuperAdministrador"
            )
            db.add(admin)
            usuarios.append(admin)

            cedulas_usadas.add("9999999999")
            usernames_usados.add("admin")
            emails_usados.add("admin@ldpsa.com")

            # Crear usuarios aleatorios
            for rol in roles_distribucion:
                # Generar datos únicos
                while True:
                    cedula = fake.unique.random_number(digits=10, fix_len=True)
                    cedula_str = str(cedula)
                    if cedula_str not in cedulas_usadas:
                        cedulas_usadas.add(cedula_str)
                        break

                nombres = fake.first_name()
                apellidos = f"{fake.last_name()} {fake.last_name()}"

                while True:
                    username = fake.user_name()[:20]
                    if username not in usernames_usados:
                        usernames_usados.add(username)
                        break

                while True:
                    email = fake.email()
                    if email not in emails_usados:
                        emails_usados.add(email)
                        break

                usuario = Usuario(
                    nombres=nombres,
                    apellidos=apellidos,
                    cedula=cedula_str,
                    username=username,
                    # Contraseña por defecto
                    password=get_password_hash("password123"),
                    email=email,
                    telefono=fake.phone_number(),
                    direction=fake.street_address(),
                    canton=random.choice(["Píllaro", "Ambato", "Latacunga"]),
                    parroquia=random.choice(
                        ["San Andrés", "Matriz", "La Merced", "Centro"]),
                    barrio=fake.city_suffix(),
                    rol=rol
                )
                db.add(usuario)
                usuarios.append(usuario)

            await db.commit()
            for u in usuarios:
                await db.refresh(u)

            print(f"✅ Creados {len(usuarios)} usuarios")

            # Separar jugadores
            jugadores = [u for u in usuarios if u.rol == "Jugador"]

            # ============================================
            # 3. CREAR REPORTES DE JUGADORES
            # ============================================
            print("\n📄 Creando reportes de jugadores...")

            tipos_reporte = [
                "Ficha técnica",
                "Informe médico",
                "Evaluación física",
                "Evaluación táctica",
                "Reporte de rendimiento"
            ]

            titulos_base = {
                "Ficha técnica": ["Evaluación Técnica", "Análisis de Habilidades", "Ficha Deportiva"],
                "Informe médico": ["Informe Médico", "Chequeo Médico", "Evaluación de Salud"],
                "Evaluación física": ["Test Físico", "Evaluación de Condición", "Análisis Físico"],
                "Evaluación táctica": ["Análisis Táctico", "Evaluación Táctica", "Revisión Estratégica"],
                "Reporte de rendimiento": ["Informe de Rendimiento", "Análisis de Desempeño", "Estadísticas"]
            }

            reportes = []

            # Crear 2-4 reportes por jugador
            for jugador in jugadores:
                num_reportes = random.randint(2, 4)

                for _ in range(num_reportes):
                    tipo = random.choice(tipos_reporte)
                    titulo_opciones = titulos_base[tipo]
                    titulo = f"{random.choice(titulo_opciones)} - {jugador.nombres} {jugador.apellidos.split()[0]}"

                    reporte = ReporteJugador(
                        jugador_id=jugador.id,
                        campeonato_id=random.choice(campeonatos).id,
                        titulo=titulo,
                        descripcion=fake.text(max_nb_chars=300),
                        tipo_reporte=tipo
                    )
                    db.add(reporte)
                    reportes.append(reporte)

            await db.commit()
            print(f"✅ Creados {len(reportes)} reportes")

            # ============================================
            # RESUMEN FINAL
            # ============================================
            print("\n" + "="*60)
            print("🎉 SEED AVANZADO COMPLETADO EXITOSAMENTE")
            print("="*60)
            print(f"\n📊 Resumen:")
            print(f"   • {len(campeonatos)} Campeonatos")
            print(f"   • {len(usuarios)} Usuarios:")
            print(f"      - {len(jugadores)} Jugadores")
            print(
                f"      - {len([u for u in usuarios if u.rol == 'Directivo'])} Directivos")
            print(
                f"      - {len([u for u in usuarios if u.rol == 'DirectivoCampeonato'])} Directivos de Campeonato")
            print(
                f"      - {len([u for u in usuarios if u.rol in ['Administrador', 'SuperAdministrador']])} Administradores")
            print(f"   • {len(reportes)} Reportes")

            print("\n🔑 Credenciales de acceso:")
            print("   SuperAdmin → username: admin | password: admin123")
            print("   Usuarios → password: password123 (para todos)")
            print(f"\n💡 Algunos usernames de ejemplo:")

            # Mostrar algunos ejemplos de usuarios
            ejemplos_jugadores = [u for u in jugadores[:3]]
            for ej in ejemplos_jugadores:
                print(f"   Jugador → username: {ej.username}")

            admin_ejemplo = next(
                (u for u in usuarios if u.rol == "Administrador"), None)
            if admin_ejemplo:
                print(f"   Admin → username: {admin_ejemplo.username}")

            print("\n✅ Base de datos lista para pruebas")

        except Exception as e:
            print(f"\n❌ Error durante el seed: {str(e)}")
            await db.rollback()
            raise


if __name__ == "__main__":
    print("🚀 Iniciando script de seed avanzado...\n")
    asyncio.run(seed_database())
