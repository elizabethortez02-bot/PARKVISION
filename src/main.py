
# PARKVISION
# Servidor web principal

from flask import Flask, render_template
from pathlib import Path

# Ubicar la carpeta templates del proyecto
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(RUTA_PROYECTO / "templates")
)


@app.route("/")
def inicio():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
