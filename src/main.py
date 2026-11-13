
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return """
    <h1>Bienvenido a PARKVISION</h1>
    <h2>Sistema inteligente de estacionamiento</h2>
    <p>Servidor web funcionando correctamente.</p>
    <p>Estacionamientos disponibles: 6</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
