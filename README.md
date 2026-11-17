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

## Cómo ejecutar PARKVISION paso a paso

Para probar el prototipo, es necesario tener Python instalado en la computadora y contar con conexión a Internet para descargar las dependencias.

### Paso 1. Descargar el proyecto

1. Ingresar al repositorio de GitHub:
   https://github.com/elizabethortez02-bot/PARKVISION
2. Presionar el botón verde **Code**.
3. Seleccionar **Download ZIP**.
4. Extraer el archivo descargado.
5. Abrir la carpeta del proyecto en Visual Studio Code.

### Paso 2. Abrir la terminal

En Visual Studio Code, seleccionar **Terminal → New Terminal**.

Verificar que la terminal esté ubicada dentro de la carpeta PARKVISION, donde se encuentran los archivos `requirements.txt` y `README.md`.

### Paso 3. Instalar las dependencias

Ejecutar el siguiente comando:

```cmd
python -m pip install -r requirements.txt
```

Esperar a que finalice la instalación.

### Paso 4. Iniciar el sistema

En la misma terminal, ejecutar:

```cmd
python src/main.py
```

Si el servidor inicia correctamente, aparecerá un mensaje similar a:

```text
Running on http://127.0.0.1:5000
```

### Paso 5. Abrir PARKVISION

1. Mantener abierta la terminal donde se ejecuta Flask.
2. Abrir un navegador, como Google Chrome.
3. Escribir la siguiente dirección:

http://127.0.0.1:5000

4. Presionar Enter.

Se mostrará la interfaz web de PARKVISION con los seis espacios de estacionamiento, sus estados y las estadísticas de disponibilidad.

**Nota importante:** Esta dirección funciona localmente en la computadora donde se ejecuta el proyecto. No es un enlace público de Internet.

### Paso 6. Finalizar la ejecución

Para detener el servidor, regresar a la terminal de Visual Studio Code y presionar `Ctrl + C`.

### Alcance de la prueba

En este primer avance, PARKVISION utiliza el archivo `prueba.jpg` para realizar el análisis de los seis espacios. La integración completa de la cámara para analizar nuevas imágenes continúa en desarrollo.
### Documentación

El documento del primer avance se encuentra en el archivo `Informe_PARKVISION.pdf`.

### Información académica

**Universidad:** Universidad Gerardo Barrios

**Facultad:** Ciencia y Tecnología

**Asignatura:** Programación Computacional III

**Docente:** Ing. William Alexis Montes Girón

**Proyecto:** PARKVISION — Primer avance
