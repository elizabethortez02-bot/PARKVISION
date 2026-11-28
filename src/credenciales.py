"""Generación local de QR y lectura de credenciales desde una fotografía."""
import io, csv
from pathlib import Path
import qrcode, cv2, numpy as np
from PIL import Image, ImageDraw

def qr_png(value):
    out=io.BytesIO();qrcode.make(value).save(out,format='PNG');return out.getvalue()

def leer_qr(raw):
    if not raw or len(raw)>5_000_000:raise ValueError('Imagen inválida o demasiado grande')
    img=cv2.imdecode(np.frombuffer(raw,np.uint8),cv2.IMREAD_COLOR)
    if img is None:raise ValueError('Imagen inválida')
    code,_,_=cv2.QRCodeDetector().detectAndDecode(img)
    if not code:raise ValueError('No se encontró un QR legible')
    return code

def generar_carnets():
    base=Path(__file__).resolve().parent.parent;dest=base/'credenciales_demo';dest.mkdir(exist_ok=True)
    with (base/'padron_demo.csv').open(encoding='utf-8') as f:
        for r in csv.DictReader(f):
            im=Image.new('RGB',(680,400),'#10243a');d=ImageDraw.Draw(im)
            d.text((30,35),'PARKVISION UNIVERSITY',fill='#5eead4');d.text((30,85),r['nombre'],fill='white');d.text((30,125),r['codigo'],fill='white');d.text((30,350),'CREDENCIAL FICTICIA - USO ACADEMICO',fill='white')
            qr=Image.open(io.BytesIO(qr_png(r['codigo']))).convert('RGB').resize((230,230),Image.Resampling.NEAREST);im.paste(qr,(410,75));im.save(dest/(r['codigo']+'.png'))
if __name__=='__main__':generar_carnets()
