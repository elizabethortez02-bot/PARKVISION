"""Indicadores calculados exclusivamente con registros existentes."""
import time
import gestion as g


def resumen(c, online):
    spaces, free, holds, available = g.capacity(c)
    completed = g.val(c, "SELECT count(*) FROM visits WHERE status='closed' AND parked IS NOT NULL")
    avg = g.val(c, "SELECT coalesce(avg(exited-entered),0) FROM visits WHERE status='closed' AND parked IS NOT NULL")
    counts = g.rows(c, "SELECT space, count(*) total FROM visits WHERE parked IS NOT NULL GROUP BY space ORDER BY space")
    alert = (
        'Cámara desconectada: accesos suspendidos' if not online
        else 'Sin cupos directos: utilice la fila virtual' if not available
        else 'Demanda alta: queda un cupo directo' if available == 1
        else 'Disponibilidad normal'
    )
    return dict(
        alert=alert,
        completed=completed,
        average_minutes=round(avg / 60, 1),
        rotation=counts,
        expired=g.val(c, "SELECT count(*) FROM reservations WHERE status='expired'"),
        incidents=g.val(c, "SELECT count(*) FROM incidents WHERE resolved=0"),
    )