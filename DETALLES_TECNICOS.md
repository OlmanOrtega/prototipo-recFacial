# Documentación técnica

Explicación de cómo funciona internamente el script de reconocimiento facial.

## 1. Fuentes de imágenes

El script trabaja con dos carpetas:

- **`base_datos/`**: fotos de referencia de la persona que se quiere reconocer (pueden ser varias fotos de la misma persona, tomadas en distintas condiciones).
- **`imagenes/`**: fotos donde se quiere comprobar si esa persona aparece.

Ambas carpetas se filtran por extensión (`.jpg`, `.jpeg`, `.png`, `.jfif`), ignorando cualquier otro archivo que puedan contener.

## 2. Verificación facial con DeepFace

Por cada imagen a analizar, el script la compara contra **cada una** de las fotos de referencia usando:

```python
DeepFace.verify(
    img1_path=ruta_ref,
    img2_path=ruta,
    model_name="Facenet",
    enforce_detection=False,
    silent=True
)
```

- **`model_name="Facenet"`**: DeepFace es una librería que unifica varios modelos de reconocimiento facial bajo una misma interfaz. Acá se usa **FaceNet**, un modelo que convierte cada rostro en un vector numérico (*embedding*) de forma que rostros de la misma persona quedan "cerca" entre sí en ese espacio vectorial, y rostros de personas distintas quedan "lejos".
- **`enforce_detection=False`**: si DeepFace no logra detectar un rostro en alguna de las dos imágenes, no lanza error — sigue adelante con el mejor intento. Es una elección de tolerancia a fallos, útil cuando las fotos no siempre tienen una cara claramente visible, aunque puede generar comparaciones poco confiables si no hay rostro real en la imagen.
- **`silent=True`**: suprime los mensajes de progreso internos de DeepFace en consola.

Internamente, DeepFace detecta el rostro en cada imagen, lo alinea y recorta, calcula su *embedding* con FaceNet, y mide la **distancia** entre ambos embeddings. Si esa distancia es menor a un umbral predefinido por el modelo, se considera `verified: True` (son la misma persona).

## 3. Criterio de "persona encontrada"

Como una foto de la carpeta `imagenes/` se compara contra **todas** las fotos de referencia, basta con que **una sola** comparación dé `verified: True` para marcar la imagen como encontrada:

```python
if resultado['verified']:
    persona_encontrada = True
    mejor_confianza = max(mejor_confianza, 1 - resultado['distance'])
```

La "confianza" mostrada (`1 - distance`) es una forma simplificada de convertir la distancia (donde más bajo = más parecido) en un número más intuitivo (donde más alto = más parecido). No es una probabilidad calibrada, sino una transformación directa de la métrica de distancia del modelo.

Si alguna comparación con la carpeta de referencia falla (por ejemplo, por no detectar rostro en alguna imagen), el error se captura y esa comparación puntual simplemente se ignora, sin detener el procesamiento del resto.

## 4. Salida visual

Cada imagen procesada se convierte a escala de grises y se le superpone un texto (`cv2.putText`) indicando si la persona fue encontrada y con qué nivel de confianza, o si no fue encontrada. Cada resultado se muestra en una ventana individual con `cv2.imshow`, y el script espera una tecla (`cv2.waitKey(0)`) antes de pasar a la siguiente imagen.

## Limitaciones conocidas

- `enforce_detection=False` puede generar comparaciones poco fiables si el rostro no es detectable o no existe en la imagen, ya que DeepFace no aborta la comparación en ese caso.
- El criterio "basta una coincidencia entre todas las fotos de referencia" puede generar falsos positivos si alguna foto de referencia es de baja calidad o ambigua.
- La primera ejecución puede tardar más de lo normal porque DeepFace descarga automáticamente los pesos preentrenados del modelo FaceNet si no los encuentra en caché local.
