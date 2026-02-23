"""Script de pruebas QA para la API."""
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.usuario import Usuario
from app.models.campeonato import Campeonato
from app.models.reporte_jugador import ReporteJugador
import asyncio
import sys
from pathlib import Path

# Añadir el directorio raíz al path
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))


async def test_data():
    """Verificar y mostrar datos de prueba."""
    async with AsyncSessionLocal() as db:
        print("🧪 INICIANDO PRUEBAS QA\n")
        print("="*60)

        # Test 1: Contar registros
        print("\n📊 TEST 1: Verificar cantidad de registros")
        print("-"*60)

        campeonatos = (await db.execute(select(Campeonato))).scalars().all()
        usuarios = (await db.execute(select(Usuario))).scalars().all()
        reportes = (await db.execute(select(ReporteJugador))).scalars().all()

        print(f"✓ Campeonatos: {len(campeonatos)}")
        print(f"✓ Usuarios: {len(usuarios)}")
        print(f"✓ Reportes: {len(reportes)}")

        # Test 2: Verificar campeonatos activos
        print("\n🏆 TEST 2: Campeonatos activos")
        print("-"*60)

        activos = [c for c in campeonatos if c.estado == "activo"]
        print(f"Campeonatos activos: {len(activos)}")
        for camp in activos:
            print(f"  • {camp.nombre} - {camp.parroquia}")

        # Test 3: Verificar jugadores por rol
        print("\n⚽ TEST 3: Usuarios por rol")
        print("-"*60)

        roles = {}
        for usuario in usuarios:
            roles[usuario.rol] = roles.get(usuario.rol, 0) + 1

        for rol, count in roles.items():
            print(f"  • {rol}: {count}")

        # Test 4: Reportes por campeonato
        print("\n📄 TEST 4: Reportes por campeonato")
        print("-"*60)

        for camp in campeonatos:
            reportes_camp = [r for r in reportes if r.campeonato_id == camp.id]
            print(f"  • {camp.nombre}: {len(reportes_camp)} reportes")

        # Test 5: Reportes por jugador
        print("\n👤 TEST 5: Top jugadores con más reportes")
        print("-"*60)

        jugadores = [u for u in usuarios if u.rol == "Jugador"]
        jugadores_reportes = []

        for jugador in jugadores:
            reportes_jugador = [
                r for r in reportes if r.jugador_id == jugador.id]
            jugadores_reportes.append((jugador, len(reportes_jugador)))

        jugadores_reportes.sort(key=lambda x: x[1], reverse=True)

        for jugador, count in jugadores_reportes[:5]:
            print(f"  • {jugador.nombres} {jugador.apellidos}: {count} reportes")

        # Test 6: Detalle de un reporte
        print("\n📋 TEST 6: Detalle de reporte de ejemplo")
        print("-"*60)

        if reportes:
            reporte = reportes[0]
            jugador = next(u for u in usuarios if u.id == reporte.jugador_id)
            campeonato = next(c for c in campeonatos if c.id ==
                              reporte.campeonato_id)

            print(f"Título: {reporte.titulo}")
            print(f"Jugador: {jugador.nombres} {jugador.apellidos}")
            print(f"Campeonato: {campeonato.nombre}")
            print(f"Tipo: {reporte.tipo_reporte}")
            print(f"Descripción: {reporte.descripcion[:100]}...")

        # Test 7: Validar integridad referencial
        print("\n🔗 TEST 7: Integridad referencial")
        print("-"*60)

        errores = 0
        for reporte in reportes:
            jugador_existe = any(u.id == reporte.jugador_id for u in usuarios)
            camp_existe = any(
                c.id == reporte.campeonato_id for c in campeonatos)

            if not jugador_existe:
                print(
                    f"❌ Reporte {reporte.id}: Jugador {reporte.jugador_id} no existe")
                errores += 1
            if not camp_existe:
                print(
                    f"❌ Reporte {reporte.id}: Campeonato {reporte.campeonato_id} no existe")
                errores += 1

        if errores == 0:
            print("✓ Todas las referencias son válidas")
        else:
            print(f"❌ {errores} errores de integridad encontrados")

        # Resumen final
        print("\n" + "="*60)
        print("✅ PRUEBAS COMPLETADAS")
        print("="*60)
        print("\n💡 Siguiente paso: Probar endpoints en http://localhost:8000/docs")


if __name__ == "__main__":
    asyncio.run(test_data())
