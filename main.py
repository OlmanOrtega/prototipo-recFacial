from deepface import DeepFace
import cv2
import os

carpetaBD= "base_datos"   
carpeta = "imagenes"

# Cargar fotos
fotos_referencia = [f for f in os.listdir(carpetaBD) 
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.jfif'))]

if not fotos_referencia:
    print("No foto base_datos")
    exit()

print(f"{len(fotos_referencia)} foto(s) de referencia cargada(s)")

# Procesar imagen
for archivo in os.listdir(carpeta):
    if not archivo.lower().endswith(('.jpg', '.jpeg', '.png', '.jfif')):
        continue
        
    ruta = os.path.join(carpeta, archivo)
    img = cv2.imread(ruta)
    if img is None:
        continue
    
    persona_encontrada = False
    mejor_confianza = 0
    
    for foto_ref in fotos_referencia:
        ruta_ref = os.path.join(carpetaBD, foto_ref)
        
        try:
            resultado = DeepFace.verify(
                img1_path=ruta_ref,
                img2_path=ruta,
                model_name="Facenet",
                enforce_detection=False,
                silent=True
            )
            
            if resultado['verified']:
                persona_encontrada = True
                mejor_confianza = max(mejor_confianza, 1 - resultado['distance'])
                
        except Exception:
            continue
    
    # Convertir escala de grises
    img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if persona_encontrada:
        texto = f"Persona encontrada umbral de confianza ({mejor_confianza:.2f})"
        color_texto = 255  # Blanco en grises
    else:
        texto = "Persona no encontrada"
        color_texto = 255  
    
    # Agregar texto a la imagen en grises
    cv2.putText(img_gris, texto, (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_texto, 2)
    
    # Mostrar
    cv2.imshow(f"Resultado - {archivo}", img_gris)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print(f"  {archivo}: {texto}")

print("\nProceso completado")
