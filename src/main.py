
# PARKVISION
# Servidor web principal

from flask import Flask, render_template
from pathlib import Path
from deteccion import detectar_espacios
from camara import iniciar_camara

# Ubicar la carpeta templates del proyecto
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(RUTA_PROYECTO / "templates")
)


@app.route("/")
def inicio():
    estados = detectar_espacios()

    disponibles = estados.count(False)
    ocupados = estados.count(True)

    return render_template(
        "index.html",
        estados=estados,
        disponibles=disponibles,
        ocupados=ocupados,
        total=len(estados)
    )

@app.route("/camara")
def abrir_camara():
    iniciar_camara()
    return "La cámara se ha cerrado correctamente."

if __name__ == "__main__":
    app.run(debug=True)
