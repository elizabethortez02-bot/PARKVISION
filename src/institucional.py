"""Identidad única y acceso temporal; todas las operaciones usan la transacción de gestión."""
import hashlib, secrets, time, csv
from pathlib import Path
import gestion as g
from werkzeug.security import generate_password_hash
# Duracion del acceso temporal en segundos
QR_DURACION = 90

def init(c):
    c.execute('CREATE TABLE IF NOT EXISTS padron(codigo TEXT PRIMARY KEY,nombre TEXT NOT NULL,activo INTEGER NOT NULL,uid INTEGER UNIQUE REFERENCES users(id))')
    c.execute('CREATE TABLE IF NOT EXISTS qr_tokens(hash TEXT PRIMARY KEY,uid INTEGER NOT NULL REFERENCES users(id),expires REAL NOT NULL,used INTEGER DEFAULT 0)')
    with (Path(__file__).resolve().parent.parent/'padron_demo.csv').open(encoding='utf-8',newline='') as f:
        for r in csv.DictReader(f):
            c.execute('INSERT OR IGNORE INTO padron(codigo,nombre,activo) VALUES(?,?,?)',(r['codigo'],r['nombre'],int(r['activo'])))

def identify(c,code):
    code=str(code).strip().upper()
    r=c.execute('SELECT * FROM padron WHERE codigo=? AND activo=1',(code,)).fetchone()
    g.require(r,'Carnet inexistente o deshabilitado')
    uid=r['uid']
    if uid is None:
        uid=c.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,'driver')",(r['nombre'],code.lower()+'@institucional.invalid',generate_password_hash(secrets.token_urlsafe(32)))).lastrowid
        c.execute('UPDATE padron SET uid=? WHERE codigo=?',(uid,code))
    return dict(id=uid,name=r['nombre'],code=code,vehicles=g.rows(c,'SELECT * FROM vehicles WHERE uid=?',(uid,)))

def issue(c, uid):
    token = secrets.token_urlsafe(32)
    now = time.time()
    expires = now + QR_DURACION
 
    # Eliminar tokens vencidos y anteriores
    c.execute(
        'DELETE FROM qr_tokens WHERE expires<=? OR uid=?',
        (now, uid)
    )
 
    # Proteger el token mediante SHA-256
    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()
 
    # Registrar el nuevo acceso temporal
    c.execute(
        'INSERT INTO qr_tokens(hash,uid,expires) VALUES(?,?,?)',
        (token_hash, uid, expires)
    )
 
    return token, expires

def redeem(c,token):
    h=hashlib.sha256(str(token).encode()).hexdigest()
    r=c.execute('SELECT t.uid FROM qr_tokens t JOIN padron p ON p.uid=t.uid WHERE t.hash=? AND t.used=0 AND t.expires>? AND p.activo=1',(h,time.time())).fetchone()
    g.require(r,'QR vencido, inválido o utilizado')
    c.execute('UPDATE qr_tokens SET used=1 WHERE hash=?',(h,));return r['uid']

def enter(c,code,plate,model,online):
    u=identify(c,code);uid=u['id'];plate=str(plate).strip().upper()
    g.require(plate and len(plate)<=24,'Placa requerida')
    v=c.execute('SELECT * FROM vehicles WHERE plate=?',(plate,)).fetchone()
    g.require(not v or v['uid']==uid,'Placa vinculada a otro usuario')
    if not v:c.execute('INSERT INTO vehicles(uid,plate,model) VALUES(?,?,?)',(uid,plate,str(model)[:80]))
    r=c.execute("SELECT r.code,v.plate FROM reservations r JOIN vehicles v ON v.id=r.vid WHERE r.uid=? AND r.status='active'",(uid,)).fetchone()
    g.require(not r or r['plate']==plate,'La reserva corresponde a otro vehículo')
    return g.enter(c,plate,r['code'] if r else '',online)
