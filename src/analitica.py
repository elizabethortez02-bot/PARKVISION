# PARKVISION UNIVERSITY
# Modulo de analitica y Smart Assistant
# Responsable: Erick

import gestion as g
from estadisticas import calcular_estadisticas


def generar_alertas(online, disponibles, espera, incidentes, vencidas):
    alertas = []

    if not online:
        alertas.append("Cámara desconectada: accesos suspendidos")
    elif disponibles == 0:
        alertas.append("Sin cupos directos: utilice la fila virtual")
    elif disponibles == 1:
        alertas.append("Demanda alta: queda un cupo directo")
    else:
        alertas.append("Disponibilidad normal")

    if espera > 0:
        alertas.append(f"Usuarios en espera: {espera}")

    if incidentes > 0:
        alertas.append(f"Revisar {incidentes} incidentes pendientes")

    if vencidas > 0:
        alertas.append(f"Reservaciones vencidas registradas: {vencidas}")

    return alertas


def resumen(c, online):
    # Capacidad actual del estacionamiento
    spaces, free, holds, available = g.capacity(c)

    # Reutilizar el modulo de estadisticas anterior
    estados = [bool(s["occupied"]) for s in spaces]
    estadisticas = calcular_estadisticas(estados)

    # Visitas finalizadas
    completed = g.val(
        c,
        """SELECT COUNT(*) FROM visits
        WHERE status = 'closed'
        AND parked IS NOT NULL""",
    )

    # Tiempo promedio desde entrada hasta salida
    avg = g.val(
        c,
        """SELECT COALESCE(AVG(exited - entered), 0)
        FROM visits
        WHERE status = 'closed'
        AND parked IS NOT NULL
        AND exited >= entered""",
    )

    # Rotacion de los seis espacios
    counts = g.rows(
        c,
        """SELECT s.id AS space,
        COUNT(v.id) AS total
        FROM spaces s
        LEFT JOIN visits v
        ON v.space = s.id
        AND v.parked IS NOT NULL
        GROUP BY s.id
        ORDER BY s.id""",
    )

    # Reservaciones vencidas
    expired = g.val(
        c,
        """SELECT COUNT(*) FROM reservations
        WHERE status = 'expired'""",
    )

    # Incidentes sin resolver
    incidents = g.val(
        c,
        """SELECT COUNT(*) FROM incidents
        WHERE resolved = 0""",
    )

    # Usuarios en espera
    waiting = g.val(
        c,
        """SELECT COUNT(*) FROM queue
        WHERE status = 'waiting'""",
    )

    # Espacios bloqueados
    blocked = sum(bool(s["blocked"]) for s in spaces)

    # Espacios asignados pendientes de ocupacion
    assigned = sum(
        s["visit"] is not None and not s["occupied"]
        for s in spaces
    )

    # Historial de eventos
    history = g.rows(
        c,
        """SELECT created, kind, detail
        FROM events
        ORDER BY id DESC LIMIT 100""",
    )

    # Smart Assistant basado en reglas
    alerts = generar_alertas(
        online,
        available,
        waiting,
        incidents,
        expired,
    )

    return {
        "alert": alerts[0],
        "alerts": alerts,
        "completed": completed,
        "average_minutes": round(avg / 60, 1),
        "rotation": counts,
        "expired": expired,
        "incidents": incidents,
        "statistics": estadisticas,
        "available": available,
        "holds": holds,
        "blocked": blocked,
        "assigned": assigned,
        "waiting": waiting,
        "history": history,
        "online": bool(online),
    }