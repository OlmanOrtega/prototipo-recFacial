# Reconocimiento Facial

Script en Python que verifica si una persona de referencia aparece en un conjunto de imágenes, usando la librería [DeepFace](https://github.com/serengil/deepface) con el modelo **FaceNet**.

## Descripción general

El script recibe dos carpetas:

1. **`base_datos/`**: una o más fotos de referencia de la persona a reconocer.
2. **`imagenes/`**: las fotos donde se quiere comprobar si esa persona aparece.

Por cada imagen en `imagenes/`, la compara contra todas las fotos en `base_datos/`. Si alguna comparación resulta positiva, se considera que la persona fue encontrada. El resultado se muestra en pantalla sobre la imagen en escala de grises, junto con un nivel de confianza.

[Documentación técnica detallada](DETALLES_TECNICOS.md)

## Requisitos

- **Python 3.10** (versión con la que fue probado el proyecto). TensorFlow 2.16.1 no es compatible con Python 3.12/3.13 en esta combinación de versiones, así que usar una versión más nueva de Python va a romper la instalación.
- **Windows:** requiere el [Visual C++ Redistributable 2015-2022 (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe) instalado. Sin esto, TensorFlow falla al importarse con un error de tipo `DLL load failed`.
- Conexión a internet la primera vez que se ejecuta (DeepFace descarga los pesos del modelo FaceNet automáticamente).

### Dependencias de Python

Las versiones en `requirements.txt` están **fijadas con `==`, no con `>=`, a propósito**. No es un descuido: TensorFlow, Keras, NumPy y OpenCV son sensibles a la versión exacta entre sí, y actualizar una sin las demás puede romper el proyecto entero. Las más críticas, que deben mantenerse alineadas entre sí, son:

```
tensorflow==2.16.1
tensorflow-intel==2.16.1
tf-keras==2.16.0
numpy==1.26.4
opencv-python==4.10.0.84
```

> **`keras` vs `tf-keras`:** no son lo mismo. Este proyecto necesita el paquete **`tf-keras`** (compatibilidad con la API de Keras 2), no el paquete `keras` standalone que instala Keras 3 por defecto. Si falta `tf-keras`, DeepFace falla con `ValueError: ... requires tf-keras package`.

> **`tensorflow-intel`:** esta dependencia es **solo para Windows**. Si estás en Mac o Linux, quitá esa línea del `requirements.txt` antes de instalar — el paquete no existe para esos sistemas y la instalación va a fallar si la dejás.

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/OlmanOrtega/prototipo-recFacial.git
cd prototipo-recFacial

# Crear un entorno virtual
python3.10 -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt
```

**Importante:** activá el entorno virtual (`venv`) *antes* de correr `pip install` o `python main.py`. Si no está activado, `pip install` puede terminar instalando todo en el Python global de tu sistema en vez del `venv` del proyecto, y vas a tener errores confusos donde `pip check` dice que todo está bien pero el programa igual falla al ejecutarse. Para confirmar que estás usando el Python correcto:

```bash
python -c "import sys; print(sys.executable)"
```

Esto debe apuntar a una ruta dentro de la carpeta `venv/` del proyecto, no a tu instalación global de Python.

## Uso

1. Colocá una o más fotos de la persona a reconocer dentro de la carpeta `base_datos/`.
2. Colocá las fotos a analizar dentro de la carpeta `imagenes/`.
3. Ejecutá:

```bash
python main.py
```

4. Cada imagen procesada se muestra en una ventana con el resultado superpuesto (`Olman encontrado (confianza)` o `No Olman bla bla`). Presioná cualquier tecla para pasar a la siguiente imagen.

## Estructura de carpetas esperada

```
proyecto/
├── main.py
├── base_datos/
│   └── (fotos de referencia)
└── imagenes/
    └── (fotos a analizar)
```

## Troubleshooting

| Error | Causa / Solución |
|---|---|
| `DLL load failed while importing _pywrap_tensorflow_internal` | Falta el Visual C++ Redistributable en Windows, o la instalación de TensorFlow quedó corrupta. Instalá el [VC++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) y reinstalá TensorFlow si el error persiste. |
| `ModuleNotFoundError: No module named 'tf_keras'` | Falta el paquete `tf-keras`. Instalalo con `pip install tf-keras==2.16.0`. |
| `opencv-python has requirement numpy>=2, but you have numpy 1.26.4` | Se instaló una versión de `opencv-python` más nueva que la fijada en el proyecto. Usá exactamente `opencv-python==4.10.0.84`, no una versión más reciente. |

## Limitaciones conocidas

- No detecta rostros con precisión garantizada si la imagen tiene mala iluminación, ángulos extremos u oclusiones (lentes, mascarillas, etc.).
- El primer análisis de cada sesión puede ser más lento por la descarga/carga del modelo FaceNet.
- Está pensado para comparar contra **una** persona objetivo por ejecución; no distingue ni etiqueta múltiples personas distintas dentro de las fotos de referencia.
