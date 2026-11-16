# PARKVISION

## Sistema inteligente de detección y monitoreo de estacionamientos

### Descripción del proyecto

PARKVISION es un prototipo académico desarrollado en Python que utiliza técnicas de visión artificial para identificar espacios de estacionamiento libres y ocupados.

En este primer avance, el sistema analiza una imagen de prueba de seis espacios de estacionamiento y presenta los resultados mediante una interfaz web desarrollada con Flask.

El prototipo permite visualizar la disponibilidad de los espacios, la cantidad de estacionamientos ocupados y los porcentajes correspondientes.

### Integrantes del equipo

| Nombre completo | Carnet |
|---|---|
| Xiomara Elizabeth Alfaro Ortez | SMSS050625 |
| Oscar Alberto Benavides Zelaya | SMSS059925 |
| Alejandro Rafael Estrada Márquez | SMSS054625 |
| Erick Abel León Amaya | SMSS060325 |
| María Fernanda Orellana Argueta | SMSS061825 |
| Carlos David Quinteros Iraheta | SMSS078225 |

### Tecnologías utilizadas

- Python
- OpenCV
- Flask
- HTML y CSS
- Git y GitHub

### Funcionalidades del primer avance

- Procesamiento de imágenes mediante OpenCV.
- Clasificación de seis espacios de estacionamiento.
- Identificación de espacios libres y ocupados.
- Cálculo de estadísticas de disponibilidad.
- Visualización de resultados mediante una interfaz web.

La integración completa de la cámara para la detección automática a partir de nuevas imágenes continúa en desarrollo.

### Ejecución del prototipo

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Iniciar la aplicación:

```bash
python src/main.py
```

Abrir en el navegador:

http://127.0.0.1:5000

### Documentación

El documento del primer avance se encuentra en el archivo `Informe_PARKVISION.pdf`.

### Información académica

**Universidad:** Universidad Gerardo Barrios

**Facultad:** Ciencia y Tecnología

**Asignatura:** Programación Computacional III

**Docente:** Ing. William Alexis Montes Girón

**Proyecto:** PARKVISION — Primer avance
