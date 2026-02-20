"""Script para poblar la base de datos con datos de prueba."""
import asyncio
import sys
from pathlib import Path

# Añadir el directorio raíz al path
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from app.models.reporte_jugador import ReporteJugador
from app.models.campeonato import Campeonato
from app.models.usuario import Usuario
from app.database import AsyncSessionLocal


async def seed_database():
    """Poblar la base de datos con datos de prueba."""
    async with AsyncSessionLocal() as db:
        try:
            print("🌱 Iniciando seed de base de datos...")

            # ============================================
            # 1. CREAR CAMPEONATOS
            # ============================================
            print("\n📋 Creando campeonatos...")
            campeonatos_data = [
                {
                    "nombre": "Copa San Andrés 2026",
                    "descripcion": "Torneo anual de fútbol amateur",
                    "canton": "Píllaro",
                    "parroquia": "San Andrés",
                    "estado": "activo"
                },
                {
                    "nombre": "Torneo Relámpago Píllaro",
                    "descripcion": "Campeonato corto de fin de semana",
                    "canton": "Píllaro",
                    "parroquia": "San Andrés",
                    "estado": "activo"
                },
                {
                    "nombre": "Liga Barrial 2025",
                    "descripcion": "Campeonato inter-barrios finalizado",
                    "canton": "Píllaro",
                    "parroquia": "San Andrés",
                    "estado": "finalizado"
                }
            ]

            campeonatos = []
            for data in campeonatos_data:
                campeonato = Campeonato(**data)
                db.add(campeonato)
                campeonatos.append(campeonato)

            await db.commit()
            print(f"✅ Creados {len(campeonatos)} campeonatos")

            # ============================================
            # 2. CREAR USUARIOS (JUGADORES Y DIRECTIVOS)
            # ============================================
            print("\n⚽ Creando usuarios...")
            usuarios_data = [
                # Jugadores
                {
                    "nombres": "Juan Carlos",
                    "apellidos": "Pérez López",
                    "cedula": "1804567890",
                    "username": "juanperez",
                    "password": "password123",
                    "email": "juan.perez@email.com",
                    "telefono": "0987654321",
                    "direction": "Barrio Centro",
                    "canton": "Píllaro",
                    "parroquia": "San Andrés",
                    "barrio": "Centro",
                    "rol": "Jugador"
                },
                {
                    "nombres": "María Fernanda",
                    "apellidos": "García Torres",
                    "cedula": "1805678901",
                    "username": "mariagarcia",
                    "password": "password123",
                    "email": "maria.garcia@email.com",
                    "telefono": "0987654322",
                    "direction": "Barrio San José",
                    "canton": "Píllaro",
                    "parroquia": "San Andrés",
                    "barrio": "San José",
                    "rol": "Jugador"
                },
                {
                    "nombres": "Luis Alberto",
                    "apellidos": "Sánchez Ruiz",
                    "cedula": "1806789012",
                    "username": "luissanchez",
                    "password": "password123",
                    "email": "luis.sanchez@email.com",
                    "telefono": "0987654323",
                    "direction": "Barrio La Cruz",
                    "canton": "Píllaro",
                    "parroquia": "San Andrés",
                    "barrio": "La Cruz",
                    "rol": "Jugador"
                },
                {
                    "nombres": "Ana Patricia",
                    "apellidos": "Martínez Díaz",
                    "cedula": "1807890123",
                    "username": "anamartinez",
                    "password": "password123",
                    "email": "ana.martinez@email.com",
                    "telefono": "0987654324",
                    "direction": "Barrio El Rosario",
                    "canton": "Píllaro",
                    "parroquia": "San Andrés",
                    "barrio": "El Rosario",
                    "rol": "Jugador"
                },
                {
                    "nombres": "Carlos Andrés",
                    "apellidos": "Rodríguez Vega",
                    "cedula": "1808901234",
                    "username": "carlosrodriguez",
                    "password": "password123",
                    "email": "carlos.rodriguez@email.com",
                    "telefono": "0987654325",
                    "direction": "Barrio La Libertad",
                    "canton": "Píllaro",
                    "parroquia": "San Andrés",
                    "barrio": "La Libertad",
                    "rol": "Jugador"
                },
                # Directivos
                {
                    "nombres": "Roberto Carlos",
                    "apellidos": "Flores Mendoza",
                    "cedula": "1809012345",
                    "username": "robertoflores",
                    "password": "password123",
                    "email": "roberto.flores@email.com",
                    "telefono": "0987654326",
                    "direction": "Barrio Centro",
                    "canton": "Píllaro",
                    "parroquia": "San Andrés",
                    "barrio": "Centro",
                    "rol": "Directivo"
                },
                {
                    "nombres": "Patricia Elena",
                    "apellidos": "Castro Morales",
                    "cedula": "1800123456",
                    "username": "patriciacastro",
                    "password": "password123",
                    "email": "patricia.castro@email.com",
                    "telefono": "0987654327",
                    "direction": "Barrio San José",
                    "canton": "Píllaro",
                    "parroquia": "San Andrés",
                    "barrio": "San José",
                    "rol": "DirectivoCampeonato"
                },
                {
                    "nombres": "Jorge Luis",
                    "apellidos": "Ramírez Silva",
                    "cedula": "1801234567",
                    "username": "jorgeramirez",
                    "password": "password123",
                    "email": "jorge.ramirez@email.com",
                    "telefono": "0987654328",
                    "direction": "Barrio La Cruz",
                    "canton": "Píllaro",
                    "parroquia": "San Andrés",
                    "barrio": "La Cruz",
                    "rol": "Administrador"
                }
            ]

            usuarios = []
            for data in usuarios_data:
                usuario = Usuario(**data)
                db.add(usuario)
                usuarios.append(usuario)

            await db.commit()

            # Refrescar para obtener IDs
            for usuario in usuarios:
                await db.refresh(usuario)

            print(f"✅ Creados {len(usuarios)} usuarios")

            # Separar jugadores de otros roles
            jugadores = [u for u in usuarios if u.rol == "Jugador"]

            # ============================================
            # 3. CREAR REPORTES DE JUGADORES
            # ============================================
            print("\n📄 Creando reportes de jugadores...")
            reportes_data = [
                {
                    "jugador_id": jugadores[0].id,
                    "campeonato_id": campeonatos[0].id,
                    "titulo": "Evaluación Técnica - Juan Pérez",
                    "descripcion": "Jugador destacado en el mediocampo. Excelente visión de juego y pases precisos. Recomendado para posición de volante central.",
                    "tipo_reporte": "Ficha técnica"
                },
                {
                    "jugador_id": jugadores[1].id,
                    "campeonato_id": campeonatos[0].id,
                    "titulo": "Informe Médico - María García",
                    "descripcion": "Recuperación exitosa de lesión en tobillo izquierdo. Apta para entrenamientos completos. Seguimiento en 2 semanas.",
                    "tipo_reporte": "Informe médico"
                },
                {
                    "jugador_id": jugadores[2].id,
                    "campeonato_id": campeonatos[0].id,
                    "titulo": "Evaluación Física - Luis Sánchez",
                    "descripcion": "Excelente condición física. Velocidad destacada en sprints de 40m. Resistencia aeróbica por encima del promedio del equipo.",
                    "tipo_reporte": "Evaluación física"
                },
                {
                    "jugador_id": jugadores[0].id,
                    "campeonato_id": campeonatos[1].id,
                    "titulo": "Reporte de Rendimiento - Torneo Relámpago",
                    "descripcion": "3 goles y 2 asistencias en 5 partidos. MVP del torneo. Liderazgo en cancha notable.",
                    "tipo_reporte": "Evaluación"
                },
                {
                    "jugador_id": jugadores[3].id,
                    "campeonato_id": campeonatos[0].id,
                    "titulo": "Evaluación Táctica - Ana Martínez",
                    "descripcion": "Buena comprensión táctica. Destaca en marcaje y anticipación. Sugerencia: trabajar salida con balón desde defensa.",
                    "tipo_reporte": "Ficha técnica"
                },
                {
                    "jugador_id": jugadores[4].id,
                    "campeonato_id": campeonatos[2].id,
                    "titulo": "Informe Final - Liga Barrial",
                    "descripcion": "Torneo completado. 8 goles, 4 asistencias. Goleador del equipo. Comportamiento ejemplar dentro y fuera de la cancha.",
                    "tipo_reporte": "Evaluación"
                }
            ]

            reportes = []
            for data in reportes_data:
                reporte = ReporteJugador(**data)
                db.add(reporte)
                reportes.append(reporte)

            await db.commit()
            print(f"✅ Creados {len(reportes)} reportes")

            # ============================================
            # RESUMEN FINAL
            # ============================================
            print("\n" + "="*50)
            print("🎉 SEED COMPLETADO EXITOSAMENTE")
            print("="*50)
            print(f"\n📊 Resumen:")
            print(f"   • {len(campeonatos)} Campeonatos")
            print(f"   • {len(usuarios)} Usuarios ({len(jugadores)} jugadores)")
            print(f"   • {len(reportes)} Reportes")

            print("\n🔑 Credenciales de prueba:")
            print("   Username: juanperez | Password: password123")
            print("   Username: mariagarcia | Password: password123")

            print("\n✅ Base de datos lista para pruebas")

        except Exception as e:
            print(f"\n❌ Error durante el seed: {str(e)}")
            await db.rollback()
            raise


if __name__ == "__main__":
    print("🚀 Iniciando script de seed...\n")
    asyncio.run(seed_database())
