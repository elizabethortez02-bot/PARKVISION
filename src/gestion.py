"""Reglas de negocio independientes de Flask y de la cámara."""
import sqlite3, time, secrets, math
from contextlib import contextmanager
from pathlib import Path
DB=Path(__file__).resolve().parent.parent/'datos'/'gestion.db'
@contextmanager
def tx():
    DB.parent.mkdir(exist_ok=True,parents=True)
    c=sqlite3.connect(DB,timeout=15); c.row_factory=sqlite3.Row
    try:
        c.execute('PRAGMA foreign_keys=ON'); c.execute('BEGIN IMMEDIATE'); yield c; c.commit()
    except Exception: c.rollback(); raise
    finally: c.close()
def init():
    with tx() as c:
        c.executescript('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE, password TEXT, role TEXT);
        CREATE TABLE IF NOT EXISTS vehicles(id INTEGER PRIMARY KEY, uid INTEGER REFERENCES users(id), plate TEXT UNIQUE, model TEXT);
        CREATE TABLE IF NOT EXISTS spaces(id INTEGER PRIMARY KEY, occupied INTEGER DEFAULT 0, blocked INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS reservations(id INTEGER PRIMARY KEY, uid INTEGER, vid INTEGER, code TEXT UNIQUE, expires REAL, status TEXT);
        CREATE TABLE IF NOT EXISTS queue(id INTEGER PRIMARY KEY, uid INTEGER, vid INTEGER, status TEXT, expires REAL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS visits(id INTEGER PRIMARY KEY, uid INTEGER, plate TEXT, space INTEGER, entered REAL, parked REAL, exited REAL, status TEXT, amount INTEGER DEFAULT 0, paid INTEGER DEFAULT 0, rate INTEGER DEFAULT 100);
        CREATE TABLE IF NOT EXISTS incidents(id INTEGER PRIMARY KEY, space INTEGER, description TEXT, created REAL, resolved INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value INTEGER);
        CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, created REAL, kind TEXT, detail TEXT);
        CREATE TABLE IF NOT EXISTS gates(id INTEGER PRIMARY KEY, gate TEXT, created REAL, done INTEGER DEFAULT 0);''')
        c.executemany('INSERT OR IGNORE INTO spaces(id) VALUES(?)',[(i,) for i in range(1,7)])
        c.executemany('INSERT OR IGNORE INTO settings VALUES(?,?)',[('limit', 2),
        ('minutes', 10),
        ('rate', 0)
    ]
)
def rows(c,q,p=()): return [dict(r) for r in c.execute(q,p)]
def val(c,q,p=()): return c.execute(q,p).fetchone()[0]
def setting(c,k): return val(c,'SELECT value FROM settings WHERE key=?',(k,))
def event(c,k,d): c.execute('INSERT INTO events(created,kind,detail) VALUES(?,?,?)',(time.time(),k,d))
def capacity(c):
    spaces=rows(c,"SELECT s.*, (SELECT id FROM visits v WHERE v.space=s.id AND v.status IN ('assigned','parked','leaving') LIMIT 1) visit FROM spaces s ORDER BY id")
    free=[s['id'] for s in spaces if not s['occupied'] and not s['blocked'] and s['visit'] is None]
    holds=val(c,"SELECT count(*) FROM reservations WHERE status='active'")+val(c,"SELECT count(*) FROM queue WHERE status='offered'")
    return spaces,free,holds,max(0,len(free)-holds)
def tick(c,online):
    now=time.time(); c.execute("UPDATE reservations SET status='expired' WHERE status='active' AND expires<=?",(now,)); c.execute("UPDATE queue SET status='expired' WHERE status='offered' AND expires<=?",(now,))
    if not online:return
    _,free,holds,available=capacity(c)
    for _ in range(min(available,max(0,setting(c,'limit')-holds))):
        q=c.execute("SELECT id FROM queue WHERE status='waiting' ORDER BY id LIMIT 1").fetchone()
        if not q:break
        c.execute("UPDATE queue SET status='offered',expires=? WHERE id=?",(now+120,q[0]))
def require(ok,msg):
    if not ok:raise ValueError(msg)
def vehicle(c,uid,vid):
    v=c.execute('SELECT * FROM vehicles WHERE id=? AND uid=?',(vid,uid)).fetchone(); require(v,'Vehículo no válido'); return v
def busy(c,uid,plate):
    return val(c,"SELECT count(*) FROM visits WHERE status!='closed' AND (uid=? OR plate=?)",(uid,plate)) or val(c,"SELECT count(*) FROM reservations WHERE uid=? AND status='active'",(uid,)) or val(c,"SELECT count(*) FROM queue WHERE uid=? AND status IN ('waiting','offered')",(uid,))
def reserve(c,uid,vid,online,offer=False):
    v=vehicle(c,uid,vid); require(online,'Fuente no disponible'); _,free,holds,available=capacity(c)
    if not offer:
        require(not busy(c,uid,v['plate']),'Ya tienes una operación activa'); require(available>0 and holds<setting(c,'limit'),'No hay cupos reservables'); require(not val(c,"SELECT count(*) FROM queue WHERE status='waiting'"),'Hay usuarios en espera')
    else: require(len(free)>=holds,'Conflicto de capacidad')
    code=secrets.token_hex(5).upper(); c.execute("INSERT INTO reservations(uid,vid,code,expires,status) VALUES(?,?,?,?,'active')",(uid,vid,code,time.time()+60*setting(c,'minutes'))); event(c,'reserva',code); return code
def enter(c,plate,code,online):
    require(online,'Fuente no disponible'); _,free,holds,available=capacity(c); uid=None; r=None
    if code:
        r=c.execute("SELECT r.*,v.plate FROM reservations r JOIN vehicles v ON v.id=r.vid WHERE code=? AND status='active'",(code.upper(),)).fetchone(); require(r,'Código inválido o vencido'); plate=r['plate']; uid=r['uid']; require(len(free)>=holds,'Capacidad comprometida')
    else:
        require(available>0,'Sin cupo directo'); require(not val(c,"SELECT count(*) FROM queue WHERE status='waiting'"),'Hay fila pendiente'); v=c.execute('SELECT uid FROM vehicles WHERE plate=?',(plate,)).fetchone(); uid=v[0] if v else None
        if uid:require(not busy(c,uid,plate),'Usuario tiene operación activa')
    require(plate and len(plate)<=24,'Placa requerida'); require(not val(c,"SELECT count(*) FROM visits WHERE plate=? AND status!='closed'",(plate,)),'Vehículo ya ingresado'); require(free,'Sin espacio físico')
    space=free[0]; c.execute("INSERT INTO visits(uid,plate,space,entered,status,rate) VALUES(?,?,?,?,'assigned',?)",(uid,plate,space,time.time(),setting(c,'rate')))
    if r:c.execute("UPDATE reservations SET status='used' WHERE id=?",(r['id'],))
    event(c,'entrada',f'{plate} P{space:02}'); c.execute("INSERT INTO gates(gate,created) VALUES('entrada',?)",(time.time(),)); return space
def detect(c,states):
    require(len(states)==6,'Se esperan seis espacios')
    for i,o in enumerate(states,1):
        old=val(c,'SELECT occupied FROM spaces WHERE id=?',(i,)); c.execute('UPDATE spaces SET occupied=? WHERE id=?',(int(o),i))
        if old==int(o):continue
        event(c,'ocupacion',f'P{i:02}: '+('ocupado' if o else 'libre'))
        v=c.execute("SELECT * FROM visits WHERE space=? AND status!='closed'",(i,)).fetchone()
        if o and not v:
            c.execute('INSERT INTO incidents(space,description,created) VALUES(?,?,?)',(i,'Ocupación por verificar' if v else 'Ocupación sin asignación',time.time()))
        if not o and v and v['status']=='parked':c.execute("UPDATE visits SET status='leaving' WHERE id=?",(v['id'],))
def amount(v): return math.ceil(max(0,(v['exited'] or time.time())-v['entered']-900)/1800)*v['rate']//2
