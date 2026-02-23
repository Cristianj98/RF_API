"""Script de pruebas completo para todos los CRUDs."""
import asyncio
import sys
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from app.models.reporte_jugador import ReporteJugador
from app.models.campeonato import Campeonato
from app.models.usuario import Usuario
from app.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class TestResult:
    """Clase para manejar resultados de pruebas."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def add_pass(self, test_name):
        self.passed += 1
        print(f"  ✅ {test_name}")

    def add_fail(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"  ❌ {test_name}: {error}")

    def summary(self):
        total = self.passed + self.failed
        print("\n" + "="*70)
        print(f"🧪 RESUMEN DE PRUEBAS")
        print("="*70)
        print(
            f"Total: {total} | ✅ Pasadas: {self.passed} | ❌ Fallidas: {self.failed}")

        if self.failed > 0:
            print("\n❌ Errores encontrados:")
            for test, error in self.errors:
                print(f"  • {test}: {error}")
        else:
            print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")


async def test_usuarios_crud(db: AsyncSession, results: TestResult):
    """Pruebas CRUD de Usuarios."""
    print("\n👤 PRUEBAS CRUD - USUARIOS")
    print("-"*70)

    # TEST 1: Listar usuarios
    try:
        result = await db.execute(select(Usuario))
        usuarios = result.scalars().all()
        assert len(usuarios) > 0, "No hay usuarios en la BD"
        results.add_pass(f"Listar usuarios ({len(usuarios)} encontrados)")
    except Exception as e:
        results.add_fail("Listar usuarios", str(e))

    # TEST 2: Buscar usuario específico por ID
    try:
        result = await db.execute(select(Usuario).where(Usuario.id == 1))
        usuario = result.scalar_one_or_none()
        assert usuario is not None, "Usuario ID=1 no encontrado"
        assert usuario.nombres is not None, "Usuario sin nombre"
        results.add_pass(f"Buscar usuario por ID (ID=1: {usuario.nombres})")
    except Exception as e:
        results.add_fail("Buscar usuario por ID", str(e))

    # TEST 3: Buscar usuario por username
    try:
        result = await db.execute(select(Usuario).where(Usuario.username == "juanperez"))
        usuario = result.scalar_one_or_none()
        assert usuario is not None, "Usuario 'juanperez' no encontrado"
        results.add_pass(f"Buscar por username (juanperez)")
    except Exception as e:
        results.add_fail("Buscar usuario por username", str(e))

    # TEST 4: Validar campos únicos
    try:
        result = await db.execute(select(Usuario))
        usuarios = result.scalars().all()

        cedulas = [u.cedula for u in usuarios]
        usernames = [u.username for u in usuarios]
        emails = [u.email for u in usuarios]

        assert len(cedulas) == len(set(cedulas)), "Hay cédulas duplicadas"
        assert len(usernames) == len(
            set(usernames)), "Hay usernames duplicados"
        assert len(emails) == len(set(emails)), "Hay emails duplicados"

        results.add_pass(
            "Validar unicidad de campos (cedula, username, email)")
    except Exception as e:
        results.add_fail("Validar unicidad de campos", str(e))

    # TEST 5: Validar roles
    try:
        result = await db.execute(select(Usuario))
        usuarios = result.scalars().all()

        roles_validos = ["Jugador", "Directivo",
                         "DirectivoCampeonato", "Administrador", "SuperAdministrador"]
        roles_encontrados = set([u.rol for u in usuarios])

        for rol in roles_encontrados:
            assert rol in roles_validos, f"Rol inválido: {rol}"

        results.add_pass(
            f"Validar roles ({len(roles_encontrados)} roles diferentes)")
    except Exception as e:
        results.add_fail("Validar roles", str(e))

    # TEST 6: Contar jugadores
    try:
        result = await db.execute(select(Usuario).where(Usuario.rol == "Jugador"))
        jugadores = result.scalars().all()
        assert len(jugadores) > 0, "No hay jugadores en la BD"
        results.add_pass(f"Contar jugadores ({len(jugadores)} jugadores)")
    except Exception as e:
        results.add_fail("Contar jugadores", str(e))


async def test_campeonatos_crud(db: AsyncSession, results: TestResult):
    """Pruebas CRUD de Campeonatos."""
    print("\n🏆 PRUEBAS CRUD - CAMPEONATOS")
    print("-"*70)

    # TEST 1: Listar campeonatos
    try:
        result = await db.execute(select(Campeonato))
        campeonatos = result.scalars().all()
        assert len(campeonatos) > 0, "No hay campeonatos en la BD"
        results.add_pass(
            f"Listar campeonatos ({len(campeonatos)} encontrados)")
    except Exception as e:
        results.add_fail("Listar campeonatos", str(e))

    # TEST 2: Buscar campeonato por ID
    try:
        result = await db.execute(select(Campeonato).where(Campeonato.id == 3))
        campeonato = result.scalar_one_or_none()
        assert campeonato is not None, "Campeonato ID=3 no encontrado"
        results.add_pass(
            f"Buscar campeonato por ID (ID=3: {campeonato.nombre})")
    except Exception as e:
        results.add_fail("Buscar campeonato por ID", str(e))

    # TEST 3: Filtrar campeonatos activos
    try:
        result = await db.execute(select(Campeonato).where(Campeonato.estado == "activo"))
        activos = result.scalars().all()
        assert len(activos) > 0, "No hay campeonatos activos"
        results.add_pass(
            f"Filtrar campeonatos activos ({len(activos)} activos)")
    except Exception as e:
        results.add_fail("Filtrar campeonatos activos", str(e))

    # TEST 4: Filtrar campeonatos finalizados
    try:
        result = await db.execute(select(Campeonato).where(Campeonato.estado == "finalizado"))
        finalizados = result.scalars().all()
        results.add_pass(
            f"Filtrar campeonatos finalizados ({len(finalizados)} finalizados)")
    except Exception as e:
        results.add_fail("Filtrar campeonatos finalizados", str(e))

    # TEST 5: Validar nombres únicos
    try:
        result = await db.execute(select(Campeonato))
        campeonatos = result.scalars().all()
        nombres = [c.nombre for c in campeonatos]
        assert len(nombres) == len(
            set(nombres)), "Hay nombres de campeonatos duplicados"
        results.add_pass("Validar unicidad de nombres")
    except Exception as e:
        results.add_fail("Validar unicidad de nombres", str(e))

    # TEST 6: Validar estados válidos
    try:
        result = await db.execute(select(Campeonato))
        campeonatos = result.scalars().all()

        estados_validos = ["activo", "finalizado", "suspendido"]
        for camp in campeonatos:
            assert camp.estado in estados_validos, f"Estado inválido: {camp.estado}"

        results.add_pass("Validar estados de campeonatos")
    except Exception as e:
        results.add_fail("Validar estados de campeonatos", str(e))


async def test_reportes_crud(db: AsyncSession, results: TestResult):
    """Pruebas CRUD de Reportes de Jugadores."""
    print("\n📄 PRUEBAS CRUD - REPORTES DE JUGADORES")
    print("-"*70)

    # TEST 1: Listar reportes
    try:
        result = await db.execute(select(ReporteJugador))
        reportes = result.scalars().all()
        assert len(reportes) > 0, "No hay reportes en la BD"
        results.add_pass(f"Listar reportes ({len(reportes)} encontrados)")
    except Exception as e:
        results.add_fail("Listar reportes", str(e))

    # TEST 2: Buscar reporte por ID
    try:
        result = await db.execute(select(ReporteJugador).where(ReporteJugador.id == 1))
        reporte = result.scalar_one_or_none()
        assert reporte is not None, "Reporte ID=1 no encontrado"
        results.add_pass(f"Buscar reporte por ID (ID=1: {reporte.titulo})")
    except Exception as e:
        results.add_fail("Buscar reporte por ID", str(e))

    # TEST 3: Filtrar reportes por jugador
    try:
        result = await db.execute(select(ReporteJugador).where(ReporteJugador.jugador_id == 1))
        reportes_jugador = result.scalars().all()
        assert len(reportes_jugador) > 0, "No hay reportes para el jugador ID=1"
        results.add_pass(
            f"Filtrar por jugador (Jugador ID=1: {len(reportes_jugador)} reportes)")
    except Exception as e:
        results.add_fail("Filtrar reportes por jugador", str(e))

    # TEST 4: Filtrar reportes por campeonato
    try:
        result = await db.execute(select(ReporteJugador).where(ReporteJugador.campeonato_id == 3))
        reportes_camp = result.scalars().all()
        assert len(reportes_camp) > 0, "No hay reportes para el campeonato ID=3"
        results.add_pass(
            f"Filtrar por campeonato (Campeonato ID=3: {len(reportes_camp)} reportes)")
    except Exception as e:
        results.add_fail("Filtrar reportes por campeonato", str(e))

    # TEST 5: Validar integridad referencial - Jugadores
    try:
        result = await db.execute(select(ReporteJugador))
        reportes = result.scalars().all()

        jugadores_result = await db.execute(select(Usuario.id))
        jugadores_ids = set([id[0] for id in jugadores_result.all()])

        for reporte in reportes:
            assert reporte.jugador_id in jugadores_ids, f"Jugador ID={reporte.jugador_id} no existe"

        results.add_pass("Validar integridad referencial (jugadores)")
    except Exception as e:
        results.add_fail("Validar integridad referencial (jugadores)", str(e))

    # TEST 6: Validar integridad referencial - Campeonatos
    try:
        result = await db.execute(select(ReporteJugador))
        reportes = result.scalars().all()

        campeonatos_result = await db.execute(select(Campeonato.id))
        campeonatos_ids = set([id[0] for id in campeonatos_result.all()])

        for reporte in reportes:
            assert reporte.campeonato_id in campeonatos_ids, f"Campeonato ID={reporte.campeonato_id} no existe"

        results.add_pass("Validar integridad referencial (campeonatos)")
    except Exception as e:
        results.add_fail(
            "Validar integridad referencial (campeonatos)", str(e))

    # TEST 7: Validar tipos de reporte
    try:
        result = await db.execute(select(ReporteJugador))
        reportes = result.scalars().all()

        tipos_encontrados = set(
            [r.tipo_reporte for r in reportes if r.tipo_reporte])
        results.add_pass(
            f"Tipos de reporte encontrados: {', '.join(tipos_encontrados)}")
    except Exception as e:
        results.add_fail("Validar tipos de reporte", str(e))


async def test_relaciones(db: AsyncSession, results: TestResult):
    """Pruebas de relaciones entre tablas."""
    print("\n🔗 PRUEBAS DE RELACIONES")
    print("-"*70)

    # TEST 1: Relación Jugador -> Reportes
    try:
        result = await db.execute(select(Usuario).where(Usuario.id == 1))
        jugador = result.scalar_one_or_none()

        reportes_result = await db.execute(
            select(ReporteJugador).where(
                ReporteJugador.jugador_id == jugador.id)
        )
        reportes = reportes_result.scalars().all()

        results.add_pass(
            f"Jugador {jugador.nombres} tiene {len(reportes)} reportes")
    except Exception as e:
        results.add_fail("Relación Jugador -> Reportes", str(e))

    # TEST 2: Relación Campeonato -> Reportes
    try:
        result = await db.execute(select(Campeonato).where(Campeonato.id == 3))
        campeonato = result.scalar_one_or_none()

        reportes_result = await db.execute(
            select(ReporteJugador).where(
                ReporteJugador.campeonato_id == campeonato.id)
        )
        reportes = reportes_result.scalars().all()

        results.add_pass(
            f"Campeonato '{campeonato.nombre}' tiene {len(reportes)} reportes")
    except Exception as e:
        results.add_fail("Relación Campeonato -> Reportes", str(e))

    # TEST 3: Contar reportes por jugador
    try:
        jugadores_result = await db.execute(select(Usuario).where(Usuario.rol == "Jugador"))
        jugadores = jugadores_result.scalars().all()

        jugador_con_mas_reportes = None
        max_reportes = 0

        for jugador in jugadores:
            reportes_result = await db.execute(
                select(ReporteJugador).where(
                    ReporteJugador.jugador_id == jugador.id)
            )
            count = len(reportes_result.scalars().all())

            if count > max_reportes:
                max_reportes = count
                jugador_con_mas_reportes = jugador

        if jugador_con_mas_reportes:
            results.add_pass(
                f"Jugador con más reportes: {jugador_con_mas_reportes.nombres} ({max_reportes} reportes)"
            )
        else:
            results.add_fail("Contar reportes por jugador",
                             "No hay jugadores con reportes")
    except Exception as e:
        results.add_fail("Contar reportes por jugador", str(e))


async def test_data_integrity(db: AsyncSession, results: TestResult):
    """Pruebas de integridad de datos."""
    print("\n🛡️ PRUEBAS DE INTEGRIDAD DE DATOS")
    print("-"*70)

    # TEST 1: Campos obligatorios en Usuarios
    try:
        result = await db.execute(select(Usuario))
        usuarios = result.scalars().all()

        for usuario in usuarios:
            assert usuario.nombres, f"Usuario ID={usuario.id} sin nombre"
            assert usuario.apellidos, f"Usuario ID={usuario.id} sin apellidos"
            assert usuario.cedula, f"Usuario ID={usuario.id} sin cédula"
            assert usuario.username, f"Usuario ID={usuario.id} sin username"
            assert usuario.email, f"Usuario ID={usuario.id} sin email"
            assert usuario.rol, f"Usuario ID={usuario.id} sin rol"

        results.add_pass(
            f"Campos obligatorios en Usuarios ({len(usuarios)} validados)")
    except Exception as e:
        results.add_fail("Campos obligatorios en Usuarios", str(e))

    # TEST 2: Campos obligatorios en Campeonatos
    try:
        result = await db.execute(select(Campeonato))
        campeonatos = result.scalars().all()

        for camp in campeonatos:
            assert camp.nombre, f"Campeonato ID={camp.id} sin nombre"
            assert camp.estado, f"Campeonato ID={camp.id} sin estado"

        results.add_pass(
            f"Campos obligatorios en Campeonatos ({len(campeonatos)} validados)")
    except Exception as e:
        results.add_fail("Campos obligatorios en Campeonatos", str(e))

    # TEST 3: Campos obligatorios en Reportes
    try:
        result = await db.execute(select(ReporteJugador))
        reportes = result.scalars().all()

        for reporte in reportes:
            assert reporte.jugador_id, f"Reporte ID={reporte.id} sin jugador_id"
            assert reporte.campeonato_id, f"Reporte ID={reporte.id} sin campeonato_id"
            assert reporte.titulo, f"Reporte ID={reporte.id} sin título"

        results.add_pass(
            f"Campos obligatorios en Reportes ({len(reportes)} validados)")
    except Exception as e:
        results.add_fail("Campos obligatorios en Reportes", str(e))

    # TEST 4: Timestamps
    try:
        result = await db.execute(select(Usuario))
        usuarios = result.scalars().all()

        for usuario in usuarios:
            assert usuario.created_at, f"Usuario ID={usuario.id} sin created_at"
            assert usuario.updated_at, f"Usuario ID={usuario.id} sin updated_at"

        results.add_pass("Validar timestamps (created_at, updated_at)")
    except Exception as e:
        results.add_fail("Validar timestamps", str(e))


async def run_all_tests():
    """Ejecutar todas las pruebas."""
    print("="*70)
    print("🧪 INICIANDO SUITE COMPLETA DE PRUEBAS QA")
    print("="*70)

    results = TestResult()

    async with AsyncSessionLocal() as db:
        await test_usuarios_crud(db, results)
        await test_campeonatos_crud(db, results)
        await test_reportes_crud(db, results)
        await test_relaciones(db, results)
        await test_data_integrity(db, results)

    results.summary()

    return results.failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
